# Grupo 
* Breno da Silveira Souza 551481
* Gabriela Vanessa Pereira Alves Mattos 551570
* Guilherme Noriyuki Ichi Toshimitsu 386200
* Rodolfo Barcelar 495921


# Introdução e Objetivos

O objetivo deste trabalho é usar sockets em UDP juntamente com a linguagem Python de programação para implementar um protocolo de transferência confiável de dados.

No nosso projeto, implementamos um protocolo simples de controle de congestionamento baseado em janela (window-based) e construído a partir de um protocolo Go-Back-N. Este protocolo visa o envio de um determinado número de pacotes (via Socket UDP). Assim, deveremos dividir uma mensagem em pacotes, ou seja, dividir a mensagem em pequenos fragmentos para serem enviadas. Para tal, foram desenvolvidos dois códigos que serviram como um cliente e um servidor para a aplicação acima mencionada.

### Emissor.py (servidor)

	Este código atuará como um servidor, ou seja, receberá uma solicitação (mensagem) de um cliente e então enviará o arquivo solicitado pelo cliente via UDP. Nosso código, além do envio da solicitação do arquivo para o cliente, será responsável pelas seguintes funções:

#### Dividir o arquivo solicitado em pacotes

	Uma vez solicitado um arquivo pelo cliente, o emissor será responsável por criar pacotes, ou seja, pequenos fragmentos do arquivo para serem enviados, caso o arquivo solicitado exista. Abaixo, o trecho de código responsável pela quebra da mensagem de acordo  com o tamanho do pacote:
    
```python
    def dividirMensagem(tamanhoPacote, mensagem):

		pacotes = []
		tamanho = int(math.ceil(len(mensagem) / (tamanhoPacote * 1.0)))

      	for i in range (0, tamanho):
          inicio = i * tamanhoPacote
          fim = inicio + tamanhoPacote
          pacotes.append(mensagem[inicio:fim])

		return pacotes
```
  
  A função acima é a responsável por dividir a mensagem no tamanho definido do pacote e salvá-la em um vetor de string. Como a mensagem deverá ser recebida em uma ordem correta para posterior montagem do arquivo, utilizou-se um número de sequência para determinar a ordem gerada dos pacotes. No nosso código, o indice do vetor vai representar o número de sequência do pacote.
  
#### Inserir informações no cabeçalho de cada pacote antes de enviá-lo

	Após a geração dos pacotes, deve-se gerar um cabeçalho para cada pacote para que a rede possa ser informada sobre algumas características de envio do pacote e sobre o pacote sendo enviado, uma vez que estamos utilizando um protocolo UDP.
    
```python    
	def gerarMensagem(numS, pacote):
		pacoteSemCheckSum = str(numS) + ";" + pacote + ";"
		valorCheckSum = checksum(pacoteSemCheckSum, 0)
		res = str(valorCheckSum) + ";" + pacoteSemCheckSum

		return res        
```
    
 A função acima é a responsável por gerar o cabeçalho dos pacotes, utilizando os valores de número de sequência e o pacote enviados por parâmetro. Observe que as informações contidas no cabeçalho são:
 * o número de sequência;
 * o número de checksum.
 
Nosso cabeçalho foi mantido o mais simples possível, apenas colocando as informações que são necessárias para o controle da transmissão confiável.

#### Gerar o checksum das informações contidas no pacote

Uma vez que estamos utilizando o protocolo UDP, o envio das informações não é feita de forma a prover determinada segurança em perdas ou alterações nas mensagens enviadas. Por isso, para garantir uma maior confiabilidade no envio e entrega correta dos dados, tanto nosso Servidor quanto nosso Cliente farão o que chamamos de checksum dos bits contidos nos pacotes. Isso garantirá que o receptor saiba se a mensagem sofreu alguma alteração em seu envio e poderá retornar para o emissor que ocorreu alguma falha na mensagem. 

O checksum, basicamente, deverá fazer uma operação de adição nos bits do pacote e, caso haja um carry no bit mais siginificativo, deverá ocorrer um Wrap Around, que é o envio do bit de carry para o bit menos significativo e, então, somá-lo. Após feita a soma de todos os bits, deve-se fazer o complemento de 1 no resultado final. Este valor será o número de checksum enviado.
```python    
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
```

Para a verificação do checksum, basta comparar a soma dos bits da mensagem somado ao valor de checksum no pacote com o número 0xffff. Caso algum valor seja diferente de 1, o checksum indica um erro.

#### Funcionamento e algumas restrições

O emissor abre o arquivo solicitado pelo receptor e, caso exista, faz a leitura de todo o arquivo em uma variável do tipo String. Quando trata-se de um arquivo muito grande, pode ocorrer um erro, pois existe um limite que a String em Python pode suportar, esse limite depende da memória RAM de cada computador. Mais informações: http://stackoverflow.com/questions/7134338/max-size-of-a-file-python-can-open

