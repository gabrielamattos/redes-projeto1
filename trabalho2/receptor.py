#!/Python27/python
# -*- coding: utf-8 -*-
from socket import *
import sys

#http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html

#segment data e a msgm em si, e numero, e referente a qual numero do back n ele pertence

def preparar_segment(seqnumero,segment_data):
	seq_bits = '{0:032b}'.format(seqnumero)
	#formato de 32 bits de seqnumero
    	checksum = '0' * 16
    	
    	indicator_bits = '01' * 8
    	data = ''
    	for i in range(1,len(segment_data)+1):
    		#vai lendo os dados do data.
        	data_character = segment_data[i-1]
        	data_byte = '{0:08b}'.format(ord(data_character))
        	data = data + data_byte
        	#e soman
    	segment = seq_bits + checksum + indicator_bits + data
    	#junta no segmento total o numero da janela, o indicador de bits, e o valor lido
    	return segment
#preara segment e dpois jogar no checksum... se retornar 0 falhou


#val = preparar_segment(seqnumero,segment_data)
#mensagem_final = fazer_checksum(val)

#Checksum	
def fazer_checksum(msg):
        if msg:
		total = 0	
                data = [msg[i:i+16] for i in range(0,len(msg),16)]
                for y in data:
			total += int(y,2)
			if total >= 65535:
				total -= 65535
		checksum = 65535 - total
		check_sum_bits = '{0:016b}'.format(checksum)
		send_msg = msg[0:32] + check_sum_bits + msg[48:]
		return send_msg
	else:
		return '0'

def makeAck(numAck):

	ack = str(numAck) + ";"
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
			nroSeqRecebido = int(parts[0])
			print "Numero de sequencia recebido: " + str(nroSeqRecebido) + ". Esperava-se o numero de sequencia: " + str(nroSeqEsperado)
			
			#primeira verificacao a ser feita
			#segundo nossa implementacao, quando o nro de seq for -1 (considerando um pacote nao corrompido)
			#existem duas possibilidades: ou essa eh a ultima parte do arquivo, ou o arquivo nao foi encontrado
			if(nroSeqRecebido == -1):
				if(parts[1] == "Arquivo nao encontrado"):
					arquivo.close()
					break
				else:
					arquivo.write(parts[1])
					arquivo.close()
					break
					
	
			if(nroSeqRecebido == nroSeqEsperado):
				#if checksum esta ok
				arquivo.write(parts[1])
				ack = makeAck(nroSeqRecebido)
				receptorSocket.sendto(ack, (nomeHost, numPort))
				print "Enviando Ack " + str(nroSeqRecebido)
				nroSeqEsperado = nroSeqEsperado + 1
			else:
				ack = makeAck(nroSeqEsperado)
				receptorSocket.sendto(ack, (nomeHost, numPort))
				print "Reenviando Ack " + str(nroSeqEsperado)

				
		receptorSocket.close()	
	else:
		print "Espera-se os argumentos: hostname do rementente, numero de porta do rementente e nome do arquivo."




main()
