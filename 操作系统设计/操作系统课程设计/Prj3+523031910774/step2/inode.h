#ifndef INODEH
#define INODEH

#pragma pack(1)
#include"superblock.h"
#include <stdint.h>
#include <stdio.h>
#define NAME_MAX 26
#define inode_per_block 8
#define inode_stable_start_block 5 
#define inode_directblock_num 6
#define MAX_LINKS 134
#define ORPHAN 0XFFFFFFFF

typedef struct inode{
        uint8_t mode;  // 0:file 1:directory 

        uint8_t links; // the link count        
        uint16_t size; //file size         
        uint16_t blocks[inode_directblock_num];//--    
        uint16_t indirect;//--           
        uint32_t timestamps[2];//?
        uint32_t dad;
        uint16_t inode_offset;
}inode;//32 bytes
extern inode inode_table[TOTAL_INODE];

typedef struct direntry{//this is for the mkdir structure , of course ,it contain the inode root:"./home"
        uint32_t inode_i;
        uint8_t mode;
        uint8_t valid;
        char name[NAME_MAX];
}direntry;//32bytes

int initial_root_inode();
//this will initial the root inode
//the root inode has to be the dir type
//success :1   else:-1

int initial_inode(inode*node,uint8_t mode,uint16_t inode_offset,uint32_t dad);
//this will initial the inode
//include initialize the type and create time and something else
//success return 1

int allocate_inode();
//this will find an empty inode and return the inode index in the inode_table
//if cannot find return -1

int write_inode(inode*node,uint16_t node_index);
//write the inode into the actual block, it depends on the index which allocate_inode provide,and the inode which initialized
//return 1 if success return -1 if else

int add_in_dir(inode*node,uint8_t mode,const char*name);
//add file or directory into one directory
//success 1   fail -1


int ls_dir(inode*node,char*name_array);
//ls the file and directory of the current inode
//success 1 fail -1

int free_inode(inode*node);
//free the inode space and the correspongding blcok space, and refresh the superblock
//success 1 fail -1

int rm_out_dir(inode*node,const char*name);
//remove the file which holds the name from the directory. use free_inode function to help finish it
//success 1 fail -1

int isempty_dir(inode*node);
//check the dir inode is empty or not , to help the rmdir_out_dir process
//success 1 fail -1 not empty

int rmdir_out_dir(inode*node,const char*name);
//the same as rm_out_dir remove dir
//success 1 fail 0 none empty dir or other reason `

int read_f(inode*node,const char*name,char*content);
//find the file with the name in the current dirctory, store the content in the content pointer
//success 1 fail -1 not file, no such file, other reason

int write_f(inode*node,const char*name,char*content);
//write content to the file with the name
//success 1 fail -1 not file, no such file, other reason

int find_from_dir(inode*node,const char*name);
//find the file from the directory
//success: inode id in the inode_table   fail: -1


#endif
