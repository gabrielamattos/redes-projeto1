#funciona como um cliente, ou seja, pega o valor passado pelo WebServer e envia para os computadores os executarem
import socket

#definicao do comando a ser chamado pelo WebServer
def sendMsg(comando):
  serverName = '192.168.0.1'
  serverPort = 9003 #aqui, temos 9000 + X, sendo X o nÃºmero do grupo. Mas nÃ£o sei que nÃºmero Ã© nosso grupo
  clientSocket = socket(AF_INET,SOCK_STREAM)
  try: #tentativa de conexão com o servidor
    clientSocket.connect ((serverName, serverPort))
    if comando:
      #envio do comando recebido para o servidor... comando TRY..EXCEPT
      clientSocket.send(comando)
      #devo limpar o comando
      comando = ""
      dados = clientSocket.rcv(1024) #recebo o comando do servidor
      dados = validacaoDosDados(dados) #valido se é uma resposta coerente
    else:
      dados = "ImpossÃ­vel gerar comando!"
    clientSocket.close()
  except Excecao: #caso a conexão com socket tiver fechado ou não tiver sido feita
    dados = "Socket sem conexão!!"
    
return dados
    
  def validacaoDosDados(msgRecebida):
    lista = msgRecebida.split() #comando split() separa cada palavra contida na mensagem
    if lista[0] != "RESPONSE":
        return "Resposta enviada Ã© incoerente!"
    lista = msgRecebida.split("RESPONSE") #pega tudo que tem na mensagem recebida, menos 'RESPONSE'   
    return  lista[1]
    

