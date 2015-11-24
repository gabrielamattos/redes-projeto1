from socket import *
import sys

#http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html



def main():
#recuperando agumentos da linha de comando
#>receptor <hostname do rementente> <numero de porta do rementente> <nome do arquivo>
	hostname = sys.argv[1]
	numPortRem = sys.argv[2]
	nomeArq = sys.argv[3]
	
	recebendo = 1
	while recebendo:
	
	receptorSocket = socket(socket.AF_INET, socket.SOCK_DGRAM)
	clientSocket.sendto(nomeArq,(hostname, numPortRem))
	respostas = clientSocket.recvfrom(2048)

	#if resposta fim da mensagem recebendo = 0

clientSocket.close()

main()
