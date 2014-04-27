import networkx as nx
import matplotlib.pyplot as plt

from operator import itemgetter
from sniffer import *

class graficador:
	def print_ipssrc_grafo(self, file):
		s = sniffer()
		s.read_from_file(file)

		total_pkts = s.total_pkts()

		#g = nx.cycle_graph(0)
		g = nx.DiGraph()

		for src in s.comunicaciones.keys():
				for dst in s.comunicaciones[src].keys():
					pkts = s.comunicaciones[src][dst]
					g.add_edge(src,dst, weight=0.1)

		# tamano de los nodos en funcion de la cantidad de paquetes mandados
		node_size = []
		for ip in g: 
			if s.ipssrc.has_key(ip):
				node_size.append( s.ipssrc[ip] / total_pkts * 5000+50 )
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

		graphviz_prog = ['twopi', 'gvcolor', 'wc', 'ccomps', 'tred', 'sccmap', 'fdp', 'circo', 'neato', 'acyclic', 'nop', 'gvpr', 'dot', 'sfdp']
		# grafico
		pos=nx.spring_layout(g,iterations=100)
		#pos = nx.shell_layout(g)
		#pos = nx.graphviz_layout(g,prog=graphviz_prog[0],args='-Goverlap=false')
		nx.draw(g,pos,
			node_size=node_size,
			node_color=node_color,
			alpha=0.7,
			edge_color='g'
			)
		plt.show()


	def show_barras(self, ips, pkts_por_ip, entropia): 
		# grafico
		fig = plt.figure()
		fig.suptitle('Informacion de las IPs', fontsize=20)

		ax = fig.gca()
		
		# linea de entropia
		ax.plot(range(len(pkts_por_ip)), [entropia] * len(pkts_por_ip), 'r', linewidth=2.0)

		# barra de informaciones
		ax.bar(range(len(pkts_por_ip)), pkts_por_ip, align='center')
		plt.xticks(range(len(pkts_por_ip)), ips, size='small', rotation=90)

		plt.xlabel('IPs', fontsize=18)
		plt.ylabel('I(s)', fontsize=16)

		plt.show()

	def print_ipssrc_barras(self, file):
		s = sniffer()
		s.read_from_file(file)

		entropia = s.ipssrc_entropia()
		ips_info = s.ipssrc_info()
		
		ips = ips_info.keys()
		sent_pkts = ips_info.values()

		self.show_barras(ips, sent_pkts, entropia)
		

	def print_ipsdst_barras(self, file):
		s = sniffer()
		s.read_from_file(file)

		entropia = s.ipsdst_entropia()
		ips_info = s.ipsdst_info()
		
		ips = ips_info.keys()
		recv_pkts = ips_info.values()

		self.show_barras(ips, recv_pkts, entropia)