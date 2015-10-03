from socket import *

import subprocess

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(1)
a = "|"
b = ";"
c = ">"
d = "<"
while 1:
	connectionSocket, addr = serverSocket.accept()
     
	sentence = connectionSocket.recv(1024)
	verificacao = sentence.startswith('REQUEST')
	if a in sentence
		sentence.replace(a,"")
	if b in sentence
		sentence.replace(b,"")
	if c in sentence
		sentence.replace(c,"")
	if d in sentence
		sentence.replace(d,"")

	comando = subprocess.Popen(sentence, stdout=subprocess.PIPE, shell=True)
	(resposta, err) = comando.communicate()
	resposta = "RESPONSE" + resposta
	connectionSocket.send(resposta)
	connectionSocket.close()
