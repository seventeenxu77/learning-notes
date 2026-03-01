#!/bin/bash

# 定义参数数组
parameters=(100 200 400 600 800 1000 1200)

# 循环遍历参数数组并调用可执行文件 multi
for param in "${parameters[@]}"; do
    ./multi "$param"
done
