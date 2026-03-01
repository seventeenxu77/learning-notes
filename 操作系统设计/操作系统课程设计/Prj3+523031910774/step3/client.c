#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<sstream>
#include<unistd.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<arpa/inet.h>

int main(int argc, char *argv[]) {
        if (argc != 2) {
                printf("ERROR:command wrong: only one parameter for port is needed\n");
                return 1;
        }
        int port = atoi(argv[1]);
        // create socket
        int clientfd = socket(AF_INET, SOCK_STREAM, 0);
        if(-1 == clientfd) {
                printf("create socket error");
                return -1;
        }

        // connect server 
        struct sockaddr_in serveraddr;
        serveraddr.sin_family = AF_INET;
        serveraddr.sin_addr.s_addr = INADDR_ANY;
        serveraddr.sin_port = htons(port);

        if(-1 == connect(clientfd, (struct sockaddr *)&serveraddr, sizeof(serveraddr))) {
                printf("connect error");
                return -1;
        }
        printf("succecc connect\n");
        char recvbuf[3072];
        char command[3072];
        memset(recvbuf,0,sizeof(recvbuf));
        memset(command,0,sizeof(command));
        while(1){
                fgets(command, sizeof(command), stdin);
                if(send(clientfd, command, strlen(command), 0)<0){
                        printf("ERROR:send data\n");
                        return 1;
                }
                int ret = recv(clientfd, recvbuf, sizeof(recvbuf), 0);
                if (ret <= 0) {
                        perror("ERROR: receive data\n");
                        return 1;
                }
                printf("%s", recvbuf);
                if (command[0]=='e') break;
        }

        // close socket
        close(clientfd);

    return 0;
}
