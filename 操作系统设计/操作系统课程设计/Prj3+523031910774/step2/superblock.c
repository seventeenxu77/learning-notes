#include"superblock.h"
#include<stdio.h>
#include<string.h>

superblocktype sb;
char diskfile[TOTAL_BLOCK][MAX_BLOCKSIZE];

int write_block(char*buffer,int block_0,int block_num){
        if(block_0+block_num-1<0||block_0+block_num>TOTAL_BLOCK)return -1;
        for(int i=0;i<block_num;i++){
                memcpy(diskfile[block_0+i],buffer+i*MAX_BLOCKSIZE,MAX_BLOCKSIZE);
        }
        return 1;
}
int read_block(char*buffer,int block_0,int block_num){
        if(block_0+block_num-1<0||block_0+block_num>TOTAL_BLOCK)return -1;
        for(int i=0;i<block_num;i++){
                memcpy(buffer+i*MAX_BLOCKSIZE,diskfile[block_0+i],MAX_BLOCKSIZE);
        }
        return 1;
}
void initial_superblock(){
        sb.count_inode=0;
        sb.count_block=133;
        sb.count_inode_free=TOTAL_INODE;
        sb.count_block_free=TOTAL_BLOCK-SYS_BLOCK;
        memset(sb.inode_map, 0, sizeof(sb.inode_map));
        memset(sb.block_map, 0, sizeof(sb.block_map));
        for(int i=0;i<=4;i++){
                sb.block_map[i]=0xFFFFFFFF;
        }
        char buffer[5*MAX_BLOCKSIZE];
        memset(buffer, 0, sizeof(buffer));
        memcpy(buffer,&sb,sizeof(sb));
        write_block(buffer,0,5);
}
int block_allocate(){
        if(!sb.count_block_free)return -1;
        for(int i=5;i<NUM_BLOCK_MAP;i++){//start from the non-sysblock
                uint32_t space_block=sb.block_map[i];
                for(int j=0;j<32;j++){
                        if((space_block>>(31-j)&1)==1)continue;//the 32-j position is 1 means here is occupied,go next position
                        else{
                                space_block=space_block|(1<<(31-j));//occupy the 32-j position of the ith BLOCK_MAP
                                sb.block_map[i]=space_block;
                                sb.count_block_free--;
                                sb.count_block++;
                                char buffer[5*MAX_BLOCKSIZE];
                                memcpy(buffer,&sb,sizeof(sb));
                                if(write_block(buffer,0,5)==-1)return -1;
                                else{
                                        return i*32+j;
                                }
                        }

                }
        }
        return -1;
}
int block_free(uint32_t block_number){//it is a real number not a bitmap
        if(block_number<SYS_BLOCK)return -1;
        int map_num=block_number/32;
        int offset=block_number%32;
        uint32_t space_block=sb.block_map[map_num];
        if((space_block>>(31-offset)&1)==0)return 0;
        else{
                space_block=space_block&(~(1U<<(31-offset)));
                sb.count_block_free++;
                sb.count_block--;
                char buf_1[MAX_BLOCKSIZE];
                memset(buf_1, 0, sizeof(buf_1));
                if(write_block(buf_1,block_number,1)==-1)return -1;
                char buf_2[5*MAX_BLOCKSIZE];
                memcpy(buf_2,&sb,sizeof(sb));
                if(write_block(buf_2,0,5)==-1)return -1;
                return 1;
        }
        return -1;
}

