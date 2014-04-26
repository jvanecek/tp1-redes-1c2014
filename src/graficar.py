from graficador import *

files = [
	'../resultados/mc_maipu/mc_maipu_all.txt',
	'../resultados/recursiva/recursiva_all.txt',
	'../resultados/casa_vanecek/casa_all.txt',
	'../resultados/orsna/orsna_all.txt',
	'../resultados/test/casa30_all.txt'
]

g = graficador()
g.print_ipssrc_graph(files[1])
g.print_barras(files[1])