Após abrir o arquivo e passar para uma String todo o contéudo dele, chega o momento da dividisão em pacotes de um tamanho já definido na variável 'tamanhoPacote'. Acontece a divisão dos pacotes como foi aprensentado na seção 'dividir o arquivo solicitado em pacotes' e, logo depois, começa o envio com o algoritmo Go-Back-N.

É importante destacar como funciona quando acaba de enviar todos os pacotes, inicialmente é realizado um join na thread que recebe ACKs para que o emissor só pare de aguardar o recebimento do ACK quando todos os ACKs forem recebidos, ou seja o ACK recebido é igual ao último número de sequência (len(pacotes) - 1). Após a finalização dessa thread de recebimento, o emissor envia um número de sequência -1, informando que o fim do arquivo chegou e o receptor deve parar de aguardar recebimento de pacote. Fazendo assim com que o emissor possa voltar a ficar aguardando alguma nova solicitação. Observe abaixo o trecho de código que trata isso

```python
	t_receptor.join()
	signal.alarm(0)
	numSeq = -1
	res = gerarMensagem(numSeq, "FIM")	
       print "Enviando pacote de dados de finalizacao da conexão."				    	servidorSocket.sendto(res, enderecoReceptor)
	arquivo.close()

```

#### Outras funcionalidades

Além das funções citadas acima, o emissor deve estar sempre pronto para receber ACKs (acknowledgments), que são os responsáveis por informar à algum outro host sobre o recebimento de algum sinal. A função de receber o ack foi colocada em uma thread separada para que o emissor funcionasse de acordo com o protocolo go-back-n, ou seja, ele não fica parado esperando pelos acks. Esses acks são confirmados em uma trhead rodando em backend, que vai apenas alterar a base da nossa janela.
```python
def receberAck():

	while 1:

		global ack
		mensagem = servidorSocket.recvfrom(2048)[0]
			
		global numSeqBase
		global numSeqMax

		parts  = mensagem.split(";", 1)
		ack = int(parts[1])
		print "Recebido ACK " + parts[1]

		checkSum = int(parts[0])		
		somaDoPacote = checksum(parts[1], 1)

		soma = checkSum + somaDoPacote
		
		
		if (len(parts) == 2):
			if(soma == 65535):		
				if (ack == (len(pacotes)-1)):
					print "Todos os ACKs recebidos."
					break
				if (ack >= numSeqBase):
					numSeqBase = ack + 1
					numSeqMax = numSeqBase + tamanhoJanela-1
					print "Numero seqBase: " + str(numSeqBase)
					print "Numero seqMax: " + str(numSeqMax)
					if (numSeqMax >= len(pacotes)):
						numSeqMax = len(pacotes) - 1
					signal.alarm(timeout)
			else:
				print "Corrupcao no ack recebido!"
		else:
			print "Corrupcao no ack recebido!"
```

Também, são definidas mensagens que aparecerão na  tela, informando os passos de sua execução, como, por exemplo: print "Enviando pacote de dados de finalizacao da conexão." Outra funcionalidade do emissor é uma função que a partir da probabilidade informada verifica se deve ocorrer perda, corrupção ou o envio normal de um determinado pacote. Isso ocorre graças a um número inteiro utilizado para simular essa probabilidade. Após isso fará o envio da mensagem normal, ou corrompida, ou não fará o envio caso seja perda. A função está definida abaixo: 
```  python
def mySendTo(nroSeq, res, enderecoReceptor, probPerda, probCorrupcao):
	if(probPerda < 1):
		probPerda = probPerda * 10
	if(probCorrupcao < 1):
		probCorrupcao = probCorrupcao * 10
	#Para decidir se havera perda ou corrupcao
	x = random.randint(1,10)
	y = random.randint(1,10)

	if(x < probPerda):
		print "Perda do pacote " + str(nroSeq)
	elif (y < probCorrupcao):
		res = "1234;90;0002j;"
		servidorSocket.sendto(res, enderecoReceptor)
	else:
		servidorSocket.sendto(res, enderecoReceptor)
```  
#### Mensagens geradas 
	* res = str(valorCheckSum) + ";" + pacoteSemCheckSum
	* print "Reenviando pacote de dados com cabecalho: " + res + "/" + str(len(pacotes))
	* print "Corrupcao no ack recebido!"
	* print "Numero seqBase: " + str(numSeqBase)
	* print "Numero seqMax: " + str(numSeqMax)
	* print "O servidor esta pronto para receber."
	* print "Arquivo solicitado: " + mensagem
	* print "Enviando pacote de dados com cabecalho: " + res + "/" + str(len(pacotes))	
	* print "Enviando pacote de dados de finalizacao da conexão."
	* print "Arquivo solicitado nao encontrado."
	* print "Espera-se o seguinte parametro: numero de porta do servico, tamanho da janela, probabilidade de perda e probabilidade de 		corrupcao."


#### Para a execução do emissor.py, basta colocar o nome do arquivo com a porta com que se deseja que o emissor envie e receba mensagens, a probabilidade de perda e de corrupção desejada. Por exemplo: "python emissor.py <80> <0.4> <0.1>", em que será utilizada a porta 80, a probabilidade de perda é 0.4 e de corrupção 0.1". 


