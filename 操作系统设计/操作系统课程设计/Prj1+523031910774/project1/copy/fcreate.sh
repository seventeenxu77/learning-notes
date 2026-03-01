#!/bin/bash

# 定义文件路径
file_path1="src.txt"
file_path2="dest.txt"

# 定义要设置的buffersize列表，单位为 Byte
buffersizes=(1 10 100 1000 10000 100000 1000000 2000000 )
    # 使用 dd 命令从 /dev/urandom 读取随机数据并写入文件
    dd if=/dev/urandom of="$file_path1" bs=50k count=1  status=none
    for buffersize in "${buffersizes[@]}"; do
            ./copy "$file_path1" "$file_path2" "$buffersize"
    done
