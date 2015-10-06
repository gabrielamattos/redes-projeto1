#################################################################################################################
# 	Nome: daemon.py												#
# 	Autor: Breno da Silveira Souza										#										#
# 	Objetivo: Daemon que representa o socket no lado servidor, com intuito de pegar a mensagem, eliminar    #
# comandos maliciosos e traduzir o número do comando para seu equivalente, além garantir a execução do comando. #
# 	Referências:												#
# - http://www.cyberciti.biz/faq/python-execute-unix-linux-command-examples/					#
# - https://docs.python.org/3/library/subprocess.html#subprocess.Popen	 					#
# - http://wiki.python.org.br/SocketBasico									#
#################################################################################################################

from socket import *
import subprocess
import string
import thread

#Estabelecendo a porta
serverPort = 9003

def conexao(con, cliente):
	#estabelecendo os padrões a serem procurados na string, os 4 primeiros devem ser ignorados, os 4 ultimos substituidos
	#pelo comando equivalente
	a = "|"
	b = ";"
	c = ">"
	d = "<"
	e = "1 "
	f = "2 "
	g = "3 "
	h = "4 "
	#Recebe a sentença do cliente
	sentence = connectionSocket.recv(1024)
	if len(sentence) > 10:
		menos = "-"
	else:
		menos = ""
	#fazendo as substituicoes necessarias nos padrões
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
	elif f in sentence:
		sentence = sentence.replace(f,"ds "+menos)
		numero = f
	elif g in sentence:
		sentence = sentence.replace(g,"finger "+menos)
		numero = g
	elif h in sentence:
		sentence = sentence.replace(h,"uptime "+menos)
		numero = h
	#executando um processo filho com Ponpen, passando a sentença tratada como parametro
	comando = subprocess.Popen(sentence, stdout=subprocess.PIPE, shell=True)
	#associando a saida com uma variavel de saida
	(resposta, err) = comando.communicate()
	#formulando o cabeçalo de reposta de acordo com o padrão
	resposta = "RESPONSE " + numero + resposta
	#enviando a resposta
	connectionSocket.send(resposta)
	#fechando a conexão
	connectionSocket.close()	
	thread.exit()



#Criando socket TCP
serverSocket = socket(AF_INET,SOCK_STREAM)
#Associando a porta 9003 com o socket do servidor
serverSocket.bind(("",serverPort))
#Espera pelos pacotes do cliente
serverSocket.listen(1)


while 1:
	#quando o cliente bate a porta, o serverSocket chama o método accept
	#e cria um novo socket no servidor chamado connectionSocket que é dedicado a esse cliente
	connectionSocket, addr = serverSocket.accept()
	#inicia uma nova thread para tratar requisicao do cliente
	thread.start_new_thread(conexao, tuple([connectionSocket, addr]))

