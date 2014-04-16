#! /usr/bin/python
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR) # para que no aparezcan warnings molestos

from scapy.all import *
from sniffer import *

import sys

print len(sys.argv)

if( len(sys.argv) <= 2 or (sys.argv[1] == 'lan' and len(sys.argv) < 4)  ): 
	print 'Formato de uso: escucha_pasiva.py [file/lan] [archivo_entrada/archivo_salida] [tiempo_sniff]'
	sys.exit() 

if( sys.argv[1] == 'file' ):
	print "Se lee del archivo" 
	pkts_file = sys.argv[2]
	
	snf = sniffer()
	snf.read_from_file(pkts_file)

	snf.dump_grafo( "%s_del_archivo.dot" % (pkts_file,) )	
	sys.exit()

if( sys.argv[1] == 'lan' ): 
	print "Se lee de la LAN"
	lan_name = sys.argv[2]
	sniff_time = int(sys.argv[3]) * 60
	 
	snf = sniffer()

	def arp_monitor_callback(pkt):
		return snf.guardar_pkt(pkt)

	sniff(prn=arp_monitor_callback, filter="arp", store=0, timeout=sniff_time)
	
	snf.dump_all( "%s_all.txt" % (lan_name,) )
	snf.dump_src( "%s_src.txt" % (lan_name,) )
	snf.dump_dst( "%s_dst.txt" % (lan_name,) )
	snf.dump_comunicaciones( "%s_com.txt" % (lan_name) )
	snf.dump_grafo( "%s.dot" % (lan_name,) )


