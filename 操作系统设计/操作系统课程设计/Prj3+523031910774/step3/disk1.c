#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/mman.h>
#include <fcntl.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<arpa/inet.h>

#define SECTOR_SIZE 256
#define CMD_BUFFERSIZE 1024
int present;//to record the distance of two cylinders
int diskfd;
int clientfd;
typedef struct{
        char* filename;
        int cylinders;
        int sector_per_cylinder;
        int fd;
        double track_to_track_delay;
        FILE*log_fp;
        char*diskfile;

} disktype;
disktype disk;

// 客户端向磁盘发送的请求
typedef struct {
    char op;               // 'W' 或 'R'
    int blockno;      // 要读写的块号（注意字节序）
    char data[SECTOR_SIZE]; // 写入时使用，读取时可以为空
} __attribute__((packed)) DiskRequest;




int I_function(){
        fprintf(disk.log_fp, "%d %d\n", disk.cylinders, disk.sector_per_cylinder);
        return 1;
}
int R_function(int c,int s,char*buf){
        if(c<0||s<0||c>=disk.cylinders||s>=disk.sector_per_cylinder){//read range error
                printf("Instruction error!:cyliner:%d  sector:%d\n",c,s);
                fprintf(disk.log_fp, "No\n");

                return 1;
        }
        if(present==-1){
                present=c;
        }
        else{
                int delta=c-present>=0?c-present:present-c;
                present=c;
                usleep(delta*disk.track_to_track_delay);
                //printf("track movement cost %f millsecond time\n",delta*disk.track_to_track_delay);
        }
        char*readpointer=disk.diskfile+(c*disk.sector_per_cylinder+s)*SECTOR_SIZE;
        fprintf(disk.log_fp, "Yes ");
        memcpy(buf,readpointer,SECTOR_SIZE);
        fprintf(disk.log_fp, "\n");
        return 1;

}
int W_function(int c,int s,char*data){
        if(c<0||s<0||c>=disk.cylinders||s>=disk.sector_per_cylinder){//read range error
                printf("Instruction error :cyliner:%d  sector:%d\n",c,s);
                fprintf(disk.log_fp, "No\n");
                return 1;
        }
        if(present==-1){
                present=c;
        }
        else{
                int delta=c-present>=0?c-present:present-c;
                present=c;
                usleep(delta*disk.track_to_track_delay);
                //printf("track movement cost %f millsecond time\n",delta*disk.track_to_track_delay);
        }

        char*writepointer=disk.diskfile+(c*disk.sector_per_cylinder+s)*SECTOR_SIZE;
        memcpy(writepointer,data, SECTOR_SIZE);
        fprintf(disk.log_fp, "Yes\n");
        return 1;
}
int E_function(){
        fprintf(disk.log_fp, "Goodbye!\n");
        fclose(disk.log_fp);
        msync(disk.diskfile, disk.cylinders * disk.sector_per_cylinder * SECTOR_SIZE, MS_SYNC);
        munmap(disk.diskfile, disk.cylinders * disk.sector_per_cylinder * SECTOR_SIZE);
        close(disk.fd);
        free(disk.filename);
        return -1;
}
void initialize(int cylinders,int sector_per_cylinder,double track_to_track_delay,char*filename){//you have to use * instead of &,because it is c not c++
        present=-1;//initialize the two records,-1 refers to this is the first cylinder
        disk.filename=strdup(filename);//use strdup function to avoid mannually allocate space for file, but we should free it by ourselves.
        disk.cylinders=cylinders;
        disk.sector_per_cylinder=sector_per_cylinder;
        disk.track_to_track_delay=track_to_track_delay;
        disk.log_fp = fopen("disk.log", "w");
        disk.fd = open(filename, O_RDWR | O_CREAT | O_TRUNC, 0644);//master has the right to write or read,other onlu read
        if (disk.fd < 0) {
                printf("Error: Could not open file '%s'.\n", filename);
                exit(-1);
        }
        long FILESIZE = cylinders*sector_per_cylinder*SECTOR_SIZE;
        int result = lseek (disk.fd, FILESIZE-1, SEEK_SET);
        if (result == -1) {
                perror ("Error calling lseek() to 'stretch' the file\n");
                close (disk.fd);
                exit(-1);
        }
        result = write (disk.fd, "", 1);
        if (result != 1) {
                perror("Error writing last byte of the file\n");
                close(disk.fd);
                exit(-1);
        }
        disk.diskfile= (char *)mmap(NULL, FILESIZE,PROT_READ | PROT_WRITE,MAP_SHARED, disk.fd, 0);
        if (disk.diskfile== MAP_FAILED){
                close(disk.fd);
                printf("Error: Could not map file.\n");
                exit(-1);
        }
}
//int process_client(){
//       char cmd[CMD_BUFFERSIZE];
//      char new_cmd[CMD_BUFFERSIZE];
//       int status=1;
//      char type[5];
//      char buffer[SECTOR_SIZE];
//      int num;
//        while (1) {
//              memset(cmd,0,sizeof(cmd));
//                memset(back,0,sizeof(back));
//              memset(buffer,0,sizeof(buffer));
//              memset(new_cmd,0,sizeof(new_cmd));
//              memset(type,0,sizeof(type));
//              memset(back,0,sizeof(back));
//              back[0]='\0';
//                if(recv(clientfd, cmd, sizeof(cmd), 0)<=0)break;
//                cmd[strcspn(cmd, "\n")] = '\0';//remove the n singnal
//              if(cmd[0]=='W'){
//                      sscanf(cmd, "%s %d %[^\n]", type, &num, buffer);
//                              printf("the cmd is:%s\n",cmd);
//                              printf("the data is:%s\n",buffer);
//                              int cylinder=num/disk.sector_per_cylinder;
//                              int sector=num%disk.sector_per_cylinder;
//                              sprintf(new_cmd, "%s %d %d %s", type, cylinder, sector, buffer);
//                      status=parse_command(new_cmd);
//                      if(status==-1){
//                              break;
//                      }
//                      if (send(clientfd, back, sizeof(back), 0) < 0) {
//                              perror("ERROR:return data to client\n");
//                      }
//              }
//              if(cmd[0]=='R'){
//                        if (sscanf(cmd, "%s %d", type, &num) == 2) {
//                              printf("%s\n",cmd);
//                                int cylinder=num/disk.sector_per_cylinder;
//                                int sector=num%disk.sector_per_cylinder;
//                                sprintf(new_cmd, "%s %d %d", type, cylinder, sector);
//                        }
//                        else {
//                                printf("ERROR:process original cmd\n");
//                       }
//                        status=parse_command(new_cmd);
//                        if(status==-1){
//                                break;
//                        }
//                      printf("disk find data:%s\n",back);
//                        if (send(clientfd, back, sizeof(back), 0) < 0) {
//                                perror("ERROR:return data to client\n");
//                        }
//                }
//
//        }
//        return 1;
//}
int process_client() {
    DiskRequest cmd;
    int status = 1;

    while (1) {
        memset(&cmd, 0, sizeof(cmd));
        char tmpbuf[SECTOR_SIZE];
        ssize_t recv_size = recv(clientfd, &cmd, sizeof(DiskRequest), 0);
        printf("%d\n",cmd.blockno);
        if (recv_size <= 0) break;
        int cylinder = int(cmd.blockno) / disk.sector_per_cylinder;
        int sector   = int(cmd.blockno) % disk.sector_per_cylinder;

        switch (cmd.op) {
            case 'R':
                status = R_function(cylinder, sector,tmpbuf);
                break;
            case 'W':
                status = W_function(cylinder, sector, cmd.data);
                break;
            case 'I':
                status = I_function();
                break;
            case 'E':
                status = E_function();
                break;
            default:
                fprintf(disk.log_fp, "Unknown command: %c\n", cmd.op);
                break;
        }
        if (status == -1) break;

        if (send(clientfd, tmpbuf, SECTOR_SIZE, 0) < 0) {
            perror("ERROR: sending response to client");
        }
    }

    return 1;
}

