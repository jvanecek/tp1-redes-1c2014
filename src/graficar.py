from graficador import *

if( len(sys.argv) < 2 ): 
	print 'Hace falta un archivo con los paquetes a analizar'
	sys.exit() 

# files = [
# 	'../resultados/mc_maipu/mc_maipu_all.txt',
# 	'../resultados/recursiva/recursiva_all.txt',
# 	'../resultados/casa_vanecek/casa_all.txt',
# 	'../resultados/orsna/orsna_all.txt',
# 	'../resultados/test/casa30_all.txt'
# ]

f = sys.argv[1]

g = graficador()
g.print_ipssrc_grafo(f)
g.print_ipssrc_barras(f)
g.print_ipsdst_barras(f)