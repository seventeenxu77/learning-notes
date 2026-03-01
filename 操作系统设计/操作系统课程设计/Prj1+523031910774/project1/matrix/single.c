// implement matrix multiplication using matrix partition based algorithm with
// time complexity O(n3) : multiple processes.
#include<stdio.h>
#include<cstring>
#include<string>
#include<stdlib.h>
#include<pthread.h>
#include<time.h>
#define B 5
#define arraysize 2000
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
int matrix_create(char*buffer,int matrix[arraysize][arraysize]){
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
int matrix_multiply(int matrix_1[arraysize][arraysize],int matrix_2[arraysize][arraysize],int result[arraysize][arraysize],int n){
        for(int i=0;i<n;i++){
                for(int j=0;j<n;j++){
                        for(int k=0;k<n;k++){
                                result[i][j]+=matrix_1[i][k]*matrix_2[k][j];
                        }
                }
        }
        return 1;
}
void matrix_multiply2(int matrix_1[arraysize][arraysize],int matrix_2[arraysize][arraysize],int result[arraysize][arraysize],int N) {
    for (int i = 0; i < N; i += B) {
        for (int j = 0; j < N; j += B) {
            for (int k = 0; k < N; k += B) {
                // process every small matrix
                for (int ii = i; ii < i + B && ii < N; ii++) {
                    for (int jj = j; jj < j + B && jj < N; jj++) {
                        int sum = 0;
                        for (int kk = k; kk < k + B && kk < N; kk++) {
                            sum += matrix_1[ii][kk] * matrix_2[kk][jj];
                        }
                        result[ii][jj] += sum;
                    }
                }
            }
        }
    }
}
int main(){
        FILE*src;
        src=fopen("data.in","r");
        if(src==NULL){
                printf("ERROR:could not open this file : data.in");
                exit(-1);
        }
        FILE*dest;
        dest=fopen("data.out","w+");
        if(dest==NULL){
                printf("ERROR:could not open this file : data.out");
                exit(-1);
        }
        ssize_t n;
        char buffer[4000];
        while(n=fread(buffer,1,sizeof(buffer),src)>0){
                //printf("%s",buffer);
        }
        //printf("%s",buffer);
        int size=0;
        int matrix_1[arraysize][arraysize];
        int matrix_2[arraysize][arraysize];
        int result[arraysize][arraysize];
        memset(result,0,sizeof(result));
        matrix_create(buffer,matrix_1);
        size=matrix_create(buffer,matrix_2);
        //matrix_multiply(matrix_1,matrix_2,result,size);
        matrix_multiply2(matrix_1,matrix_2,result,size);
        for(int i=0;i<size;i++){
                for(int j=0;j<size;j++){
                        //printf("%d\n",result[i][j]);
                }
        }
        char buffer_out[4000];
        std::string matrix_out="";
        for(int i=0;i<size;i++){
                for(int j=0;j<size;j++){
                        matrix_out+=std::to_string(result[i][j]);
                        matrix_out+=" ";
                }
                if(i!=size-1){
                matrix_out+="| ";
                }
        }
        fwrite(matrix_out.c_str(),1,matrix_out.length(),dest);//if use char[],cannot use sizeof(char[]),that will cause 4000 to be writed into this file,which is wrong
        //printf("%s",matrix_out.c_str());
        fclose(src);
        fclose(dest);
}
                