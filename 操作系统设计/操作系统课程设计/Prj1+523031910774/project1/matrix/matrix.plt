# 设置图片输出格式和文件名
set term png
set output 'matrix.png'

# 设置标题和坐标轴标签
set title 'Matrix Threads Plot'
set xlabel 'matrix_size'
set ylabel 'time(ms)/size^3'

# 绘制 6 条线
plot 'src1.txt' using 2:1 with linespoints title 'thread:1', \
     'src2.txt' using 2:1 with linespoints title 'thread:2', \
     'src3.txt' using 2:1 with linespoints title 'thread:3', \
     'src4.txt' using 2:1 with linespoints title 'thread:4', \
     'src5.txt' using 2:1 with linespoints title 'thread:5', \
     'src6.txt' using 2:1 with linespoints title 'thread:6'

# 关闭输出
unset output
~              