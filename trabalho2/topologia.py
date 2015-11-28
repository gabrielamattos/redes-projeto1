#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI



def simpleTest():
	"Create and test a simple network"
	
	net = Mininet(host=CPULimitedHost, link=TCLink)
	h1 = net.addHost( 'h1' ) # h1 is a Host() object
	h2 = net.addHost( 'h2' ) # h2 is a Host()
	#s1 = net.addSwitch( 's1' ) # s1 is a Switch() object
	c0 = net.addController( 'c0' ) # c0 is a Controller()
	net.addLink( h1, h2, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True ) # creates a Link() object
	#net.addLink( h2, s1, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True )
	net.start()
	#h2.cmd( 'python receptor.py &' )
	#h1.cmd( 'python emissor.py &'  )
	CLI( net )
	net.stop()
	
	


simpleTest()
