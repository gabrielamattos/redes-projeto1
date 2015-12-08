# -*- coding: utf-8 -*-

#################################################################################################################
# 	Nome: emissor.py											#
# 	Objetivo: atua como servidor UDP com adicao dos servicos de checksum e uso do protocolo Go-Back-N	#
# 	Referencias:												#
# - http://www.cs.sfu.ca/CourseCentral/371/oba2/Sep19.pdf							#
# - http://www.binarytides.com/programming-udp-sockets-in-python/						#
#################################################################################################################


from socket import *
import sys
import math
import numpy
import threading
import signal
import random

#Definição da operação de checksum, com base no link especificado
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
pacotes = []
tamanhoJanela = 2
numSeqMax = tamanhoJanela - 1
numSeq = 0
numSeqBase = 0
end = 0
timeout = 2
ack = -1

lock = threading.Lock()
servidorSocket = socket(AF_INET, SOCK_DGRAM)


# Nome da funcao: gerarMensagem()
# Objetivo: com os valores de número de sequencia e o pacote enviados por parametro, essa funcao vai gerar a mensagem final com checksum
def gerarMensagem(numS, pacote):
	pacoteSemCheckSum = str(numS) + ";" + pacote + ";"
	valorCheckSum = checksum(pacoteSemCheckSum, 0)
	res = str(valorCheckSum) + ";" + pacoteSemCheckSum

	return res

# Nome da funcao: definirReenvio()
# Objetivo: quando atinge o timeout, essa funcao trata de reenviar os pacotes da janela		
def definirReenvio(signum, stack):

	signal.alarm(timeout)
	#ack eh a variavel que representa o ultimo ack confirmado
	for x in range(numSeqBase, numSeqMax+1):
		res = gerarMensagem(x, pacotes[x])
		print "Reenviando pacote de dados com cabecalho: " + res + "/" + str(len(pacotes))				    
		mySendTo(x, res, end, probPerda, probCorrupcao)

# Uso do signal para setar alarme do timeout
signal.signal(signal.SIGALRM, definirReenvio)

# Nome da funcao: mySendTo()
# Objetivo: vai determinar apartir da probabilidade se deve ocorrer perda, corrupcao ou envio normal
def mySendTo(nroSeq, res, enderecoReceptor, probPerda, probCorrupcao):
	if(probPerda < 1):
		probPerda = probPerda * 10
	if(probCorrupcao < 1):
		probCorrupcao = probCorrupcao * 10
	#Para decidir se havera perda ou corrupcao
	x = random.randint(1,10)
	y = random.randint(1,10)

	if(x < probPerda):
		print "Perda do pacote " + str(nroSeq)
	elif (y < probCorrupcao):
		res = "1234;90;0002j;"
		servidorSocket.sendto(res, enderecoReceptor)
	else:
		servidorSocket.sendto(res, enderecoReceptor)
		
# Nome da funcao: dividirMensagem()
# Objetivo: dividir a a mensagem no tamanho definido do pacote e salvar em um vetor de string, o indice do vetor vai representar o numero de sequencia
def dividirMensagem(tamanhoPacote, mensagem):

	pacotes = []
	tamanho = int(math.ceil(len(mensagem) / (tamanhoPacote * 1.0)))

	for i in range (0, tamanho):
		inicio = i * tamanhoPacote
		fim = inicio + tamanhoPacote
		pacotes.append(mensagem[inicio:fim])

	return pacotes

