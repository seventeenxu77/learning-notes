#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <string>
#include <fcntl.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<arpa/inet.h>

#include "inode1.h"
#define CMD_BUFFERSIZE 3072
int now_dir=0;
int diskfd;
int fsfd;
int clientfd;
char back[CMD_BUFFERSIZE];
int f_flag;
//char*command_array[]=
//{
//      "f",
//      "mk",
//      "mkdir",
//      "rm",
//      "cd",
//      "rmdir",
//      "ls",
//      "cat",
//      "w",
//      "i",
//      "d",
//      "e"
//};
int comp_char(const char* str1, const char* str2, size_t n) {
    return strncmp(str1, str2, n) == 0;
}
void load_buf(const char* tail){
    strcat(back, tail);
}

bool is_valid_name(char* name){
        int len=strlen(name);
        if(len>NAME_MAX){
                printf("too long name, the max name length is: 26\n");
                load_buf("too long name, the max name length is: 26\n");
                return 0;
        }
        int i=0;
        while(i<len){
                char c=name[i];
                if(c=='/'||c==' '){
                        printf("incorrct char: '/' and ' ',please check your filename\n");
                        load_buf("incorrct char: '/' and ' ',please check your filename\n");
                        return 0;
                }
                i++;
        }
        return 1;
}

