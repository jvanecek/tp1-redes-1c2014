#!/usr/bin/gnuplot
# set terminal pngcairo  transparent enhanced font "arial,10" fontscale 1.0 size 500, 350 
# set output 'histograms.6.png'
set border 3 front linetype -1 linewidth 1.000
set boxwidth 0.75 absolute
set style fill   solid 1.00 border lt -1
set grid nopolar
set title "Title" 
set xlabel "IP" 
set ylabel "#ARP" 
set yrange [ 0.00000 : * ] noreverse nowriteback
n = "`awk 'END {print NR}' < test/casa_dst.txt`"
plot 'test/casa_dst.txt' using 2 w boxes title column(1)
#plot 'test/casa_dst.txt' using 2 w boxes title column(1)
pause -1 "Hit any key to continue"

