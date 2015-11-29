# -*- coding: utf-8 -*-
# Referencias: http://www.cs.sfu.ca/CourseCentral/371/oba2/Sep19.pdf
#http://www.binarytides.com/programming-udp-sockets-in-python/
from socket import *
import sys

def main():

	if(len(sys.argv)>1):
		numPort = int(sys.argv[1])
		print numPort
		servidorSocket = socket(AF_INET, SOCK_DGRAM)
		servidorSocket.bind(('', numPort))
		print "The server is ready to receive"

	
		while 1:
			mensagem, enderecoReceptor = servidorSocket.recvfrom(2048)
	
			res = "RESPONSE " +  " " + mensagem
	
			servidorSocket.sendto(res, enderecoReceptor)
		else:
			print "Espera-se o seguinte parametro: numero de porta do serviço"

main()