int read_inode(inode* node, uint16_t node_index){
        int block_offset=inode_stable_start_block+node_index/inode_per_block;//find the actual block
        int inode_offset=sizeof(inode)*(node_index%inode_per_block);//the inode position of the block
        char buffer[MAX_BLOCKSIZE];
        if(read_block(buffer,block_offset,1)<0)return -1;//read block content , so we can change it later
        memcpy(node, &buffer[inode_offset], sizeof(inode));
        return 1;
}
int pre_process(){
    char buf[5*MAX_BLOCKSIZE];
    memset(buf, 0, sizeof(buf));
    for(int i=0; i<5; i++){
        if (read_block(&buf[i*MAX_BLOCKSIZE],i,1) < 0) {
        return -1;
        }
    }
    memcpy(&sb, buf, sizeof(superblocktype));
    return 1;
}
void debug(){
        printf("now dir id:%d\n",now_dir);
        printf("now dir links:%d\n",inode_table[now_dir].links);
        direntry dirp[8];//store the dir type content of a block
        char buffer[MAX_BLOCKSIZE];
        for(int i=0;i<inode_directblock_num;i++){//I think I should pack the search process , I am a fool
                if(inode_table[now_dir].blocks[i]==0)continue;
                read_block(buffer,inode_table[now_dir].blocks[i],1);
                memcpy(&dirp,buffer,MAX_BLOCKSIZE);
                for(int j=0;j<inode_per_block;j++){
                        if(dirp[j].valid==1&&dirp[j].mode==0){
                                        printf("the file under dir: %s  id:%d\n",dirp[j].name,dirp[j].inode_i);
                        }
                        if(dirp[j].valid==1&&dirp[j].mode==1){
                                        printf("the folder under dir: %s   id:%d\n",dirp[j].name,dirp[j].inode_i);
                        }

                }
        }
}
int f_func(){
        //printf("inode size: %lu\n", sizeof(inode));
        if(f_flag==1){
                load_buf("already format, please do not format again\n");
                return 1;
        }
        initial_superblock();
        if(initial_root_inode()==-1)return -1;
        for(int i=1;i<TOTAL_INODE;i++){//do not intial root_inode
                initial_inode(&inode_table[i],0,i,ORPHAN);
        }
        for(int i=0;i<TOTAL_INODE;i++){
                if(write_inode(&inode_table[i],i)==-1)return -1;
        }
        f_flag=1;
        load_buf("Done\n");
        return 1;
}
int w_func(char*cmd){
        if(!f_flag){
                printf("you have not format the file system, please use command: f\n");
                load_buf("you have not format the file system, please use command: f\n");
                return 1;
        }
        char*tmp=cmd+2;
        int length;
        char content[MAX_LINKS*MAX_BLOCKSIZE];
        char name[NAME_MAX];
        sscanf(tmp, "%s %d %[^\n]", name, &length, content);//%d is a pointer
        if(is_valid_name(name)==0){
                return 1;
        }
        if(write_f(&inode_table[now_dir],name,content)==-1){
                printf("wrong\n");
                load_buf("No\n");
                return -1;
        }
        load_buf("Yes\n");
        return 1;
}
int i_func(char*cmd){
        if(!f_flag){
                printf("you have not format the file system, please use command: f\n");
                load_buf("you have not format the file system, please use command: f\n");
                return 1;
        }
        char*tmp=cmd+2;
        char name[NAME_MAX];
        char buffer[MAX_LINKS*MAX_BLOCKSIZE];
        int pos;
        int length;
        char content[MAX_LINKS*MAX_BLOCKSIZE];
        sscanf(tmp, "%s %d %d %[^\n]", name, &pos, &length, content);
        if(is_valid_name(name)==0){
                return 1;
        }
        int inode_id=find_from_dir(&inode_table[now_dir],name);
        if(inode_id==-1){
                printf("do not find the file\n");
                return -1;
        }
        int old_size=inode_table[inode_id].size;
        if(pos>old_size)pos=old_size;
        if(read_f(&inode_table[now_dir],name,buffer)==-1)return -1;
         memmove(buffer + pos + length, buffer + pos, old_size - pos);
         memcpy(buffer+pos,content,length);
         buffer[length+old_size]='\0';
         if(write_f(&inode_table[now_dir],name,buffer)==-1){
                 load_buf("No\n");
                 return -1;
         }
         load_buf("Yes\n");
         return 1;
}
int d_func(char*cmd){
        if(!f_flag){
                printf("you have not format the file system, please use command: f\n");
                load_buf("you have not format the file system, please use command: f\n");
                return 1;
        }
        char*tmp=cmd+2;
        char name[NAME_MAX];
        char buffer[MAX_LINKS*MAX_BLOCKSIZE];
        int pos;
        int length;
        sscanf(tmp, "%s %d %d", name, &pos, &length);
        if(is_valid_name(name)==0){
                return 1;
        }
        int inode_id=find_from_dir(&inode_table[now_dir],name);
        if(inode_id==-1){
                printf("do not find the file\n");
                return -1;
        }
        int old_size=inode_table[inode_id].size;
        if(pos>old_size)pos=old_size;
        if (pos + length > old_size)length = old_size - pos;
        if(read_f(&inode_table[now_dir],name,buffer)==-1)return -1;
        memmove(buffer+pos,buffer+pos+length,old_size-pos-length);
         buffer[old_size-length]='\0';
         if(write_f(&inode_table[now_dir],name,buffer)==-1){
                 load_buf("No\n");
                 return -1;
         }
         load_buf("No\n");
         return 1;
}

