// a shell-like program that illustrates how Linux spawns processes. It
// should handle the commands with arguments and the commands connected by
// pips. Server program is needed to return command result to client request.
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<sstream>
#include<unistd.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<sys/wait.h>
#include<netinet/in.h>
#include<arpa/inet.h>
int parseLine(char*line,char*command_array[]){
        char*p;
        int count=0;
        p=strtok(line," ");
        while(p&&strcmp(p,"|")!=0){
                command_array[count]=p;
                count++;
                p=strtok(NULL," ");
        }
        command_array[count]=NULL;
        return count;
}
int main(int argc,char*argv[]){
        int BASIC_SERVER_PORT=atoi(argv[1]);//here 1 or 0
        int sockfd;
        sockfd=socket(AF_INET,SOCK_STREAM,0);
        if(sockfd<0){
                perror("ERROR:opening socket");
                exit(2);
        }
        struct sockaddr_in serv_addr;
        serv_addr.sin_family=AF_INET;
        serv_addr.sin_addr.s_addr=htonl(INADDR_ANY);
        serv_addr.sin_port=htons(BASIC_SERVER_PORT);
        if(bind(sockfd,(sockaddr*)&serv_addr,sizeof(serv_addr))==-1){
        perror("ERROR:binding\n");
        close(sockfd);
        exit(2);
        }
        if(listen(sockfd,5)==-1){
                perror("ERROR:listening\n");
                close(sockfd);
                exit(2);
        }
        printf("Accepting connections......\n");//here must have '\n',unless it cannot be printed out
        int client_sockfd;
        struct sockaddr_in client_addr;
        socklen_t len=sizeof(client_addr);
        char buffer[1024];
        int status;
        char*command_array[1024];
        while(1){
        client_sockfd=accept(sockfd,(sockaddr*)&client_addr,&len);
        if(client_sockfd==-1){
        perror("ERROR:accepting\n");
        close(sockfd);
        exit(2);
        }
        pid_t pid=fork();
        if(pid<0){
                printf("ERROR:forking\n");
        }
        if(pid==0){
        while(1){
        int readn=read(client_sockfd,buffer,1024);
        if(buffer[readn-1]=='\n'||buffer[readn-2]=='\r'){
        buffer[readn-1]='\0';
        buffer[readn-2]='\0';
        }
        buffer[readn]='\0';
        if(strcmp(buffer,"exit")==0){
                shutdown(client_sockfd,SHUT_RDWR);
                printf("success:close client connection from ip: %s port: %d\n",inet_ntoa(client_addr.sin_addr),ntohs(client_addr.sin_port));
                exit(0);
        }
        printf("received command from ip:%s port:%d :%s\n",inet_ntoa(client_addr.sin_addr),ntohs(client_addr.sin_port),buffer);
        char*line;
        char buffer_temp[1024];
        int total=0;
        strcpy(buffer_temp,buffer);
        line=buffer_temp;
        while(line!=NULL){
                parseLine(line,command_array);
                line=strtok(NULL,"");
                total++;
        }
        total-=1;
        int count=0;
        line=buffer;
        int mypip[total][2];
        for(int i=0;i<total;i++){
                if(pipe(mypip[i])==-1){
                        printf("ERROR:piping\n");
                        exit(2);
                }
        }
        while(line!=NULL){
                parseLine(line,command_array);
                line=strtok(NULL,"");//this has to be none string
                count++;
        pid_t pid_third=fork();
        if(pid_third>0){//cannot close father pip in advance,else pip cannot be used,if do not close it ,the pip is blocked untill exit
            if(count>1){
                    close(mypip[count-2][0]);
                    close(mypip[count-2][1]);//close father pip
            }
    }
    if(pid_third<0){
            printf("ERROR:forking_sec\n");
            exit(2);
    }
    if(pid_third==0){
            if(line==NULL){
                    close(mypip[count-2][1]);
                    close(0);
                    dup2(mypip[count-2][0],STDIN_FILENO);
                    dup2(client_sockfd,STDOUT_FILENO);
                    close(mypip[count-2][0]);
            }
            else{
            if(count==1){
                    close(mypip[count-1][0]);
                    close(1);
                    dup2(mypip[count-1][1],STDOUT_FILENO);
                    close(mypip[count-1][1]);
            }
            else{
                    close(mypip[count-2][1]);
            close(0);
            dup2(mypip[count-2][0],STDIN_FILENO);
            close(1);
            close(mypip[count-1][0]);
            dup2(mypip[count-1][1],STDOUT_FILENO);
            close(mypip[count-2][0]);
            close(mypip[count-1][1]);//close pip timely,in case of pip blocking
            }
            }
    if(execvp(command_array[0],command_array)==-1){
            printf("ERROR:running command:'%s'\n",buffer);
            exit(0);
    }
    }
    }
    }
    }
    }
    return 0;
}