### Receptor.py (O Cliente)

Este é o código responsável por enviar o nome de um arquivo que deseja receber do emissor e é aquele que irá receber o código do emissor.

#### Calculo do checksum
Uma vez que o receptor deverá receber as mensagens, ele também deverá fazer o cálculo do checksum para ver se a mensagem obtida está corropida, garantindo assim um recebimento mais seguro do arquivo solicitado. Utilizará as mesmas funções descritas anteriormente.

#### Envio dos ACKs
Uma vez que o receptor recebe mensagens do emissor, ele deve enviar os ACKs correspondentes para informar sobre o recebimento correto das mensagens. O envio dos ACKs é feito formulando-se pacotes que serão enviados para o emissor. Basicamente, utiliza-se uma função para criação do pacote do ack, que recebe como parâmetro o número do ack, que é correspondente ao número de sequência que foi recebido por último, sem perda nem corrupção, e na ordem. O pacote é simplesmente formado por um campo de checksum e um campo com o número do ack.
```python
def makeAck(numAck):
	ack = str(numAck)
	checkSum = checksum(ack, 0)
	ack =  str(checkSum) + ";" + ack
	return ack

def mySendTo(numAck, ack, receptorSocket, nomeHost, numPort, probPerda, probCorrupcao):
	if(probPerda < 1):
		probPerda = probPerda * 10
	if(probCorrupcao < 1):
		probCorrupcao = probCorrupcao * 10
	#Para decidir se havera perda ou corrupcao
	x = random.randint(1,10)
	y = random.randint(1,10)

	if(x < probPerda):
		print "Perda do Ack " + str(numAck)
	elif (y < probCorrupcao):
		ack = "1234;90"
		receptorSocket.sendto(ack, (nomeHost, numPort))
	else:
		receptorSocket.sendto(ack, (nomeHost, numPort))
```
Vale lembrar que não é necessário que o emissor envie um ACK quando da requisição enviada pelo receptor. Essa requisição é apenas uma forma de fazer uma conexão entre o próprio receptor e o emissor e, portanto, não há necessidade de envio de ACKs pelo emissor.

Algumas outras funções relacionadas ao receptor está na verificação de corrupção, junção dos pacotes para a formação do arquivo final requisitado, pedir o reenvio de determinados pacotes de acordo com o número da sequência (cujo reenvio será feito pelo emissor).

#### Mensagens geradas

* print "Requisitando arquivo " + msgInicial + " para o servidor " + nomeHost + " na porta " + str(numPort)
* print "A soma do checksum é: " + str(soma)
* print "Numero de sequencia recebido: " + str(nroSeqRecebido) + ". Esperava-se o numero de sequencia: " + str(nroSeqEsperado)
* print "Arquivo nao encontrado"
* print "Enviando Ack " + str(nroSeqRecebido)
* print "Reenviando Ack " + str(ultimoAck)
* print "Corrupcao detectada no pacote!"
* print "Espera-se os argumentos: hostname do rementente, numero de porta do rementente, nome do arquivo, probabilidade de perda (um numero entre 0.0 e 0.4, com uma casa decimal), e probabilidade de corrupcao (um numero entre 0.0 e 0.4, com uma casa decimal)"

#### Para a execução do receptor.py, basta colocar o nome do arquivo, o hostname e a porta utilizada pelo emissor, além do nome do arquivo desejado, todos como parâmetro. Por exemplo: "python receptor.py <0.0.0.0> <80> <myFile.jpg>".

### Topologia

O arquivo topologia.py é um código em python, que utiliza funções do Mininet, e que é responsável por criar a topologia para os nossos testes, ou seja, é responsável por criar uma rede lógica para que possamos testar nossos códigos. Nele, são criados dois hosts h1 e h2 ligados por um linker e um controlador c0. Observe a topologia no código abaixo. Apesar de ser possível determinar parâmetros no link que vão adicionar perda e delay, optamos por deixar o link mais simples e implementamos nossas próprias funções de perda.
```python
def topologia():
	net = Mininet(host=CPULimitedHost, link=TCLink)
	h1 = net.addHost( 'h1', ip='10.0.0.1' ) # h1 is a Host() object
	h2 = net.addHost( 'h2', ip='10.0.0.2' ) # h2 is a Host()
	c0 = net.addController( 'c0' ) # c0 is a Controller()
	net.addLink( h1, h2, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True ) # creates a Link() object
	net.start()
	CLI( net )
	net.stop()

topologia()
```
Para maiores detalhes sobre a topologia, vidde arquivo topologia.py que contém ótimos comentários e instruções que ajudarão em qualquer dúvida.

# Resultados

![](https://github.com/gabrielamattos/redes-ufscar/blob/master/trabalho2/Fotos%20Resultados/12346919_1672828859664888_1624719873_n.jpg)

![](https://github.com/gabrielamattos/redes-ufscar/blob/master/trabalho2/Fotos%20Resultados/12358094_1672828856331555_1731055159_n.jpg)