int e_func(){
        load_buf("Goodbye!!!\n");
        return -1;
}
int mk_func(char* name){
        if(!f_flag){
                printf("you have not format the file system, please use command: f\n");
                load_buf("you have not format the file system, please use command: f\n");
                return 1;
        }
        if(!is_valid_name(name)){
                return 1;
        }
        if(add_in_dir(&inode_table[now_dir],0,name)==-1){
                printf("fail to execute commmand\n");
                load_buf("No");
                return -1;
        }
        printf("success to execute commmand,mk: %s\n",name);
        load_buf("Yes\n");

        return 1;
}
int rm_func(char* name){
        if(!f_flag){
                printf("you have not format the file system, please use command: f\n");
                load_buf("you have not format the file system, please use command: f\n");
                return 1;
        }
        if(is_valid_name(name)==0){
                return 1;
        }
        if(rm_out_dir(&inode_table[now_dir],name)==-1){
                load_buf("No\n");
                return -1;
        }
        load_buf("Yes\n");
        return 1;
}
int cd_func(char*path){
        if(!f_flag){
                printf("you have not format the file system, please use command: f\n");
                load_buf("you have not format the file system, please use command: f\n");
                return 1;
        }
        int store=now_dir;
        char path_copy[CMD_BUFFERSIZE];
        strncpy(path_copy, path, sizeof(path_copy));
        path_copy[sizeof(path_copy) - 1] = '\0';
        char* tmp = strtok(path_copy, "/");
        while(tmp!=NULL){
                if(strcmp(tmp,"..")==0){
                        if(inode_table[now_dir].dad==ORPHAN){
                                printf("ERROR:this is root directory or it is an orphan\n");
                                now_dir=store;
                                return -1;
                        }
                        now_dir=inode_table[now_dir].dad;
                }
                else if(strcmp(tmp,".")==0);
                else{
                        if(inode_table[now_dir].mode==0){
                                printf("ERROR:this is not a directory\n");
                                now_dir=store;
                                return -1;
                        }
                        int result=find_from_dir(&inode_table[now_dir],tmp);
                        if(result==-1){
                                printf("ERROR:can not find the name\n");
                                now_dir=store;
                                return -1;
                        }
                        if(inode_table[result].mode==0){
                                printf("ERROR:this is a file, cannot use cd command\n");
                                now_dir=store;
                                return -1;
                        }
                        now_dir=result;
                }
                tmp=strtok(NULL,"/");
        }
        return 1;
}
int ls_func(){
        if(!f_flag){
                printf("you have not format the file system, please use command: f\n");
                load_buf("you have not format the file system, please use command: f\n");
                return 1;
        }
        char name[64*NAME_MAX];
        ls_dir(&inode_table[now_dir],name);
        load_buf(name);
        load_buf("\n");
        printf("%s\n",name);
        return 1;

}
int cat_func(char*name){
        if(!f_flag){
                printf("you have not format the file system, please use command: f\n");
                load_buf("you have not format the file system, please use command: f\n");
                return 1;
        }
        if(is_valid_name(name)==0){
                return 1;
        }
        char content[1536];//256*6
        if(read_f(&inode_table[now_dir],name,content)==-1){
                printf("fail to execute commmand\n");
                return -1;
        }
        load_buf(content);
        load_buf("\n");
        printf("%s\n",content);
        return 1;
}
int mkdir_func(char*name){
        if(!f_flag){
                printf("you have not format the file system, please use command: f\n");
                load_buf("you have not format the file system, please use command: f\n");
                return 1;
        }
        if(is_valid_name(name)==0){
                return 1;
        }
        if(add_in_dir(&inode_table[now_dir],1,name)==-1){
                printf("fail to execute commmand\n");
                load_buf("No\n");
                return -1;
        }
        printf("success to execute commmand\n");
        load_buf("Yes\n");

        return 1;

}
int rmdir_func(char* name){
        if(!f_flag){
                printf("you have not format the file system, please use command: f\n");
                load_buf("you have not format the file system, please use command: f\n");
                return 1;
        }
        if(is_valid_name(name)==0){
                return 1;
        }
        if(rmdir_out_dir(&inode_table[now_dir],name)==-1){
                load_buf("No\n");
                return -1;
        }
        load_buf("Yes\n");
        return 1;
}

