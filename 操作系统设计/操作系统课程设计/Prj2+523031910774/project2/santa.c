//
//santa
// After the ninth reindeer arrives, Santa must invoke prepareSleigh, and then all nine reindeer must invoke getHitched.
// After the third elf arrives, Santa must invoke helpElves. Concurrently, all three elves should invoke getHelp.
// All three elves must invoke getHelp before any additional elves enter (increment the elf counter).
// prepareSleigh should prior to  helpElves
// after the prepareSleigh reaches total , the santa will sleep forever ,all the threads will exit.
#include<stdio.h>
#include<stdlib.h>
#include<pthread.h>
#include<semaphore.h>
#include<unistd.h>
#define max_sleep 400
#define sleeptime usleep(rand()%max_sleep*1000)//in linux,sleep refers to s not ms,so we use usleep
#define longsleeptime usleep(rand()%(max_sleep*10)*1000)
int stepcount=0;
const int total=30;
const int reindeernum=9;
const int elfnum=10;
pthread_t santa_thread;
pthread_t reindeer_thread[reindeernum];
pthread_t elf_thread[elfnum];
int reindeer_id[reindeernum];
int elf_id[elfnum];
int reindeer_count=0;
int elf_count=0;
int endflag=0;
sem_t santawake;
sem_t reindeerwake;
sem_t elfwake;
sem_t mutex;
sem_t group;
sem_t confirm;
void*santa(void*arg){
        while(1){
                sem_wait(&santawake);
                sem_wait(&mutex);
                if(reindeer_count==reindeernum){
                        stepcount++;
                        if(stepcount==total)
                        {
                                printf("Santa: sleep forever\n");
                                break;
                        }
                        printf("Santa: PrepareSleigh\n");
                        for(int i=0;i<reindeernum;i++){
                                sleeptime;
                                sem_post(&reindeerwake);
                        }
                        for(int i=0;i<reindeernum;i++){
                                sem_wait(&confirm);
                        }
                        reindeer_count=0;
                }
                else if(elf_count==3){
                        printf("Santa: helpElves\n");
                        sleeptime;
                        for(int i=0;i<3;i++){
                                sleeptime;
                                sem_post(&elfwake);
                        }
                        for(int i=0;i<3;i++){
                                sem_wait(&confirm);
                        }
                        elf_count=0;
                        sem_post(&group);
                }
                sem_post(&mutex);
        }
        endflag=1;
        for(int i=0;i<elfnum;i++){
                sem_post(&group);
        }
        for(int i=0;i<elfnum;i++){
                sem_post(&elfwake);
        }//wake every  waiting elf
        for(int i=0;i<reindeernum;i++){
                sem_post(&reindeerwake);
        }//wake every reindeer
        pthread_exit(NULL);
}
void*reindeer(void*arg){
        int id=*(int*)arg;
        while(1){
                longsleeptime;
                sem_wait(&mutex);
                printf("reindeer %d: reach the North Pole\n", id);
                reindeer_count++;
                if(reindeer_count==reindeernum){
                        sem_post(&santawake);
                }
                sem_post(&mutex);
                sem_wait(&reindeerwake);
                longsleeptime;
                sem_post(&confirm);
                printf("reindeer %d: getHitched\n", id);
                if(endflag){
                        break;
                }
        }
        pthread_exit(NULL);
}
void*elf(void*arg){
    int id=*(int*)arg;
    while(1){
            longsleeptime;
            sem_wait(&group);
            if(endflag){
                    break;
            }
            sem_wait(&mutex);
            printf("Elf %d: wait in line\n", id);
            elf_count++;
            if(elf_count==3){
                    sem_post(&santawake);
            }
            else{
                    sem_post(&group);
            }
            sem_post(&mutex);
            sem_wait(&elfwake);
            longsleeptime;
            printf("Elf %d: getHelp\n", id);
            sem_post(&confirm);
            if(endflag){
                    break;
            }
            longsleeptime;
    }
    pthread_exit(NULL);
}
int main(){
    srand(time(NULL));
    sem_init(&santawake, 0, 1);
    sem_init(&reindeerwake, 0, 0);
    sem_init(&elfwake, 0, 0);
    sem_init(&mutex, 0, 1);
    sem_init(&group,0,1);
    sem_init(&confirm,0,0);
    pthread_create(&santa_thread,NULL,santa,NULL);
    for(int i=0;i<reindeernum;i++){
            reindeer_id[i]=i+1;
            pthread_create(&reindeer_thread[i],NULL,reindeer,&reindeer_id[i]);
    }
    for(int i=0;i<elfnum;i++){
            elf_id[i]=i+1;
            pthread_create(&elf_thread[i],NULL,elf,&elf_id[i]);
    }
    pthread_join(santa_thread, NULL);
    for (int i = 0; i < reindeernum; i++) {
            pthread_join(reindeer_thread[i], NULL);
    }
    for (int i = 0; i < elfnum; i++) {
            pthread_join(elf_thread[i], NULL);
    }
    sem_destroy(&santawake);
    sem_destroy(&reindeerwake);
    sem_destroy(&elfwake);
    sem_destroy(&mutex);
    sem_destroy(&group);
    sem_destroy(&confirm);
}