# Nome da funcao: receberAck()
# Objetivo: receber o ack e fazer o deslizamento da janela.
def receberAck():

	while 1:

		global ack
		mensagem = servidorSocket.recvfrom(2048)[0]
			
		global numSeqBase
		global numSeqMax

		parts  = mensagem.split(";", 1)
		if (len(parts) == 2):
			ack = int(parts[1])
			print "Recebido ACK " + parts[1]

			checkSum = int(parts[0])		
			somaDoPacote = checksum(parts[1], 1)

			soma = checkSum + somaDoPacote
			if(soma == 65535):		
				if (ack == (len(pacotes)-1)):
					print "Todos os ACKs recebidos."
					break
				if (ack >= numSeqBase):
					numSeqBase = ack + 1
					numSeqMax = numSeqBase + tamanhoJanela-1
					print "Numero seqBase: " + str(numSeqBase)
					print "Numero seqMax: " + str(numSeqMax)
					if (numSeqMax >= len(pacotes)):
						numSeqMax = len(pacotes) - 1
					signal.alarm(timeout)
			else:
				print "Corrupcao no ack recebido!"
		else:
			print "Corrupcao no ack recebido!"
	

def main():
	global numSeq
	global numSeqBase
	global numSeqMax
	global pacotes
	global end
	global ack
	global tamanhoJanela
	global probPerda
	global probCorrupcao

	tamanhoPacote = 5
	if(len(sys.argv) != 4):

		# Recebimento de parametros
		numPort = int(sys.argv[1])
		tamanhoJanela = int(sys.argv[2])

		# Trata probabilidade de perda
		probPerda = float(sys.argv[3])
		if(probPerda > 0.4 or probPerda < 0.0):
			probPerda = 0.4

		# Trata probabilidade de corrupcao
		probCorrupcao = float(sys.argv[4])
		if(probCorrupcao > 0.4 or probCorrupcao < 0.0):
			probCorrupcao = 0.4		

		# Criacao de conexao com a porta informada
		servidorSocket.bind(('', numPort))

	
		while 1:

			print "O servidor esta pronto para receber."
			mensagem, enderecoReceptor = servidorSocket.recvfrom(2048)
			end = enderecoReceptor

			# Criacao de Thread que ficara executando a funcao receberAck em segundo plano
			t_receptor = threading.Thread(target = receberAck)
			t_receptor.daemon = True			

			try:
				arquivo = open(mensagem, 'r')
				print "Arquivo solicitado: " + mensagem
				mensagem = arquivo.read()

				# Inicia a thread
	
				t_receptor.start()
				
				# Inicia valores dos numeros de sequencias
				numSeqBase = 0
				numSeq = 0
				numSeqMax = tamanhoJanela - 1
				ack = -1
	
				pacotes = dividirMensagem(tamanhoPacote, mensagem)
				
				# O timeout eh usado para decidir quando ocorrerá o reenvio	
				signal.alarm(timeout)
	
				# Transmissao dos pacotes em ordem
				while 1:
					if (numSeq == (len(pacotes)) and ack == (len(pacotes)-1)):
						break

					# Só envia a mensagem quando o numSeq não atingiu o tamanho da janela
					if (numSeq <= numSeqMax and numSeq < len(pacotes)):

						res = gerarMensagem(numSeq, pacotes[numSeq])
						print "Enviando pacote de dados com cabecalho: " + res + "/" + str(len(pacotes))				    
						mySendTo(numSeq, res, enderecoReceptor, probPerda, probCorrupcao)
	
						numSeq += 1

				# Quando o arquivo acaba enviamos o numero de sequencia igual a -1 para que o receptor identifique esse termino
				
				t_receptor.join()
				signal.alarm(0)
				numSeq = -1
				res = gerarMensagem(numSeq, "FIM")	
				print "Enviando pacote de dados de finalizacao da conexão."				    			
				servidorSocket.sendto(res, enderecoReceptor)
				arquivo.close()

			# Quando o arquivo solicitado não existe eh enviado para o receptor o numero de sequencia igual a -1 e a mensagem de arquivo nao encontrado
			except IOError:	

				
				numSeq = -1
				res = gerarMensagem(numSeq, ";Arquivo nao encontrado")
				print "Arquivo solicitado nao encontrado."	
				servidorSocket.sendto(res, enderecoReceptor)
						
						
	else:
		print "Espera-se o seguinte parametro: numero de porta do servico, tamanho da janela, probabilidade de perda e probabilidade de corrupcao."

main()
