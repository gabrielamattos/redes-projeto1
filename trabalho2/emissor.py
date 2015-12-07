# -*- coding: utf-8 -*-
# Referencias: http://www.cs.sfu.ca/CourseCentral/371/oba2/Sep19.pdf
#http://www.binarytides.com/programming-udp-sockets-in-python/
from socket import *
import sys
import math
import numpy
import threading
import signal

#fonte do checksum como base ea stackoverflow.com a maioria das pessoas usa essa funcao como base.
def carry_around_add(a, b):
    c = a + b
    return (c & 0xffff) + (c >> 16)

def checksum(msg, opcao):
   	s = 0
	if len(msg) % 2 == 1:
            msg += "\0"
   	for i in range(0, len(msg), 2):
       		w = ord(msg[i]) + (ord(msg[i+1]) << 8)
       		s = carry_around_add(s, w)
   	if(opcao == 0):
   		return ~s & 0xffff
	else:
		return s & 0xffff
   



#variaveis globais que serao usadas para enviar os dados e receber o ack
tamanhoJanela = 2
numSeqMax = tamanhoJanela - 1
tamanhoPacote = 5
ack = -1
numSeq = 0
numSeqBase = 0
i = 0
checkSum = 0
look = threading.Lock()
pacotes = []

timeout = 5

def definirReenvio(signum, stack):

	look.acquire()
	global timeout
	print 'Houve timeout'
	global i
	global numSeq
	i = ack + 1
	numSeq  = i
	print i		
	print numSeq
	signal.alarm(timeout)

	look.release()

servidorSocket = socket(AF_INET, SOCK_DGRAM)
signal.signal(signal.SIGALRM, definirReenvio)


# A mensagem sera dividida no tamanho da janela e salva em um vetor de string, o indice do vetor vai representar o numero de sequencia
def dividirMensagem(tamanhoPacote, mensagem):

	pacotes = []
	tamanho = int(math.ceil(len(mensagem) / (tamanhoPacote * 1.0)))

	for i in range (0, tamanho):
		inicio = i * tamanhoPacote
		fim = inicio + tamanhoPacote
		pacotes.append(mensagem[inicio:fim])

	return pacotes

def receberAck():

	while 1:

		look.acquire()

		mensagem = servidorSocket.recvfrom(2048)[0]
			
		global numSeqBase
		global numSeqMax
		global i
		global pacotes
		
		global ack		

		parts  = mensagem.split(";")
		ack = int(parts[1])
		print "Recebito ACK " + parts[1]
		
		# verificar se nao eh necessario fazer uso do >=
		if (ack == - 1):
			print "Todos os ACKs recebidos."
			break
		if (ack >= numSeqBase):
			numSeqMax = numSeqMax + (ack - numSeqBase)
			numSeqBase = ack
			signal.alarm(timeout)
		print numSeqBase
		print numSeqMax
		print i

	
		look.release()



def main():
	global i
	global numSeq
	global numSeqBase
	global numSeqMax
	global pacotes
	global ack

	if(len(sys.argv)>1):
		numPort = int(sys.argv[1])
		print numPort
		servidorSocket.bind(('', numPort))

		t_receptor = threading.Thread(target = receberAck)
		t_receptor.daemon = True
	
		while 1:

		
			print "O servidor esta pronto para receber."
			mensagem, enderecoReceptor = servidorSocket.recvfrom(2048)
			print mensagem
	
			try:
				arquivo = open(mensagem, 'r')
				print mensagem
				mensagem = arquivo.read()
				# tratar arquivo nao encontrado aqui
				
				t_receptor.start()
				ack = 0
				numSeqBase = 0
				numSeq = 0
				i = 0
				numSeqMax = tamanhoJanela - 1
	
				pacotes = dividirMensagem(tamanhoPacote, mensagem)
	
				#eh criado uma thread para receber os acks do receptor
	
				signal.alarm(timeout)
	
				#pacote eh transmitido em ordem
				while 1:
					if (i == (len(pacotes) - 1)):
						print numSeq
						break

					if (numSeq <= numSeqMax):
				
   						pacoteSemCheckSum = str(numSeq) + ";" + pacotes[i] + ";"
						valorCheckSum = checksum(pacoteSemCheckSum, 0)
						res = str(valorCheckSum) + ";" + pacoteSemCheckSum
						# [melhorar depois] mensagem avisando que foi enviado o pacote
						print "Enviando pacote de dados com cabecalho: " + res + "/" + str(len(pacotes))				    
						servidorSocket.sendto(res, enderecoReceptor)
	
						numSeq += 1
						i += 1
					#quando atinge o tamanho da janela ele deve reenviar os pacotes
					#else:
						#time
						#print "Tamanho da janela atingido " + str(i)
						#print ack
						#i = ack + 1
						#numSeq = i
					#print i
					#print numSeq
	
				numSeq = -1
				pacoteSemCheckSum = str(numSeq) + ";" + pacotes[i] + ";"
				valorCheckSum = checksum(pacoteSemCheckSum, 0)
				res = str(valorCheckSum) + ";" + pacoteSemCheckSum
				servidorSocket.sendto(res, enderecoReceptor)
				arquivo.close()
				
			except IOError:	
				numSeq = -1
				pacoteSemCheckSum = str(numSeq) + ";Arquivo nao encontrado"
				valorCheckSum = checksum(pacoteSemCheckSum, 0)
				res = str(valorCheckSum) + ";" + pacoteSemCheckSum
				servidorSocket.sendto(res, enderecoReceptor)
	 
				print "Arquivo solicitado nao encontrado."
						

			t_receptor.join()
						
		else:
			print "Espera-se o seguinte parametro: numero de porta do servico"

main()
