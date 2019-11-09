from __future__ import print_function
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import pmonitor
import os
#from time import time
from signal import SIGINT


def CreateTopo():
	os.system('mn -c')
	net = Mininet(link=TCLink, host=CPULimitedHost)	
	
	h1 = net.addHost( 'server', ip='192.168.1.2/24' )
	h2 = net.addHost( 'client', ip='172.16.0.2/24' )

	r1 = net.addHost( 'r1' )

	net.addLink( r1, h1, bw=2, max_queue_size=100 )  # for clarity
	net.addLink( r1, h2, bw=1024, max_queue_size=100 )
	net.build()	

	#Definisi router
	r1.cmd( "ifconfig r1-eth0 0" )
	r1.cmd( "ifconfig r1-eth1 0" )

	r1.cmd("ip addr add 192.168.1.1/24 brd + dev r1-eth0")
	r1.cmd("ip addr add 172.16.0.1/24 brd + dev r1-eth1")
	r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")

	h1.cmd("ip route add default via 192.168.1.1")
	h2.cmd("ip route add default via 172.16.0.1")

	h1.cmd("sysctl -w net.ipv4.tcp_congestion_control=reno")
	h2.cmd("sysctl -w net.ipv4.tcp_congestion_control=reno")

	CLI(net)
	net.stop()

if __name__ == '__main__':
	setLogLevel( 'info' )
	CreateTopo()
