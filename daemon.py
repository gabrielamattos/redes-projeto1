# -*- coding: utf-8 -*-
#################################################################################################################
# 	Nome: daemon.py												#
# 	Autor: Breno da Silveira Souza										#														#
# 	Objetivo: Daemon que representa o socket no lado servidor, com intuito de pegar a mensagem, eliminar    #
# comandos maliciosos e traduzir o numero do comando para seu equivalente, alem garantir a execucao do comando. #
# 	Referencias:												#
# - http://www.cyberciti.biz/faq/python-execute-unix-linux-command-examples/					#
# - https://docs.python.org/3/library/subprocess.html#subprocess.Popen	 					#
# - http://wiki.python.org.br/SocketBasico									#
#################################################################################################################

from socket import *
import subprocess
import string

#Estabelecendo a porta
serverPort = 9003
#Criando socket TCP
serverSocket = socket(AF_INET,SOCK_STREAM)
#Associando a porta 9003 com o socket do servidor
serverSocket.bind(("",serverPort))
#Espera pelos pacotes do cliente
serverSocket.listen(1)
a = "|"
b = ";"
c = ">"
d = "<"
e = "1 "
f = "2 "
g = "3 "
h = "4 "


while 1:
	connectionSocket, addr = serverSocket.accept()
	sentence = connectionSocket.recv(1024)
	if len(sentence) > 10:
		menos = "-"
	else:
		menos = ""
	sentence = sentence.replace("REQUEST ","")
	if a in sentence:
		sentence = sentence.replace(a,"")
	if b in sentence:
		sentence = sentence.replace(b,"")
	if c in sentence:
		sentence = sentence.replace(c,"")
	if d in sentence:
		sentence = sentence.replace(d,"")
	if e in sentence:
		sentence = sentence.replace(e,"ps "+menos)
		numero = e
	if f in sentence:
		sentence = sentence.replace(f,"ds "+menos)
		numero = f
	if g in sentence:
		sentence = sentence.replace(g,"finger "+menos)
		numero = g
	if h in sentence:
		sentence = sentence.replace(h,"uptime "+menos)
		numero = h
	comando = subprocess.Popen(sentence, stdout=subprocess.PIPE, shell=True)
	(resposta, err) = comando.communicate()
	resposta = "RESPONSE " + numero + resposta
	connectionSocket.send(resposta)
	connectionSocket.close()

