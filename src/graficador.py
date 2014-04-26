import networkx as nx
import matplotlib.pyplot as plt

from operator import itemgetter
from sniffer import *

class graficador:
	def print_ipssrc_graph(self, file):
		s = sniffer()
		s.read_from_file(file)

		total_pkts = s.total_pkts()

		g = nx.Graph()

		for src in s.comunicaciones.keys():
				for dst in s.comunicaciones[src].keys():
					pkts = s.comunicaciones[src][dst]
					g.add_edge(src,dst,weight=0.1)

		# tamano de los nodos en funcion de la cantidad de paquetes mandados
		node_size = []
		for ip in g: 
			if s.ipssrc.has_key(ip):
				node_size.append( s.ipssrc[ip] / total_pkts * 700+50 )
			else: 
				node_size.append( min( s.ipssrc.values() ) ) 
		
		# color de los nodos en funcion de la entropia		
		ips_info = s.ipssrc_info()
		entropia = s.ipssrc_entropia()
		node_color = []
		for ip in g: 
			if ips_info.has_key(ip) and ips_info[ip] < entropia: # si la informacion de la ip es menor de la entropia es distinguido
				node_color.append(2)
			else:
				node_color.append(0)

		# grafico
		pos=nx.spring_layout(g,iterations=200)
		nx.draw(g,pos,
			node_size=node_size,
			node_color=node_color
			)
		plt.show()

	def print_barras(self, file):
		s = sniffer()
		s.read_from_file(file)

		entropia = s.ipssrc_entropia()
		ips_info = s.ipssrc_info()
		
		ips = ips_info.keys()
		sent_pkts = ips_info.values()

		# grafico
		fig = plt.figure()
		fig.suptitle('Informacion de las IPs', fontsize=20)

		ax = fig.gca()
		
		# entropia
		ax.plot(range(len(sent_pkts)), [entropia] * len(sent_pkts), 'r', linewidth=2.0)

		# informaciones
		ax.bar(range(len(sent_pkts)), sent_pkts, align='center')
		plt.xticks(range(len(sent_pkts)), ips, size='small', rotation=90)

		plt.xlabel('IPs', fontsize=18)
		plt.ylabel('I(s)', fontsize=16)

		plt.show()