int main(int argc, char *argv[]){
        if (argc != 6)
        {
                printf("Error Usage: %s <cylinders> <sector per cylinder> <track-to-track delay> <disk-storage-filename>\n", argv[0]);
                return 1;
        }
        int cylinders=atoi(argv[1]);
        int sector_per_cylinder=atoi(argv[2]);
        char*p;
        double track_to_track_delay = strtod(argv[3], &p);
        char*filename=argv[4];
        int disk_port = atoi(argv[5]);
        initialize(cylinders,sector_per_cylinder,track_to_track_delay,filename);
        //connect the fs
        struct sockaddr_in disk_serv_addr,client_addr;
        diskfd=socket(AF_INET,SOCK_STREAM,0);
        if(diskfd<0){
                perror("ERROR:opening socket\n");
                exit(2);
        }
        disk_serv_addr.sin_family=AF_INET;
        disk_serv_addr.sin_addr.s_addr=htonl(INADDR_ANY);
        disk_serv_addr.sin_port=htons(disk_port);
        if(bind(diskfd,(sockaddr*)&disk_serv_addr,sizeof(disk_serv_addr))==-1){
                perror("ERROR:binding\n");
                close(diskfd);
                exit(2);
        }
        if(listen(diskfd,1)==-1){
                perror("ERROR:listening\n");
                close(diskfd);
                exit(2);
        }
        printf("Accepting connections......\n");//here must have '\n',unless it cannot be print



        while (1) {
                socklen_t len=sizeof(client_addr);
                clientfd=accept(diskfd,(sockaddr*)&client_addr,&len);//here accept first parameter is the server itself
                if(clientfd==-1){
                        perror("ERROR:accepting\n");
                        close(clientfd);
                        continue;
                }
                printf("client connected, client socket: %d\n", clientfd);
                process_client();
                close(clientfd);
        }
}
