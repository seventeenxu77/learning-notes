// implement matrix multiplication using matrix partition based algorithm with
// time complexity O(n3) : single process.
#include<stdio.h>
#include<string>
#include<cstring>
#include<stdlib.h>
#include<pthread.h>
#include<time.h>
#define snum 10000
int process_size;
int size;
int matrix_1[snum][snum];
int matrix_2[snum][snum];
int result[snum][snum];
int read(char*buffer,int& count){
        int num=0;
        while(buffer[count]!=' '&&buffer[count]!='\n'){
                if(buffer[count]=='|'){
                        count+=2;
                        continue;
                }
                num=num*10+(buffer[count]-'0');
                count++;
        }
        count++;
        return num;
}
int matrix_create(char*buffer,int matrix[snum][snum]){
        int count=0;
        int n=0;
        int index=0;
        while(buffer[index]!='|'){
                if(buffer[index]==' '){
                        n++;
                }
                index++;
        }

        for(int i=0;i<n;i++){
                for(int j=0;j<n;j++){
                        matrix[i][j]=read(buffer,count);
                }
        }
        return n;
}
void*phread_multi(void*ranknum){
        long begin=(long)ranknum;//long type can avoid precison loss
        long begin_num=begin*process_size;
        long last_num=(begin+1)*process_size-1;
        if(last_num>size-1)//take attention for this comparison
        {
                last_num=size-1;
        }
        for(int i=begin_num;i<=last_num;i++){
                for(int j=0;j<size;j++){
                        for(int k=0;k<size;k++){
                                result[i][j]+=matrix_1[i][k]*matrix_2[k][j];
                        }
                }
        }
        pthread_exit(NULL);//finish this thread

}
int main(int argc,char*argv[]){//here has to declare this two arguments,unless argc cannot be used
        srand(time(0));
        clock_t start,end;
        double elapsed;
        FILE*src;
        FILE*dest;//this decleration should be out the if section
        if(argc>1){
                size=atoi(argv[1]);
                dest=fopen("random.out","w+");
                if(dest==NULL){
                        printf("ERROR:could not open this file : random.out");
                        exit(-1);
                }
                for(int i=0;i<size;i++){
                        for(int j=0;j<size;j++){
                                matrix_1[i][j]=rand()%10;
                                matrix_2[i][j]=rand()%10;
                        }
                }
        }
        if(argc==1){
        src=fopen("data.in","r");
        if(src==NULL){
                printf("ERROR:could not open this file : data.in");
                exit(-1);
        }
        dest=fopen("data.out","w+");
        if(dest==NULL){
                printf("ERROR:could not open this file : data.out");
                exit(-1);
        }
        ssize_t n;
        char buffer[50000];
        while(n=fread(buffer,1,sizeof(buffer),src)>0){
                //printf("%s",buffer);
        }
        //printf("%s\n",buffer);
        matrix_create(buffer,matrix_1);//
        size=matrix_create(buffer,matrix_2);//data.out situation
        }
        //above code donot change,read matrix from data.in file
        pthread_t*thread_array=new pthread_t[size];
        for(int threadnum=1;threadnum<7;threadnum++){
        memset(result,0,sizeof(result));
        start=clock();
        process_size=(size%threadnum==0?size/threadnum:(size/threadnum)+1);
        int rc=0;
        pthread_attr_t attr;
        pthread_attr_init(&attr);
        pthread_attr_setdetachstate(&attr,PTHREAD_CREATE_JOINABLE);
        pthread_attr_setscope(&attr, PTHREAD_SCOPE_SYSTEM);
        for(long i=0;i<threadnum;i++){//set i into long type
                 rc = pthread_create (&thread_array[i], &attr, phread_multi, (void*)i);
                 if (rc) {
                         printf("ERROR; return code from pthread_create(t1) is %d\n", rc);
                         exit(-1);}
        }
        for(int i=0;i<threadnum;i++){
                void* status1;
                rc = pthread_join (thread_array[i], &status1);
                if (rc){
                        printf("ERROR; return code from pthread_join(t1)is %d\n", rc);
                        exit(-1);
                }
        }
        end=clock();
        elapsed=((double)(end-start))/CLOCKS_PER_SEC*1000;
        printf("threads:%d  runtime:%f\n",threadnum,elapsed);
        std::string path="src"+std::to_string(threadnum)+".txt";
        FILE*fp=fopen(path.c_str(),"a");
        if(fp==NULL){
                perror("cannot open file fp");
                return 1;
        }
        double size3=1000000*elapsed/(double)(size*size*size);
        fprintf(fp,"%f %d\n",size3,size);
        fclose(fp);
        }
        //below code donot change,write matrix into certain file
        //for(int i=0;i<size;i++){
        //        for(int j=0;j<size;j++){
        //                printf("%d\n",result[i][j]);
        //        }
        //}
        std::string matrix_out="";
        for(int i=0;i<size;i++){
                for(int j=0;j<size;j++){
                        matrix_out+=std::to_string(result[i][j]);
                        matrix_out+=" ";
                }
                if(i!=size-1){
                matrix_out+="| ";
                }
        //you can change outfile here
        }
        //printf("%s\n",matrix_out.c_str());
        if(argc>1){
                fwrite(matrix_out.c_str(),1,matrix_out.length(),dest);//here cannot use sizeof,because sizeof return the ocuupation of string subject rather than the length of str`
                fclose(dest);
        }
        if(argc==1){
                fwrite(matrix_out.c_str(),1,matrix_out.length(),dest);//if use char[],cannot use sizeof(char[]),that will cause 4000 to be writed into this file,which is wrong
                fclose(src);
                fclose(dest);
        }
}

          