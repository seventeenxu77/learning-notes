set terminal pngcairo enhanced font 'Arial,10' size 800,600
set output're.png'

set title "Time and Buffersize"
set xlabel "Buffer Size(Byte)"
set ylabel "Time(ms)"
set logscale x
set xtics (1,10,100,1000,10000,100000,1000000,10000000)
plot "src00.txt" using 2:1 with linespoints \
    linecolor rgb 'blue' \
    pointtype 7 \
    pointsize 1.5 \
    title "50KB Input", \
