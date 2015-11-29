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
		elif flag ==1:
			val2 = ord('0') + (ord(msg[i+1])<<8)
		val1 = verCarry(val1,val2)
	ret = ~val1 & 0xffff
	return ret

#!/Python27/python
# -*- coding: utf-8 -*-
from socket import *
import sys

#http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html



def main():
	
	if (len(sys.argv) > 3):
		nomeHost = sys.argv[1]
		numPort = int(sys.argv[2])
		nomeArq = sys.argv[3]
		print nomeHost
		print numPort
		print nomeArq
		clientSocket = socket(AF_INET, SOCK_DGRAM)

		clientSocket.sendto(nomeArq, (nomeHost, numPort))

		resMessage = clientSocket.recvfrom(8192)[0]
		clientSocket.close()
		print resMessage
	else:
		print "Espera-se os argumentos: hostname do rementente, numero de porta do rementente e nome do arquivo."




main()
