#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include "inode.h"
#include "superblock.h"
inode inode_table[TOTAL_INODE];

int initial_root_inode(){
        inode_table[0].mode=1;
        inode_table[0].links=0;
        inode_table[0].size=0;
        inode_table[0].timestamps[0]=time(NULL);
        inode_table[0].dad=ORPHAN;
        inode_table[0].inode_offset=0;
        memset(inode_table[0].blocks,0,sizeof(inode_table[0].blocks));
        sb.inode_map[0] |= (1 << 31);
        sb.count_inode++;
        return 1;
}

int initial_inode(inode*node,uint8_t mode,uint16_t inode_offset,uint32_t dad){
        node->mode=mode;
        node->links=0;
        node->size=0;
        node->timestamps[0]=time(NULL);
        node->dad=dad;
        node->inode_offset=inode_offset;
        memset(inode_table[inode_offset].blocks,0,sizeof(inode_table[0].blocks));//when create a new inode, refresh the block[i]
        write_inode(node,inode_offset);
        return 1;
}
int allocate_inode(){
        if(!sb.count_inode_free)return -1;
        for(int i=0;i<NUM_INODE_MAP;i++){
                uint32_t space_inode=sb.inode_map[i];
                for(int j=0;j<32;j++){
                        if((space_inode>>(31-j)&1)==1)continue;//the inode space is already occupied
                        else{
                                space_inode=space_inode|(1<<(31-j));
                                sb.inode_map[i] = space_inode;//remember to write back
                                sb.count_inode_free--;
                                sb.count_inode++;
                                char buffer[5*MAX_BLOCKSIZE]={0};
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

int write_inode(inode*node,uint16_t node_index){
        int block_offset=inode_stable_start_block+node_index/inode_per_block;//find the actual block
        int inode_offset=sizeof(inode)*(node_index%inode_per_block);//the inode position of the block
        char buffer[MAX_BLOCKSIZE];
        if(read_block(buffer,block_offset,1)<0)return -1;//read block content , so we can change it later
        memcpy(buffer+inode_offset,node,sizeof(inode));
        if(write_block(buffer,block_offset,1)<0)return -1;
        return 1;
}

int add_in_dir(inode*node,uint8_t mode,const char*name){//the directory node is as an argument
        if(node->mode==0)
        {
                printf("mode\n");
                return -1;
        }
        direntry dirp[8];//store the dir type content of a block
        char buffer[MAX_BLOCKSIZE];
        for(int i=0;i<inode_directblock_num;i++){
                if(node->blocks[i]==0)continue;//we first satisfied the block which have already had some dirp;
                if(read_block(buffer,node->blocks[i],1)==-1){
                        printf("readblock\n");
                        return -1;
                }
                memcpy(&dirp,buffer,MAX_BLOCKSIZE);
                for(int j=0;j<8;j++){
                        if(dirp[j].valid==0){
                                int new_inode_id=allocate_inode();
                                if(new_inode_id==-1){
                                        printf("newinodeid\n");
                                        return -1;
                                }
                                initial_inode(&inode_table[new_inode_id],mode,new_inode_id,node->inode_offset);
                                dirp[j].inode_i=new_inode_id;
                                dirp[j].mode=mode;
                                dirp[j].valid=1;
                                strcpy(dirp[j].name,name);
                                memcpy(buffer,&dirp,MAX_BLOCKSIZE);
                                write_block(buffer,node->blocks[i],1);
                                write_inode(&inode_table[new_inode_id],new_inode_id);
                                node->timestamps[0]=time(NULL);
                                node->links++;
                                return 1;
                        }
                }
        }
        if(node->links<inode_directblock_num){//cannot find the unfilled block,need to allocate new block
                for(int i=0;i<inode_directblock_num;i++){
                        if(node->blocks[i]==0){
                                node->blocks[i]=block_allocate();
                                int new_inode_id=allocate_inode();
                                if(new_inode_id==-1)return -1;
                                initial_inode(&inode_table[new_inode_id],mode,new_inode_id,node->inode_offset);
                                dirp[0].inode_i=new_inode_id;
                                dirp[0].mode=mode;
                                dirp[0].valid=1;
                                strcpy(dirp[0].name,name);
                                memcpy(buffer,&dirp,MAX_BLOCKSIZE);
                                write_block(buffer,node->blocks[i],1);
                                write_inode(&inode_table[new_inode_id],new_inode_id);
                                node->links++;
                                node->timestamps[0]=time(NULL);
                                return 1;
                        }
                }
        }
        printf("there is no space to add file or folder\n");
        return -1;
}

//h----------------------------------------------------------------------------------------------------
int lexi(const void*a,const void*b){
        return strcmp((const char*)a,(const char*)b);
}
int ls_dir(inode*node,char*name_array){
        if(node->mode==0){
                printf("ERROR:not directory\n");
                return -1;
        }
        char file[64][NAME_MAX];
        char dir[64][NAME_MAX];
        int index1=0;
        int index2=0;
        direntry dirp[8];//store the dir type content of a block
        char buffer[MAX_BLOCKSIZE];
        for(int i=0;i<inode_directblock_num;i++){
                if(node->blocks[i]==0)continue;
                if(read_block(buffer,node->blocks[i],1)==-1){
                        printf("readblock\n");
                        return -1;
                }
                memcpy(&dirp,buffer,MAX_BLOCKSIZE);
                for(int j=0;j<8;j++){
                        if(dirp[j].valid==1){
                                if(dirp[j].mode==0){
                                        strcpy(file[index1],dirp[j].name);
                                        index1++;
                                }
                                if(dirp[j].mode==1){
                                        strcpy(dir[index2],dirp[j].name);
                                        index2++;
                                }
                        }
                }
        }
        qsort(dir, index2, sizeof(dir[0]), lexi);
        qsort(file, index1, sizeof(file[0]), lexi);
        name_array[0]='\0';
        for(int i=0;i<index1;i++){
                strcat(name_array,file[i]);
                strcat(name_array," ");
        }
        if(index2!=0){
                strcat(name_array,"&");
        }
        for(int i=0;i<index2;i++){
                strcat(name_array,dir[i]);
                strcat(name_array," ");
        }
        return 1;


}

int free_inode(inode*node){
        if(node->inode_offset==0)return -1;
        int map_index=node->inode_offset/32;
        int in_index=node->inode_offset%32;
        if(((sb.inode_map[map_index]>>(31- in_index))&1)==0)return 1;
        for(int i=0;i<inode_directblock_num;i++){
                if(node->blocks[i]==0)continue;
                block_free(node->blocks[i]);//refresh the block , but the inode needs to be refreshed by yourself
        }
        //if(node->indirect!=0){
        //}
        initial_inode(node,0,node->inode_offset,ORPHAN);
        sb.count_inode--;
        sb.count_inode_free++;
        sb.inode_map[map_index]&=(~(1U<<(31-in_index)));
        char buf_2[5*MAX_BLOCKSIZE];
        memset(buf_2, 0, sizeof(buf_2));
        memcpy(buf_2,&sb,sizeof(sb));
        if(write_block(buf_2,0,5)==-1)return -1;
        return 1;
}

int rm_out_dir(inode*node,const char*name){
        if(node->mode==0){
                printf("mode\n");
                return -1;
        }
        direntry dirp[8];//store the dir type content of a block
        char buffer[MAX_BLOCKSIZE];
        for(int i=0;i<inode_directblock_num;i++){
                if(node->blocks[i]==0)continue;
                if(read_block(buffer,node->blocks[i],1)==-1){
                        printf("readblock\n");
                        return -1;
                }
                memcpy(&dirp,buffer,MAX_BLOCKSIZE);
                for(int j=0;j<inode_per_block;j++){
                        if(dirp[j].valid==1){
                                if(strcmp(name,dirp[j].name)==0&&dirp[j].mode==0){
                                        free_inode(&inode_table[dirp[j].inode_i]);
                                        dirp[j].valid=0;//note:just set the dirp[j].valid , if the blocks is empty, it is still allocated some space, need to be processed
                                        memcpy(buffer,&dirp,MAX_BLOCKSIZE);
                                        write_block(buffer,node->blocks[i],1);
                                        write_inode(&inode_table[dirp[j].inode_i],dirp[j].inode_i);
                                        node->timestamps[0]=time(NULL);
                                        node->links--;
                                        return 1;
                                }
                        }
                }
        }
        return -1;
}

int isempty_dir(inode*node){
        if(node->mode==0)return 0;
        direntry dirp[8];//store the dir type content of a block
        char buffer[MAX_BLOCKSIZE];
        for(int i=0;i<inode_directblock_num;i++){
                if(node->blocks[i]==0)continue;
                if(read_block(buffer,node->blocks[i],1)==-1)return 0;
                memcpy(&dirp,buffer,MAX_BLOCKSIZE);
                for(int j=0;j<8;j++){
                        if(dirp[j].valid==1){
                                printf("ERROR:dir not empty\n");
                                return 0;
                        }
                }
                block_free(node->blocks[i]);
                node->links--;
                node->blocks[i]=0;//refresh the blocks by the way, if we delete file , we donot need execute this step, but dir need to refresh
        }
        return 1;

}

int rmdir_out_dir(inode*node,const char*name){
        if(node->mode==0){
                printf("mode\n");
                return -1;
        }
        direntry dirp[8];//store the dir type content of a block
        char buffer[MAX_BLOCKSIZE];
        for(int i=0;i<inode_directblock_num;i++){
                if(node->blocks[i]==0)continue;
                if(read_block(buffer,node->blocks[i],1)==-1){
                        printf("readblock\n");
                        return -1;
                }
                memcpy(&dirp,buffer,MAX_BLOCKSIZE);
                for(int j=0;j<inode_per_block;j++){
                        if(dirp[j].valid==1){
                                if(strcmp(name,dirp[j].name)==0&&dirp[j].mode==1){
                                        if(!isempty_dir(&inode_table[dirp[j].inode_i])){
                                                printf("ERROR:not empty\n");
                                                return -1;
                                        }
                                        free_inode(&inode_table[dirp[j].inode_i]);
                                        dirp[j].valid=0;
                                        memcpy(buffer,&dirp,MAX_BLOCKSIZE);
                                        write_block(buffer,node->blocks[i],1);
                                        write_inode(&inode_table[dirp[j].inode_i],dirp[j].inode_i);
                                        node->timestamps[0]=time(NULL);
                                        return 1;
                                }
                        }
                }
        }
        return -1;

}

int read_f(inode*node,const char*name,char*content){
        if(node->mode==0){
                printf("not a directory\n");
                return -1;
        }
        direntry dirp[8];//store the dir type content of a block
        char buffer[MAX_BLOCKSIZE];
        char buf_2[MAX_BLOCKSIZE];
        content[0]='\0';
        for(int i=0;i<inode_directblock_num;i++){//I think I should pack the search process , I am a fool
                if(node->blocks[i]==0)continue;
                if(read_block(buffer,node->blocks[i],1)==-1){
                        printf("readblock\n");
                        return -1;
                }
                memcpy(&dirp,buffer,MAX_BLOCKSIZE);
                for(int j=0;j<inode_per_block;j++){
                        if(dirp[j].valid==1){
                                if(strcmp(name,dirp[j].name)==0&&dirp[j].mode==0){//find the file
                                        inode id=inode_table[dirp[j].inode_i];
                                        for(int k=0;k<inode_directblock_num;k++){
                                                if(id.blocks[k]==0)continue;
                                                int block_id=id.blocks[k];
                                                read_block(buf_2,block_id,1);
                                                memcpy(content+k*MAX_BLOCKSIZE,buf_2,MAX_BLOCKSIZE);
                                        }
                                        return 1;
                                }
                        }
                }
        }
        return -1;

}

int write_f(inode*node,const char*name,char*content){
        if(node->mode==0){
                printf("not a directory\n");
                return -1;
        }
        direntry dirp[8];//store the dir type content of a block
        char buffer[MAX_BLOCKSIZE];
        int flag=1;
        inode id;
        int index;
        for(int i=0;i<inode_directblock_num&&flag;i++){//I think I should pack the search process , I am a fool
                if(node->blocks[i]==0)continue;
                if(read_block(buffer,node->blocks[i],1)==-1){
                        printf("readblock\n");
                        return -1;
                }
                memcpy(&dirp,buffer,MAX_BLOCKSIZE);
                for(int j=0;j<inode_per_block&&flag;j++){
                        if(dirp[j].valid==1){
                                if(strcmp(name,dirp[j].name)==0&&dirp[j].mode==0){//find the file
                                        index=dirp[j].inode_i;
                                        id=inode_table[index];
                                        flag=0;
                                        break;
                                }
                        }
                }
        }
        if(flag){
                printf("cannot find the file\n");
                return -1;
        }
        int block_should=((strlen(content)+1)+MAX_BLOCKSIZE-1)/MAX_BLOCKSIZE;//this will get interger upper,if it is times of max,then keep still`
        char store[strlen(content)+1];//do not set it too large, if too large ,the stack may be overflowing.
        memcpy(store,content,strlen(content)+1);
        int first=(block_should>6?6:block_should);
        uint16_t t_indirect[128];
        uint8_t links=id.links;
        int indirect_id=0;//this will store the indirect block id;
        if(block_should-int(links)>int(sb.count_block_free)){
                printf("no free block\n");
                return -1;
        }
        if(block_should>int(links)){//the last file did not have enough space for the new file
                for(int i=links;i<first;i++){
                        //printf("%d\n",links);
                        //printf("%d\n",block_should);   just for debug
                        int new_block=block_allocate();
                        if(new_block==-1){
                                printf("no blocks\n");
                                return -1;
                        }
                        id.blocks[i]=new_block;
                }
                if(links>6){
                        memset(buffer,0,sizeof(buffer));
                        read_block(buffer,id.indirect,1);
                        memcpy(&t_indirect,buffer,MAX_BLOCKSIZE);//this will save the previous content, so we can find the history
                }
                else{
                        if(block_should>6){
                                indirect_id=block_allocate();//this will allocate block for the indirect inode
                                if(indirect_id==-1)return -1;
                                id.indirect=indirect_id;
                        }
                }
        }
        else{//free the redundant block left by last file
                if(links>6){//this can handle two situation: links>6,block_s>6   ;  link>6,block_s<=6
                        int door=(block_should>6?block_should:6);
                        memset(buffer,0,sizeof(buffer));
                        if(read_block(buffer,id.indirect,1)==-1)return -1;
                        memcpy(&t_indirect,buffer,MAX_BLOCKSIZE);
                        for(int i=door-6;i<links-6;i++){
                                block_free(t_indirect[i]);
                        }
                        if(block_should<=6){
                                id.indirect=0;
                        }
                }
                else{
                        for(int i=block_should;i<links;i++){
                                block_free(id.blocks[i]);
                        }
                }
        }
        memset(buffer,0,sizeof(buffer));
        for(int i=0;i<first;i++){
                memcpy(buffer,store+i*MAX_BLOCKSIZE,MAX_BLOCKSIZE);
                write_block(buffer,id.blocks[i],1);
        }
        if(id.indirect!=0){
                for(int i=0;i<block_should-6;i++){
                        memcpy(buffer,store+(i+6)*MAX_BLOCKSIZE,MAX_BLOCKSIZE);
                        write_block(buffer,t_indirect[i],1);
                }
        }
        id.links=block_should;
        id.size=strlen(content);
        id.timestamps[0]=time(NULL);
        inode_table[index]=id;
        write_inode(&inode_table[index],index);
        return 1;
}

int find_from_dir(inode*node,const char*name){
        if(node->mode==0){
                printf("not a directory\n");
                return -1;
        }
        direntry dirp[8];//store the dir type content of a block
        char buffer[MAX_BLOCKSIZE];
        for(int i=0;i<inode_directblock_num;i++){//I think I should pack the search process , I am a fool
                if(node->blocks[i]==0)continue;
                if(read_block(buffer,node->blocks[i],1)==-1){
                        printf("readblock\n");
                        return -1;
                }
                memcpy(&dirp,buffer,MAX_BLOCKSIZE);
                for(int j=0;j<inode_per_block;j++){
                        if(dirp[j].valid==1){
                                if(strcmp(name,dirp[j].name)==0){
                                        return dirp[j].inode_i;
                                }
                        }
                }
        }
        return -1;

}
