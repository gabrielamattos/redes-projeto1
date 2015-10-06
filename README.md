# Redes - Projeto 1 - Servidor de Consultas Linux


Esse projeto tem como intuito demonstrar o funcionamento da interação entre cliente e servidor via CGI a partir da programação de sockets em python. Além disso, enteder a criação de aplicativo servidor multithread nesse contexto.
A aplicação que será desenvolvida permitirá que o usuário possa realizar uma busca de resultados em comando de linha, a partir de um cunjunto de máquinas Linux e através de uma interface Web.


Primeiramente, deverá ser mostrado uma página Web que contem três máquinas separadas por número (máquina 1, 2 e 3), juntamente com um conjunto de comandos que poderão ser executados em uma ou mais máquinas. Esses comandos são iguais para as três máquinas: ps, df, finger e uptime. O webserver é implementado na linguagem python, e será um programa CGI acoplado a um servidor apache.


Uma vez que os comandos forem selecionados e enviados, haverá um programa acoplado ao web server, no qual chamamos de backend, também implementado em python, que servirá como um programa cliente, ou seja, a partir dos comandos selecionados no web server, o backend será responsável por acionar algum servidor e enviar as requisições geradas pelo web server.


Esses servidores são programas que estarão rodando em cada uma das três máquinas e que são chamados "daemons", também implementados em python. Dessa forma, os daemons redirecionarão todas as saídas geradas pela execução dos comandos  para o backend, que juntará todas essas informações e criará uma página web com estes resultados.
Dessa forma, em nosso projeto, está contido:

1- Um programa webserver.py que nada mais é que um programa CGI acoplado a um servidor apache;

2- Uma página HTML em formato de formulário com os dados das requisições e que será servida pelo programa webserver.py (servidor web apache mais CGI);

3- Um programa backend.py, em python, que também será acoplado ao programa webserver.py;

4- Aplicativo daemon. py, em python, que executa os programas localmente, processa a saída e a replica em várias máquinas. Esse aplicativo deverá rodar em qualquer outro backend de outro grupo da disciplica. Dessa forma, padronizou-se a sintaxe dos cabeçalhos do protocólo da camada de aplicação que se comunicam com o daemon, os quais possuem três campos em formato ASCII e em uma única string, separada por espaços:
 
 4-a- Um campo descrevendo o tipo da mensagem como: "REQUEST" ou "RESPONSE";
 
 4-b- Campo descrevendo os comandos suportados, de acordo com o seguinte padrão: 1-"ps", 2-"df", 3-"finger", 4-"uptime";
 
 4-c- Campo contendo argumentos opcionas como, por exemplo, "ps '-ef'"
Assim, além dos comandos, poderão ser executados argumentos para cada tipo do comando. O daemon faz verificações se não são usados parâmetros maliciosos como "|", ";", ">".

