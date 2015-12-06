# -*- coding: utf-8 -*-
# Referencias: http://www.cs.sfu.ca/CourseCentral/371/oba2/Sep19.pdf
#http://www.binarytides.com/programming-udp-sockets-in-python/
from socket import *
import sys
import math
import numpy
import threading
import signal

def carry_around_add(a, b):
    c = a + b
    return (c & 0xffff) + (c >> 16)

def checksum(msg):
   s = 0
   for i in range(0, len(msg), 2):
       w = ord(msg[i]) + (ord(msg[i+1]) << 8)
       s = carry_around_add(s, w)
   return ~s & 0xffff
   
#teste = "abcdefghijklmnopqrst"
#chk = checksum(teste)
#msg_type = '\x08;' # ICMP Echo Request
#msg_code = '\x00;' # must be zero
#msg_checksum_padding = '' # "...with value 0 substituted for this field..."
#rest_header = "arquivo;" # from pcap
#entire_message = msg_type + msg_code + msg_checksum_padding + rest_header + teste
#entire_chk = checksum(entire_message)
#print(entire_message)
#print ('{:x}'.format(entire_chk))
#print("Checksum : 0x%04x" % checksum(entire_message))
#new_checked =  "0x%04x;"% entire_chk + rest_header  + teste
#print(new_checked)


#variaveis globais que serao usadas para enviar os dados e receber o ack
tamanhoJanela = 2
numSeqMax = tamanhoJanela - 1
tamanhoPacote = 5
ack = 0
numSeq = 0
numSeqBase = 0

timeout = 2

servidorSocket = socket(AF_INET, SOCK_DGRAM)



# A mensagem sera dividida no tamanho da janela e salva em um vetor de string, o indice do vetor vai representar

def dividirMensagem(tamanhoPacote, mensagem):

	pacotes = []
	tamanho = int(math.ceil(len(mensagem) / (tamanhoPacote * 1.0)))

	for i in range (0, tamanho):
		inicio = i * tamanhoPacote
		fim = inicio + tamanhoPacote
		pacotes.append(mensagem[inicio:fim])

	return pacotes

def receberAck():


	mensagem = servidorSocket.recvfrom(2048)[0]

	global numSeqBase
	global numSeqMax

	parts  = mensagem.split(";")
	ack = int(parts[0])
	print "Ack recebido"

	# verificar se nao eh necessario fazer uso do >=
	if (ack >= numSeqBase):
		numSeqMax = numSeqMax + (ack+1 - numSeqBase)
		numSeqBase = ack
	print numSeqBase
	print numSeqMax


def main():

	if(len(sys.argv)>1):
		numPort = int(sys.argv[1])
		print numPort
		servidorSocket.bind(('', numPort))
	
		while 1:

		
			print "O servidor esta pronto para receber."
			mensagem, enderecoReceptor = servidorSocket.recvfrom(2048)

			numSeqBase = 0
			numSeq = 0
			numSeqMax = tamanhoJanela - 1

			pacotes = dividirMensagem(tamanhoPacote, mensagem)

			#eh criado uma thread para receber os acks do receptor
			t_receptor = threading.Thread(target = receberAck)
			t_receptor.daemon = True
			t_receptor.start()

			#pacote eh transmitido em ordem
			for i in range (0, len(pacotes)):

				if (numSeq <= numSeqMax):
			
					res = str(numSeq) + ";" + pacotes[i] + ";"
					# [melhorar depois] mensagem avisando que foi enviado o pacote
					print "Enviando pacote de dados com cabecalho: " + res + "/" + str(len(pacotes))				    
					servidorSocket.sendto(res, enderecoReceptor)

					numSeq += 1
				#quando atinge o tamanho da janela ele deve reenviar os pacotes
				else:
					#time
					print "Tamanho da janela atingido " + str(i)
					i = ack + 1
					numSeq = i

			
						
		else:
			print "Espera-se o seguinte parametro: numero de porta do servico"

main()
