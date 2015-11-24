# -*- coding: utf-8 -*-
from socket import *
import sys

#http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html



def main():
#recuperando agumentos da linha de comando
#>receptor <hostname do rementente> <numero de porta do rementente> <nome do arquivo>
	
	if (len(sys.argv) > 3):
		nomeHost = sys.argv[1]
		numPort = int(sys.argv[2])
		nomeArq = sys.argv[3]
		print nomeHost
		print numPort
		print nomeArq
		recebendo = 1
		#Esse while deverá ser usado para receber os pacotes do servidor, logo deve pensar um pouco mais em como ele deve ser usado para receber os pacotes aos poucos, acredito que a solicitação do arquivo (sendto) só pode acontecer uma vez
		#while recebendo: 
	
		receptorSocket = socket(AF_INET, SOCK_DGRAM)
		receptorSocket.sendto(nomeArq,(nomeHost, numPort))
		respostas, enderecoServidor = receptorSocket.recvfrom(2048)
		print respostas
			#if resposta fim da mensagem recebendo = 0

		receptorSocket.close()
	else:
		print "Espera-se os argumentos: hostname do rementente, numero de porta do rementente e nome do arquivo."



main()
