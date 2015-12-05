# -*- coding: utf-8 -*-
# Referencias: http://www.cs.sfu.ca/CourseCentral/371/oba2/Sep19.pdf
#http://www.binarytides.com/programming-udp-sockets-in-python/
from socket import *
import sys
import math
import numpy
import threading
import signal

#variaveis globais que serao usadas para enviar os dados e receber o ack
tamanhoJanela = 2
numSeqMax = tamanhoJanela - 1
tamanhoPacote = 5
ack = 0
numSeq = 0
numSeqBase = 0

timeout = 2



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

	parts  = mensagem.split(";")
	ack = int(parts[0])
	print ack
	print numSeq
	
	# verificar se nao eh necessario fazer uso do >=
	if (ack > numSeqBase):
		numSeqMax = numSeqMax + (ack+1 - numSeqBase)
		numSeqBase = ack


def main():

	if(len(sys.argv)>1):
		numPort = int(sys.argv[1])
		print numPort
		servidorSocket = socket(AF_INET, SOCK_DGRAM)
		servidorSocket.bind(('', numPort))
	
		while 1:
			print "O servidor está pronto para receber."

	
			mensagem, enderecoReceptor = servidorSocket.recvfrom(2048)

			numSeqBase = 0
			numSeq = 0
			numSeqMax = tamanhoJanela - 1

			pacotes = dividirMensagem(tamanhoPacote, mensagem)

			#eh criado uma thread para receber os acks do receptor
			t_receptor = threading.Thread(receberAck)
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
			print "Espera-se o seguinte parametro: numero de porta do serviço"

main()
