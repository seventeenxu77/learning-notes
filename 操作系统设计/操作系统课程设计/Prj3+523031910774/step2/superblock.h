#ifndef SUPERBLOCKH
#define SUPERBLOCKH

#include <stdint.h>
#include <stdio.h>

#define MAX_BLOCKSIZE 256
#define NUM_INODE_MAP 32
#define NUM_BLOCK_MAP 256   //bytes
#define TOTAL_INODE 1024    //32*32=1024
#define TOTAL_BLOCK 8192    //32*256=8192
#define SYS_BLOCK 133       //5+32*32*32/256=133 blocks

//---define diskfileS
extern char diskfile[TOTAL_BLOCK][MAX_BLOCKSIZE];//form the diskfile by 2-dimmension array
int write_block(char*buffer,int block_0,int block_num);
//---this will write block from the buffer into the diskfile
//---if sucucess , return 1
//---if not, return -1
int read_block(char*buffer,int block_0,int block_num);
//---this will read block from the diskfile into the buffer
//---if sucucess , return 1
//---if not, return -1








//---define superblock
typedef struct{
        uint32_t count_inode;//total inode
        uint32_t count_block;//total block
        uint32_t count_inode_free;//free inode
        uint32_t count_block_free;//free block
        uint32_t inode_map[NUM_INODE_MAP];//the inode bitmap
        uint32_t block_map[NUM_BLOCK_MAP];//the block bitmap
        uint32_t root_inode;
}superblocktype;
extern superblocktype sb;
//total space cost:4*5+4*32+4*256=1172 bytes,so we should have 5 blocks
void initial_superblock();
//---this will initialize the superblock
int block_allocate();
//---this will find the empty block
//---if sucucess , return the number of the target block
//---if not, return -1 to inform system, there is no empty block
int block_free(uint32_t block_number);
//---this will free the target block
//---if sucucess, return 1 
//---if the target block is empty, return 0
//---if fail, return -1


#endif
