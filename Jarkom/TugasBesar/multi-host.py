from mininet.topo import Topo
from mininet.node import Node
#import os
#from mininet.net import Mininet

class LinuxRouter( Node ):
	"Mengaktifkan IP Fordwarding"
	def config( self, **params ):
		super( LinuxRouter, self).config( **params )
		#Mengaktifkan fordwarding pada router
		self.cmd( 'sysctl net.ipv4.ip_forward=1' )

	def terminate( self ):
		self.cmd( 'sysctl net.ipv4.ip_forward=0' )
		super( LinuxRouter, self).terminate()


class MyTopo( Topo ):
	
	#net = Mininet(link=TCLink, host=CPULimitedHost)

	"Topology"
	def __init__(self):
		"Buat Topology"
		#Inisialisasi topologi
		Topo.__init__( self )
		
		#Definisi IP Router
		iprouter = '10.0.1.1/24'

		#Tambahkan Host dan Router
		Router1 = self.addNode( 'r1', cls=LinuxRouter, ip=iprouter )
		Host1 = self.addHost( 'h1', ip='10.0.1.100/24', defaultRoute='via 10.0.1.1' )
		Host2 = self.addHost( 'h2', ip='10.0.2.100/24', defaultRoute='via 10.0.2.1' )
		
		#Buat koneksi, setting max_queue dan bandwitch
		self.addLink( Host1, Router1, bw=2, max_queue_size=100, intfName2='r1-eth1', params2={ 'ip' : iprouter } )
		self.addLink( Host2, Router1, bw=1024, max_queue_size=100, intfName2='r1-eth2', params2={ 'ip' : '10.0.2.1/24'} )
topos = { 'topologi': ( lambda: MyTopo() ) }
