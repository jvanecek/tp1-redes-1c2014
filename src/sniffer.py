#! /usr/bin/python
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR) # para que no aparezcan warnings molestos

from scapy.all import *
from math import log
from datetime import datetime

def now():
	return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class sniffer: 
	crudo = ""
	ipssrc = {}
	ipsdst = {}
	comunicaciones = {}

	# parsea todos los paquetes guardados en un archivo con el formato dado por dump_all()
	def read_from_file(self, file_name): 
		with open(file_name) as f: 
			lines = f.readlines()

			for line in lines:
				pkt_str = line.split(" ")
				
				pkt = ARP(
					op=1, 
					psrc=pkt_str[2],
					hwsrc=pkt_str[3].strip("(").strip(")"),
					pdst=pkt_str[5],
					hwdst=pkt_str[6].strip("(").strip(")\n")
				)

				self.guardar_pkt(pkt)

	def guardar_pkt(self, pkt): 
		if ARP in pkt and pkt[ARP].op in (1,): #who-has

			src = pkt[ARP].psrc
			dst = pkt[ARP].pdst

			hsrc = pkt[ARP].hwsrc
			hdst = pkt[ARP].hwdst

			if not self.ipssrc.has_key(src): self.ipssrc[src] = 0.0
			if not self.ipsdst.has_key(dst): self.ipsdst[dst] = 0.0
			
			if not self.comunicaciones.has_key(src): self.comunicaciones[src] = {}
			if not self.comunicaciones[src].has_key(dst): self.comunicaciones[src][dst] = 0.0

			self.ipssrc[src] += 1
			self.ipsdst[dst] += 1
			self.comunicaciones[src][dst] += 1

			crudo = "%s: %s (%s) -> %s (%s)" % (now(), src, hsrc, dst, hdst)
			self.crudo += crudo + "\n"

			return crudo

	def total_pkts(self):
		return sum( self.ipssrc.values() )

	def ipssrc_info(self):
		info = {}
		N = sum( self.ipssrc.values() )
		for ip in self.ipssrc:
			info[ip] = - log( self.ipssrc[ip] / N )
		return info

	def ipssrc_entropia(self):
		N = sum(self.ipssrc.values())
		Ps = [ k/N for k in self.ipssrc.values() ]
		H = -sum([ p*log(p,2) for p in Ps ])
		return H

	def dump_all(self, file_name):
		with open(file_name, 'w') as f:
			f.write(self.crudo)
		f.closed

	def dump_src(self, file_name):		
		with open(file_name, 'w') as f:
			for ip, cant in self.ipssrc.iteritems():
				f.write("%s %s\n" % (ip, cant))
		f.closed

	def dump_dst(self, file_name):
		with open(file_name, 'w') as f:
			for ip, cant in self.ipsdst.iteritems():
				f.write("%s %s\n" % (ip, cant))
		f.closed

	def dump_comunicaciones(self, file_name): 
		with open(file_name, 'w') as f: 
			for src in self.comunicaciones.keys():
				for dst in self.comunicaciones[src].keys():
					f.write( "%s %s %s\n" % (src, dst, self.comunicaciones[src][dst]) )
		f.closed

	def dump_grafo(self, file_name):
		with open(file_name, 'w') as f:
			# armo un diccionario (indice => ip) de todas las ips que aparecen en la sniffeada
			indice_ip = {}
			for src in self.ipssrc.keys():
				if not src in indice_ip.values(): indice_ip[len(indice_ip) + 1] = src
			for dst in self.ipsdst.keys():
				if not dst in indice_ip.values(): indice_ip[len(indice_ip) + 1] = dst

			# modifico el diccionario para que quede ip => indice
			indice_ip = dict(zip(indice_ip.values(), indice_ip.keys()))

			f.write("digraph LAN {\n")
			for ip in indice_ip:
				f.write('\t%s [label="%s", shape=circle];\n' % (indice_ip[ip], ip))
			for src in self.comunicaciones:
				for dst in self.comunicaciones[src]:
					f.write('\t%s -> %s [label="%s"];\n' % (indice_ip[src], indice_ip[dst], self.comunicaciones[src][dst]))
			f.write("}\n")
		f.closed 