int match_command(char* cmd){
        if(comp_char(cmd,"f",1)){
                return f_func();
        }
        if(comp_char(cmd,"w ",2))return w_func(cmd);
        if(comp_char(cmd,"i ",2))return i_func(cmd);
        if(comp_char(cmd,"d ",2))return d_func(cmd);
        if(comp_char(cmd,"e",1))return e_func();
        if(comp_char(cmd,"mk ",3))return mk_func(cmd+3);
        if(comp_char(cmd,"rm ",3))return rm_func(cmd+3);
        if(comp_char(cmd,"cd ",3))return cd_func(cmd+3);
        if(comp_char(cmd,"ls",2))return ls_func();
        if(comp_char(cmd,"cat ",4))return cat_func(cmd+4);
        if(comp_char(cmd,"mkdir ",6))return mkdir_func(cmd+6);
        if(comp_char(cmd,"rmdir ",6))return rmdir_func(cmd+6);
        if(comp_char(cmd,"debug",5))debug();
        return 1;
}
int process_client(){
        char cmd[CMD_BUFFERSIZE];

        int status;
        if(pre_process()==1){
                if(sb.magic==0xEF53){
                        for (int i = 0; i < TOTAL_INODE; i++){
                                if (read_inode(&inode_table[i], i)<0) {
                                        break;
                                }
                        }
                        f_flag=1;
                }
        }
        while (1) {
                memset(cmd,0,sizeof(cmd));
                memset(back,0,sizeof(back));
                back[0]='\0';
                //for (int i = 0; i < TOTAL_INODE; i++){
                //if (read_inode(&inode_table[i], i)<0) {
                //        printf("can not load inode into the fs\n");
                //        break;
                //    }
                //}load_process
                if(recv(clientfd, cmd, sizeof(cmd), 0)<=0)break;
                cmd[strcspn(cmd, "\n")] = '\0';//remove the n singnal
                status=match_command(cmd);
                if(status==-1)
                {
                        break;
                }
                if (send(clientfd, back, sizeof(back), 0) < 0) {
                        perror("ERROR:return data to client\n");
                }
        }
        return 1;
}
int main(int argc,char*argv[]){
        if (argc != 3) {
        printf("ERROR:command wrong: only one parameter for port is needed\n");
        return 1;
        }
        f_flag=0;
        int disk_port = atoi(argv[1]);
        int fs_port = atoi(argv[2]);
        back[0]='\n';
        //connet to the disk server
        diskfd=socket(AF_INET,SOCK_STREAM,0);
        if(diskfd<0){
                perror("ERROR:opening socket\n");
                exit(2);
        }
        struct sockaddr_in disk_serv_addr;
        disk_serv_addr.sin_family=AF_INET;
        disk_serv_addr.sin_addr.s_addr=htonl(INADDR_ANY);
        disk_serv_addr.sin_port=htons(disk_port);
        if(-1 == connect(diskfd, (struct sockaddr *)&disk_serv_addr, sizeof(disk_serv_addr))) {
                printf("connect error: fs to disk\n");
                return -1;
        }
        printf("succecc connect disk server\n");
        //set up fs server
        struct sockaddr_in fs_serv_addr,client_addr;
        fsfd=socket(AF_INET,SOCK_STREAM,0);
        if(fsfd<0){
                perror("ERROR:opening socket\n");
                exit(2);
        }
        fs_serv_addr.sin_family=AF_INET;
        fs_serv_addr.sin_addr.s_addr=htonl(INADDR_ANY);
        fs_serv_addr.sin_port=htons(fs_port);
        if(bind(fsfd,(sockaddr*)&fs_serv_addr,sizeof(fs_serv_addr))==-1){
        perror("ERROR:binding\n");
        close(fsfd);
        exit(2);
        }
        if(listen(fsfd,5)==-1){
                perror("ERROR:listening\n");
                close(fsfd);
                exit(2);
        }
        printf("Accepting connections......\n");//here must have '\n',unless it cannot be printed out






        while (1) {
                socklen_t len=sizeof(client_addr);
                clientfd=accept(fsfd,(sockaddr*)&client_addr,&len);//here accept first parameter is the server itself
                if(clientfd==-1){
                        perror("ERROR:accepting\n");
                        close(clientfd);
                        continue;
                }
                printf("client connected, client socket: %d\n", clientfd);
                process_client();
                close(clientfd);
        }
        close(fsfd);

}
