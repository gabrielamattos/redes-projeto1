from socket import *

import subprocess

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(1)
print "The server is ready to receive"
x = "|"
y = ";"
z = ">"
while 1:
	connectionSocket, addr = serverSocket.accept()
     
	sentence = connectionSocket.recv(1024)
	verificacao = sentence.startswith('REQUEST')
	if x in sentence
		sentence.replace(x,"")
	if y in sentence
		sentence.replace(y,"")
	if z in sentence
		sentence.replace(z,"")

	comando = subprocess.Popen(sentence, stdout=subprocess.PIPE, shell=True)
	(resposta, err) = comando.communicate()
	resposta = "RESPONSE" + resposta
	connectionSocket.send(resposta)
	connectionSocket.close()
