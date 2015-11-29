#!/Python27/python
# -*- coding: utf-8 -*-
from socket import *
import sys

#http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html


#auxiliar do checksum	
def verCarry(a,b):
	c= a+ b
	return(c & 0xffff) + (c>>16)
	
#funcao checksum do livro  capitulo 3 para 16 bits usado no ud para saber se foi alterado indevidademente		+#!/Python27/python
#https://pt.wikiversity.org/wiki/Introdu%C3%A7%C3%A3o_%C3%A0s_Redes_de_Computadores/Protocolo_UDP
def checksum(msg,flag):
	val1 = 0
	for i in range(0, len(msg),2):
		if flag == 0:
			val2 = ord(msg[i]) + (ord(msg[i+1])<<8)
		elif flag ==1:
			val2 = ord('0') + (ord(msg[i+1])<<8)
		val1 = verCarry(val1,val2)
	ret = ~val1 & 0xffff
	return ret

def main():
	
	if (len(sys.argv) > 3):
		nomeHost = sys.argv[1]
		numPort = int(sys.argv[2])
		nomeArq = sys.argv[3]
		print nomeHost
		print numPort
		print nomeArq
		receptorSocket = socket(AF_INET, SOCK_DGRAM)

		receptorSocket.sendto(nomeArq, (nomeHost, numPort))

		resMessage = receptorSocket.recvfrom(8192)[0]
		receptorSocket.close()
		print resMessage
	else:
		print "Espera-se os argumentos: hostname do rementente, numero de porta do rementente e nome do arquivo."




main()
