// Forking two processes to copy file using pipe system call.The name of two
// files are given as command line arguments
#include<stdio.h>
#include<stdlib.h>
#include<sys/types.h>
#include<sys/wait.h>
#include<unistd.h>
#include<time.h>
#include<string>
#include<cstring>
#include <sys/stat.h>
// 通过stat结构体 获得文件大小，单位字节
long getfilesize(const char *filename) {
    struct stat statbuf;
    // 调用 stat 函数获取文件状态信息
    if (stat(filename, &statbuf) == -1) {
        perror("filename:wrong");
        return -1;
    }
    // 返回文件大小
    return (long)statbuf.st_size;
}

int main(int argc,char*argv[]){
        FILE*src;
        int size=atoi(argv[3]);
        if(size<=0)
        {
                printf("ERROR:Buffersize wrong: '%d'.\n",size);
                exit(-1);
        }
        src=fopen(argv[1],"r");
        if(src==NULL){
                printf("ERROR:could not open this file '%s'.\n",argv[1]);
                exit(-1);
        }
        FILE*dest;
        dest=fopen(argv[2],"w+");
        if(dest==NULL){
                printf("ERROR:could not open this file '%s'.\n",argv[2]);
                fclose(src);
                exit(-1);
        }
        int mypipe[2];
        if(pipe(mypipe)){
                fprintf(stderr,"ERROR:pipe failed.\n");
                return -1;
        }
        pid_t ForkPID;
        ForkPID=fork();
        clock_t start,end;
        double elapsed;
        start=clock();//start time should be set in father process,because clock calculates by CPU ticks not realtime
        switch(ForkPID){
                case -1:
                        printf("ERROR:failed to fork.\n");
                        break;
                case 0:
                        {
                        char buffer[size];
                        close(mypipe[0]);
                        ssize_t n;
                        while((n=fread(buffer,1,sizeof(buffer),src))>0)
                        {
                                write(mypipe[1],buffer,n);
                        }
                        close(mypipe[1]);
                        fclose(src);
                        printf("Read file end.\n");
                        exit(0);
                        }
                default:
                        {
                        char buffer[size];
                        wait(NULL);
                        close(mypipe[1]);
                        ssize_t n;
                        while((n=read(mypipe[0],buffer,sizeof(buffer)))>0){
                                fwrite(buffer,1,n,dest);
                        }
                        end=clock();
                        close(mypipe[0]);
                        fclose(dest);
                        printf("Write file end.\n");
                        //here is not right to add "exit(0)"
                        }

        }
        elapsed=((double)(end-start))/CLOCKS_PER_SEC*1000;
        printf("Time used %fmilisecond.\n",elapsed);
        long filesize=getfilesize("src.txt");//at beginning,I use copy.txt,it outputs -inf which means infinite
        //std::string path="src"+std::to_string(filesize/1000000)+".txt";
        std::string path="src00.txt";
        FILE *fp = fopen(path.c_str(), "a");
        if (fp == NULL) {
        perror("can not open file fp");
        return 1;
        }
        // write float  into file
        //float result=(elapsed/(float)(filesize));
        fprintf(fp, "%f %d\n", elapsed,size);
        fclose(fp);
}
     