#include"superblock1.h"
#include<stdio.h>
#include<string.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<arpa/inet.h>


superblocktype sb;
extern int diskfd;
char cmd[MAX_BLOCKSIZE+100];
char block_content[MAX_BLOCKSIZE];
char disk_return_buf[MAX_BLOCKSIZE];
char tmp[100];//process interger into string and receive data from disk in the write_block function
//char diskfile[TOTAL_BLOCK][MAX_BLOCKSIZE];

//int write_block(char*buffer,int block_0,int block_num){
//        if(block_0+block_num-1<0||block_0+block_num>TOTAL_BLOCK)return -1;
//      memset(cmd,0,sizeof(cmd));
//      cmd[0]='\0';
//       for(int i=0;i<block_num;i++){
//                //memcpy(diskfile[block_0+i],buffer+i*MAX_BLOCKSIZE,MAX_BLOCKSIZE);
//              memset(block_content,0,sizeof(block_content));
//              memset(disk_return_buf,0,sizeof(disk_return_buf));
//              memset(tmp,0,sizeof(tmp));
//              sprintf(tmp, "%d", block_0+i);
//              strcat(cmd,"W ");
//              strcat(cmd,tmp);
//              memcpy(block_content,buffer+i*MAX_BLOCKSIZE,MAX_BLOCKSIZE);
//              strcat(cmd," ");
//              strcat(cmd,block_content);
//              if (send(diskfd,cmd , sizeof(cmd), 0) < 0) {
//                      perror("ERROR:write_block to disk\n");
//                      return -1;
//              }
//              memset(tmp, 0, sizeof(tmp));
//              int ret = recv(diskfd, disk_return_buf, MAX_BLOCKSIZE, 0);
//              if (ret <= 0) {
//                      perror("ERROR:return data from disk\n");
//                      return -1;
//              }
//        }
//        return 1;
//}
int write_block(char *buffer, int block_0, int block_num) {
    if (block_0 + block_num > TOTAL_BLOCK) {
        fprintf(stderr, "Block write out of range\n");
        return -1;
    }
    char redata[MAX_BLOCKSIZE];
    for (int i = 0; i < block_num; ++i) {
        DiskRequest req;
        req.op = 'W';
        req.blockno = block_0 + i;
        memcpy(req.data, buffer + i * MAX_BLOCKSIZE, MAX_BLOCKSIZE);

        if (send(diskfd, &req, sizeof(req), 0)<0) {
            perror("send write request failed");
            return -1;
        }

        if (recv(diskfd, redata, MAX_BLOCKSIZE, 0) <= 0 ) {
            perror("write response error from disk");
            return -1;
        }
    }

    return 1;
}


//int read_block(char*buffer,int block_0,int block_num){
//        if(block_0+block_num-1<0||block_0+block_num>TOTAL_BLOCK)return -1;
//      memset(cmd,0,sizeof(cmd));
//        cmd[0]='\0';
//        for(int i=0;i<block_num;i++){
//                //memcpy(buffer+i*MAX_BLOCKSIZE,diskfile[block_0+i],MAX_BLOCKSIZE);
//              memset(tmp,0,sizeof(tmp));
//              memset(block_content,0,sizeof(block_content));
//                memset(disk_return_buf,0,sizeof(disk_return_buf));
//                sprintf(tmp, "%d", block_0+i);
//                strcat(cmd,"R ");
//                strcat(cmd,tmp);
//                memcpy(block_content,buffer+i*MAX_BLOCKSIZE,MAX_BLOCKSIZE);
//                strcat(cmd," ");
//                strcat(cmd,block_content);
//                if (send(diskfd,cmd , sizeof(cmd), 0) < 0) {
//                        perror("ERROR:write_block to disk\n");
//                        return -1;
//                }
//                memset(tmp, 0, sizeof(tmp));
//                int ret = recv(diskfd, buffer + i * MAX_BLOCKSIZE, MAX_BLOCKSIZE, 0);
//                if (ret <= 0) {
//                        perror("ERROR:return data from disk\n");
//                        return -1;
//                }
//        }
//        return 1;
//}
int read_block(char *buffer, int block_0, int block_num) {
    if (block_0 + block_num > TOTAL_BLOCK) {
        fprintf(stderr, "Block read out of range\n");
        return -1;
    }

    for (int i = 0; i < block_num; ++i) {
        DiskRequest req;
        req.op = 'R';
        req.blockno = block_0 + i;
        memset(req.data, 0, MAX_BLOCKSIZE); // not strictly needed

        if (send(diskfd, &req, sizeof(req),0)<0) {
            perror("send read request failed");
            return -1;
        }
        memset(buffer,0,MAX_BLOCKSIZE);
        if (recv(diskfd, buffer, MAX_BLOCKSIZE, 0)<=0) {
            perror("receive read response failed");
            return -1;
        }
    }

    return 1;
}

void initial_superblock(){
        sb.magic=0xEF53;
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
        printf("initial_superblock is: %s",buffer);
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
