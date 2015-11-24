from socket import *
import sys

#http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html



def main():
#recuperando agumentos da linha de comando
#>receptor <hostname do rementente> <numero de porta do rementente> <nome do arquivo>
	
	if (len(sys.argv) > 3):
		hostname = sys.argv[1]
		numPortRem = int(sys.argv[2])
		nomeArq = sys.argv[3]
	
		recebendo = 1
		while recebendo:
	
			receptorSocket = socket(AF_INET, SOCK_DGRAM)
			receptorSocket.sendto(nomeArq,(hostname, numPortRem))
			respostas = receptorSocket.recvfrom(2048)

			#if resposta fim da mensagem recebendo = 0

		receptorSocket.close()
	else:
		print "Espera-se os argumentos: hostname do rementente, numero de porta do rementente e nome do arquivo."



main()
