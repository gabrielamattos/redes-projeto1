#!/Python27/python
# -*- coding: utf-8 -*-
from socket import *
import sys

#http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html

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
   

def makeAck(numAck):
	ack = str(numAck) + ";"
	checkSum = checksum(ack, 0)
	ack =  str(checkSum) + ";" + ack
	return ack



def main():
	
	if (len(sys.argv) > 3):
		nomeHost = sys.argv[1]
		nroPort = sys.argv[2]
		numPort = int(sys.argv[2])
		nomeArq = sys.argv[3]
		

		#print len(nomeArq)
		#msgInicial = "0;" + nomeArq
		msgInicial = nomeArq
		#estabelecendo conexao antes de inicializar a transmissao dos dados
		receptorSocket = socket(AF_INET, SOCK_DGRAM)
		receptorSocket.sendto(msgInicial, (nomeHost, numPort))
		print "Requisitando arquivo " + msgInicial + " para o servidor " + nomeHost + " na porta " + nroPort
		nroSeqEsperado = 0
		ack = makeAck(0)
		arquivo = open('ArquivoRecebido.out', 'w')
		while 1:
			resMessage = receptorSocket.recvfrom(8192)[0]
			parts  = resMessage.split(";")
			nroSeqRecebido = int(parts[1])
			print "Numero de sequencia recebido: " + str(nroSeqRecebido) + ". Esperava-se o numero de sequencia: " + str(nroSeqEsperado)
			
			#primeira verificacao a ser feita
			#segundo nossa implementacao, quando o nro de seq for -1 (considerando um pacote nao corrompido)
			#existem duas possibilidades: ou essa eh a ultima parte do arquivo, ou o arquivo nao foi encontrado

			#considerando que o checksum vem logo apos o numero de sequencia no cabecalho, no teste para verificacao ele sera desconsiderado
			#
			verificacao = resMessage.split(";", 1)
			checkSum = int(verificacao[0])
			mensagemSemChecksum = verificacao[1]
			
			somaDoPacote = checksum(mensagemSemChecksum, 1)
			
			soma = checkSum + somaDoPacote
			#nao houve alteracao nos dados
			if(soma == 65535):

				if(nroSeqRecebido == -1):
					if(parts[2] == "Arquivo nao encontrado"):
						arquivo.close()
					else:
						arquivo.write(parts[2])
						arquivo.close()
					break
						
				
				if(nroSeqRecebido == nroSeqEsperado):
					arquivo.write(parts[2])
					ack = makeAck(nroSeqRecebido)
					receptorSocket.sendto(ack, (nomeHost, numPort))
					print "Enviando Ack " + str(nroSeqRecebido)
					nroSeqEsperado = nroSeqEsperado + 1
				else:
					ack = makeAck(nroSeqEsperado)
					receptorSocket.sendto(ack, (nomeHost, numPort))
					print "Reenviando Ack " + str(nroSeqEsperado)
			else:
				ack = makeAck(nroSeqEsperado)
				receptorSocket.sendto(ack, (nomeHost, numPort))
				print "Reenviando Ack " + str(nroSeqEsperado)
				
		receptorSocket.close()	
	else:
		print "Espera-se os argumentos: hostname do rementente, numero de porta do rementente e nome do arquivo."




main()
