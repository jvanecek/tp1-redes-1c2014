TP1 de Redes
================

Un captador de paquetes de red (sniffer) para analizar una lan predeterminada. 

Puede tomar paquetes de una red al vuelo, o tomarlos de un archivo. 

Permite luego tener un listado de todas las ips que mandaron paquetes y la cantidad que lo hicieron, asi como las ips que recibieron y la cantidad. Ademas guarda la cantidad de veces que dos ips se comunican, y permite guardar un grafo en formato .dot de estas comunicaciones. 

Uso: escucha_pasiva.py [file/lan] [archivo_entrada/archivo_salida] [tiempo_sniff]'

[file/lan] 
	- file permite levantar los paquetes de un archivo. El nombre del archivo va en el segundo parametro. 
	- lan permite leer los paquetes capturados de la placa de red. Son necesarios los otros dos parametros. 

[archivo_entrada/archivo_salida] 
	- dependiendo de la primera opcion, esto es o de donde se levantan los paquetes, o donde se guardan

[tiempo_sniff] 
	- si la primera opcion es file, este es el tiempo en minutos de escucha de la red. 

