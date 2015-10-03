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
e = "1 "
f = "2 "
g = "3 "
h = "4 "
while 1:
	connectionSocket, addr = serverSocket.accept()
     
	sentence = connectionSocket.recv(1024)
	verificacao = sentence.startswith("REQUEST")
	sentence.replace("REQUEST ","")
	if a in sentence
		sentence.replace(a,"")
	if b in sentence
		sentence.replace(b,"")
	if c in sentence
		sentence.replace(c,"")
	if d in sentence
		sentence.replace(d,"")
	if e in sentence
		sentence.replace(e,"ps -")
	if f in sentence
		sentence.replace(f,"ds -")
	if g in sentence
		sentence.replace(g,"finger -")
	if h in sentence
		sentence.replace(h,"uptime -")
	

	comando = subprocess.Popen(sentence, stdout=subprocess.PIPE, shell=True)
	(resposta, err) = comando.communicate()
	resposta = "RESPONSE " + resposta
	connectionSocket.send(resposta)
	connectionSocket.close()
