# -*- coding: utf-8 -*- 

#################################################################################################################
# 	Nome: backend.py											#
# 	Autor: Rodolfo Barcelar											#
#	Contribuição: Gabriela Mattos										#
# 	Objetivo: funciona como um cliente, ou seja, pega o valor passado pelo WebServer e envia para os 	#
# computadores os executarem.											#
# 	Referências:												#
# - https://docs.python.org/2/howto/sockets.html 								#
# - http://wiki.python.org.br/SocketBasico 									#
#################################################################################################################

# Importando biblioteca do Socket
from socket import *

# Função que define o comando a ser chamado pelo WebServer
def sendMsg(comando):
	# Definindo o IP do servidor
	serverName = '192.168.0.1'
	# Definindo a porta do servidor
	serverPort = 9003 #aqui, temos 9000 + X, sendo X o numero do grupo. Mas nao sei que numero eh nosso grupo
	
	# Criando o mecanismo de socket para receber a conexão
	clientSocket = socket(AF_INET,SOCK_STREAM)
	
	# Tentando conectar com o servidor
	try: 
    		clientSocket.connect(serverName, serverPort)
    		if comando:
      			# Enviando o comando recebido para o servidor... comando TRY..EXCEPT
      			clientSocket.send(comando)
      			# Limpando o comando após o envio
			comando = ""
			# Recebendo o comando do servidor
			dados = clientSocket.rcv(1024) 
			# Validando se a resposta é coerente
			dados = validacaoDosDados(dados) 
		else:
			dados = "Impossivel gerar comando!"

		clientSocket.close()

	except Excecao: #caso a conexao com socket tiver fechado ou nao tiver sido feita
		dados = "Socket sem conexao!"
 
	return dados

def validacaoDosDados(msgRecebida):
	lista = msgRecebida.split() #comando split() separa cada palavra contida na mensagem

	if lista[0] != "RESPONSE":
        	return "Resposta enviada eh incoerente!"

	lista = msgRecebida.split("RESPONSE") #pega tudo que tem na mensagem recebida, menos 'RESPONSE'   

	return  lista[1]
    

