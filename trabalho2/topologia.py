#!/usr/bin/python
# -*- coding: utf-8 -*- 
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI

# Modo de Usar:
# Abrir um terminal, mudar o diretório de trabalho para a pasta que contém todos os arquivos
# No terminal, digitar: sudo python topologia.py
# Após digitar esse comando, no terminal aparecerá o seguinte: mininet>
# digitar xterm h1 (mininet > xterm h1) - instalar xterm caso não esteja instalado no sistema
# digitar xterm h2 (mininet > xterm h1) 
# Esses comandos abrirão um terminal xterm para cada um dos hosts
# digitar os comandos para rodar os arquivos python em cada um desses terminais, lembrando de
# passar como nome do host emissor o nome definido na topologia.


def simpleTest():

	
	net = Mininet(host=CPULimitedHost, link=TCLink)
	h1 = net.addHost( 'h1', ip='10.0.0.1' ) # h1 is a Host() object
	h2 = net.addHost( 'h2', ip='10.0.0.2' ) # h2 is a Host()
	#s1 = net.addSwitch( 's1' ) # s1 is a Switch() object
	c0 = net.addController( 'c0' ) # c0 is a Controller()
	net.addLink( h1, h2, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True ) # creates a Link() object
	#net.addLink( h2, s1, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True )
	net.start()
	#h2.cmd( 'nohup python2.7 ./receptor.py & ' )
	#h1.cmd( 'nohup python2.7 ./emissor.py & '  )
	CLI( net )
	net.stop()
	
	


simpleTest()
