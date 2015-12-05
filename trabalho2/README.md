# redes-projeto2
O objetivo deste trabalho é usar sockets em UDP juntamente com a linguagem Python de programação para implementar um protocolo de transferência confiável de dados

No nosso projeto, implementamos um protocolo simples de controle de congestionamento baseado em janela (window-based) e construído a partir de um protocolo Go-Back-N. Este protocolo visa o envio de um determinado número de pacotes (via Socket UDP) sem o retorno de um acknowlegmente(ACK) do receptor, desde que haja pacotes disponíveis. Assim, deveremos dividir uma mensagem em pacotes, ou seja, dividir a mensagem em pequenos fragmentos para serem enviadas.

Oberve o uso de dois códigos: o emissor.py e o receptor.py. O programa receptor aturará como um cliente, e o receptor, como um servidor. Na execução do programa receptor, em linha de comando, será passado como argumentos os hostname e a porta do emissor, assim como o nome do arquivo que o receptor quer recuperar do emissor. Já o programa emissor, deverá ser passado como argumento na sua execução, a porta com que se dejsea trabalhar (via linha de comando).

Primeiramente, o receptor enviará para o emissor o arquivo que gostaria de receber. O emissor, recebendo o pedido, irá verificar a existência do arquivo. Se ele existir, deverá dividir o arquivo em vários pacotes menores. Além disso, após a divisão, o emissor deverá incluir algumas informaçõs no cabecalho do pacote. No nosso código, usamos um cabeçalho com as seguintes informações: host do envio, porta para o envio, tamanho do arquivo, número de sequência e o número checksum.

Como nosso protocolo visa uma tranferência confiável de arquivos, deve-se fazer o número checksum para a verificação de perdas ou ruídos no envio das mensagens. O checksum nada mais é que a soma dos diferentes bytes presentes no pacote e, caso houver carry na soma, é feito o wrap around deste carry. Assim, ao enviar o rquivo, o receptor poderá verificar se houve alguma alteração na mensagem recebda durante seu envio.

A nossa janela possui um tamanho fixo igual a 2. Portando, o número de sequência presente no cabeçalho poderá ter o valor 0 ou 1. O tamanho do pacote utilizado é igual a 5. Além disso, no envio e recebimento tanto do pacote quanto dos ACKs, será informado, mediante a escrita na tela, de que processo está sendo executado no momento.


