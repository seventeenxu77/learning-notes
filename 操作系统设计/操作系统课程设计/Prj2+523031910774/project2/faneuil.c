//
// faneuil
// Immigrants must invoke enter, checkIn, sitDown, swear, getCertificate and leave.
// The judge invokes enter, confirm and leave.
// Spectators invoke enter, spectate and leave.
// While the judge is in the building, no one may enter and immigrants may not leave.
// The judge can not confirm until all immigrants, who have invoked enter, have also invoked checkIn.
//
#include<stdio.h>
#include<stdlib.h>
#include<pthread.h>
#include<semaphore.h>
#include<unistd.h>
#define threadnum 20
#define max_sleep 200
#define sleeptime usleep(rand()%max_sleep*1000)//in linux,sleep refers to s not ms,so we use usleep
#define longsleeptime usleep(rand()%(max_sleep*10)*1000)
sem_t judge;
sem_t mutex;
sem_t checkin;
sem_t confirm;
sem_t remain;
sem_t all_confirmed;
pthread_t thread_array[threadnum];
const int imm_range=6;
const int jud_range=8;
const int spe_range=10;
const int range_max=10;
int judge_id=-1;
int judge_num=0;
int immigrant_id=-1;
int spectator_id=-1;
int enter=0;//immigrants who have come in the building
int checked=0;
int confirmed;
int total;
void*immigrants_func(void*arg){
        sem_wait(&judge);
        immigrant_id++;
        int id=immigrant_id;//local name
        printf("Immigrant #%d enter\n", id);
        sem_wait(&mutex);
        enter++;
        //
        //remaining code
        //total--;
        //if(total==1){
        //        sem_post(&remain);
        //}
        sem_post(&mutex);
        sem_post(&judge);
        sleeptime;
        sem_wait(&mutex);
        printf("Immigrant #%d checkIn\n", id);
        checked++;
        sleeptime;
        printf("immigrant #%d sitdown\n",id);
        if(judge_num>0&&enter==checked){//there is a judge waiting for checkin signal
                sem_post(&checkin);//if receive judge mutex,then skip the release mutex process,release checkin signal
        }else{sem_post(&mutex);}//if do not receive judge mutex,it should release it
        sem_wait(&confirm);
        printf("Judge #%d confirm the immigrant #%d\n", judge_id, id);
        sem_post(&confirm);
        sleeptime;
        printf("Immigrant #%d swear\n", id);
        sleeptime;
        printf("Immigrant #%d getCertificate\n", id);
        sem_wait(&mutex);
        confirmed++;
        if(confirmed==enter){
                sem_post(&all_confirmed);
        }
        sem_post(&mutex);
        sleeptime;
        sem_wait(&judge);
        printf("immigrant #%d leave\n",id);
        sem_post(&judge);
        pthread_exit(NULL);
}
void*judge_func(void*arg){
        sem_wait(&judge);
        sem_wait(&mutex);//use mutex to occupy the usage of 'enter' variable
        judge_id++;
        judge_num++;
        //
        //remaining code
        //total--;
        //if(total==1){
        //        sem_post(&remain);
        //}
        printf("judge #%d enter\n",judge_id);
        sleeptime;
        int id=judge_id;
        if(enter-checked>0){//in case of that this building is no people
        sem_post(&mutex);//before judge getting in,there are several immigrants,ensure all of them have checked in
        sem_wait(&checkin);
        }
        sem_post(&mutex);
        for(int i=0;i<enter;i++){//do not bring in 'enter-confirmed',just make it 0 at the end,because imm_func will change confirmed 
                longsleeptime;
                sem_post(&confirm);
            }
            if(enter>0){
            sem_wait(&all_confirmed);
            }
            for(int i=0;i<enter;i++){
                    sem_wait(&confirm);
            }
            enter=checked=confirmed=0;
            sleeptime;
            printf("judge #%d leave\n",id);
            judge_num--;
            sem_post(&judge);
            pthread_exit(NULL);
    }
    void*spectator_func(void*arg){
            sem_wait(&judge);
            spectator_id++;
            sem_wait(&mutex);
            //
            //remaining code
            //total--;
            //if(total==1){
            //      sem_post(&remain);
            //}
            ////
            sem_post(&mutex);
            int id=spectator_id;
            printf("Spectator #%d enter\n", id);
            sem_post(&judge);
            longsleeptime;
            printf("Spectator #%d spectate\n", id);
            longsleeptime;
            printf("Spectator #%d leave\n", id);
            pthread_exit(NULL);
    }
    
    void generate_threads(int pid){
            int sort=rand()%range_max+1;
            int rc=0;
            //
            //remaining code
            //if(pid==threadnum-1){
            //      sem_wait(&remain);//ensure all the thread get the judge signal
            //      rc = pthread_create (&thread_array[pid],NULL, judge_func, NULL);
            //      return;
            //}
            //
            if(sort<=imm_range){
                    rc = pthread_create (&thread_array[pid],NULL, immigrants_func, NULL);
            }
            else if(sort<=jud_range){
                    rc = pthread_create (&thread_array[pid],NULL, judge_func, NULL);
            }
            else{
                    rc = pthread_create (&thread_array[pid],NULL, spectator_func, NULL);
            }
            if (rc) {
                    printf("ERROR; return code from pthread_create(t1) is %d\n", rc);
                    exit(-1);
            }
    }
    int main(){
            srand(time(NULL));
            sem_init(&judge,0,1);
            sem_init(&mutex,0,1);
            sem_init(&checkin,0,0);
            sem_init(&confirm,0,0);
            sem_init(&remain,0,0);
            sem_init(&all_confirmed,0,0);
            //
            //remaining code
            //total=threadnum;
            //int i=0;
            //while(i<threadnum){
            //      longsleeptime;
            //      generate_threads(i);
            //      i++;
            //      longsleeptime;
            //}
            //
            while(1){
                    longsleeptime;
                    generate_threads(0);
            }
    
            //
            //remaining code
            //for(int i=0;i<threadnum;i++){
            //        void* status1;
            //        int rc = pthread_join (thread_array[i], &status1);
            //        if (rc){
            //                printf("ERROR; return code from pthread_join(t1)is %d\n", rc);
        //                exit(-1);
        //       }
        //}
        printf("imm_num:%d jud_num:%d spec_num:%d\n",immigrant_id+1,judge_id+1,spectator_id+1);
        sem_destroy(&judge);
        sem_destroy(&mutex);
        sem_destroy(&checkin);
        sem_destroy(&confirm);
        sem_destroy(&remain);
        sem_destroy(&all_confirmed);

}
    