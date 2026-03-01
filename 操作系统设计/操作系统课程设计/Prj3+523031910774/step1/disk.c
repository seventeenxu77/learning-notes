#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/mman.h>
#include <fcntl.h>
#define SECTOR_SIZE 256
#define CMD_BUFFERSIZE 1024
int present;//to record the distance of two cylinders
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
int I_function(){
        fprintf(disk.log_fp, "%d %d\n", disk.cylinders, disk.sector_per_cylinder);
        return 1;
}
int R_function(int c,int s){
        if(c<0||s<0||c>=disk.cylinders||s>=disk.sector_per_cylinder){//read range error
                printf("Instruction error!\n");
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
        int i=0;
        while(readpointer[i]&&i!=SECTOR_SIZE){
                fprintf(disk.log_fp, "%c", readpointer[i]);
                i++;
        }
        fprintf(disk.log_fp, "\n");
        return 1;

}
int W_function(int c,int s,char*data){
        if(c<0||s<0||c>=disk.cylinders||s>=disk.sector_per_cylinder){//read range error
                printf("Instruction error!\n");
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
        return -1;
}
int parse_command(const char *cmd) {
    char type;
    int c, s;
    char data[SECTOR_SIZE + 1];
    memset(data,0,sizeof(data));
    switch (cmd[0]) {
        case 'I':
            return I_function();
            break;
        case 'R':
             if (sscanf(cmd, "R %d %d", &c, &s) == 2) {
                     return R_function(c,s);
            }
            break;
        case 'W':
            int k;
            k=sscanf(cmd, "W %d %d %256[^\n]", &c, &s, data);
            if (k==3) return W_function(c,s,data);
            else if(k==2){
                    data[0]='\0';
                    return W_function(c,s,data);
            }
            break;
        case 'E':
            return E_function();
            break;
        default:
            fprintf(disk.log_fp, "Unknown command: %c\n", cmd[0]);
            return -1;
    }
    return 1;
}
void initialize(int cylinders,int sector_per_cylinder,double track_to_track_delay,char*filename){//you have to use * instead of &,because it is c not c++
        present=-1;//initialize the two records,-1 refers to this is the first cylinder
        disk.filename=strdup(filename);//use strdup function to avoid mannually allocate space for file, but we should free it by ourselves.
        disk.cylinders=cylinders;
        disk.sector_per_cylinder=sector_per_cylinder;
        disk.track_to_track_delay=track_to_track_delay;
        disk.log_fp = fopen("disk.log", "w");
        disk.fd = open (filename, O_RDWR | O_CREAT, 0);
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
int main(int argc, char *argv[]){
        if (argc != 5)
        {
                printf("Error Usage: %s <cylinders> <sector per cylinder> <track-to-track delay> <disk-storage-filename>\n", argv[0]);
                return 1;
        }
        int cylinders=atoi(argv[1]);
        int sector_per_cylinder=atoi(argv[2]);
        char*p;
        double track_to_track_delay = strtod(argv[3], &p);
        char*filename=argv[4];
        disktype disk;
        initialize(cylinders,sector_per_cylinder,track_to_track_delay,filename);
        char cmd[CMD_BUFFERSIZE];
        int status;
        while (fgets(cmd, sizeof(cmd), stdin)) {
        cmd[strcspn(cmd, "\n")] = '\0';//remove the n singnal
        status=parse_command(cmd);
        if(status==-1)
        {
                break;
        }
    }
}
