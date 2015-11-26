# -*- coding: utf-8 -*-
from socket import *
import sys

#http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html


def verCarry(a,b):
	c= a+ b
	return(c & 0xffff) + (c>>16)
#auxiliar do checksum	
def checksum(msg,flag):
	val1 = 0
	for i in range(0, len(msg),2):
		if flag == 0:
			val2 = ord(msg[i]) + (ord(msg[i+1])<<8)
		elif flag ==1
			val2 = ord('0') + (ord(msg[i+1])<<8)
		val1 = verCarry(val1,val2)
	ret = ~val1 & 0xffff
	return ret

#funcao checksum do livro  capitulo 3 para 16 bits usado no ud para saber se foi alterado indevidademente
#https://pt.wikiversity.org/wiki/Introdu%C3%A7%C3%A3o_%C3%A0s_Redes_de_Computadores/Protocolo_UDP
#



def main():
#recuperando agumentos da linha de comando
#>receptor <hostname do rementente> <numero de porta do rementente> <nome do arquivo>
	
	if (len(sys.argv) > 3):
		nomeHost = sys.argv[1]
		numPort = int(sys.argv[2])
		nomeArq = sys.argv[3]
		#WindowSize = int(sys.argv[4])
		#Maxdata =  int(sys.argv[5])
		#tamanho da nossa janela 
		#tamanho maximo do arquivo
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
			
		packList = [] 
		#pacotes a receber
		npackets = 0
		#nro pacotes
		
		

		receptorSocket.close()
	else:
		print "Espera-se os argumentos: hostname do rementente, numero de porta do rementente e nome do arquivo."



main()
