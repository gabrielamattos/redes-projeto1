# -*- coding: utf-8 -*-
# Referencias: http://www.cs.sfu.ca/CourseCentral/371/oba2/Sep19.pdf
from socket import *
import sys

def main():

	if(len(sys.argv)>1):
		numPort = int(sys.argv[1])
		ipServidor = ""
		print numPort
		servidorSocket = socket(AF_INET, SOCK_DGRAM)
		servidorSocket.bind((ipServidor, numPort))
		print "The server is ready to receive"
		
		while 1: 
			print "Aqui, teste"
			messagem, endCliente = servidorSocket.recvfrom(2048)
			mensagemModificada = messagem.upper()
			servidorSocket.sendTo(mensagemModificada, endCliente)

	else:
		print "Espera-se o seguinte parametro: numero de porta do serviço"

main()
