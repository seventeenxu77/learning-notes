# <center>Project2 Typescript</center>
### some details about project 1
## faneuil
### Iinitialization
You can intialize the four parts in the `faneuil.c` file, and then compile the code.
```shell
#define threadnum 20
#define max_sleep 200
#define sleeptime usleep(rand()%max_sleep*1000)//in linux,sleep refers to s not ms,so we use usleep
#define longsleeptime usleep(rand()%(max_sleep*10)*1000)
```
You can change the threadnum to control the number of threads, and change the max_sleep to control the sleep time of the threads.

### Test
You can use this command to test the performance of the program:
```shell
./faneuil
```
This program will run infinite loop, and you can use `Ctrl+C` to stop it.Hre is an example of the output:
```shell
Immigrant #0 enter
Immigrant #0 checkIn
immigrant #0 sitdown
Immigrant #1 enter
Immigrant #1 checkIn
immigrant #1 sitdown
Spectator #0 enter
Spectator #0 spectate
Spectator #0 leave
Immigrant #2 enter
Immigrant #2 checkIn
immigrant #2 sitdown
Immigrant #3 enter
Immigrant #3 checkIn
immigrant #3 sitdown
Immigrant #4 enter
Immigrant #4 checkIn
immigrant #4 sitdown
Immigrant #5 enter
Immigrant #5 checkIn
immigrant #5 sitdown
Immigrant #6 enter
Immigrant #6 checkIn
immigrant #6 sitdown
Immigrant #7 enter
Immigrant #7 checkIn
immigrant #7 sitdown
Immigrant #8 enter
Immigrant #8 checkIn
immigrant #8 sitdown
Spectator #1 enter
Spectator #1 spectate
Spectator #1 leave
judge #0 enter
Judge #0 confirm the immigrant #1
Judge #0 confirm the immigrant #7
Judge #0 confirm the immigrant #0
Judge #0 confirm the immigrant #2
Judge #0 confirm the immigrant #3
Judge #0 confirm the immigrant #4
Judge #0 confirm the immigrant #5
Judge #0 confirm the immigrant #6
Judge #0 confirm the immigrant #8
Immigrant #6 swear
Immigrant #2 swear
Immigrant #3 swear
Immigrant #0 swear
Immigrant #8 swear
Immigrant #6 getCertificate
Immigrant #7 swear
Immigrant #2 getCertificate
Immigrant #4 swear
Immigrant #4 getCertificate
Immigrant #5 swear
Immigrant #8 getCertificate
Immigrant #1 swear
Immigrant #7 getCertificate
Immigrant #0 getCertificate
Immigrant #3 getCertificate
Immigrant #5 getCertificate
Immigrant #1 getCertificate
judge #0 leave
immigrant #2 leave
immigrant #8 leave
immigrant #6 leave
immigrant #7 leave
immigrant #0 leave
immigrant #3 leave
Immigrant #9 enter
Immigrant #9 checkIn
immigrant #9 sitdown
immigrant #4 leave
immigrant #5 leave
immigrant #1 leave
Immigrant #10 enter
Immigrant #10 checkIn
immigrant #10 sitdown
Immigrant #11 enter
Immigrant #11 checkIn
immigrant #11 sitdown
judge #1 enter
Judge #1 confirm the immigrant #9
Judge #1 confirm the immigrant #10
Judge #1 confirm the immigrant #11
Immigrant #11 swear
Immigrant #9 swear
Immigrant #9 getCertificate
Immigrant #11 getCertificate
Immigrant #10 swear
Immigrant #10 getCertificate
judge #1 leave
Spectator #2 enter
immigrant #9 leave
immigrant #11 leave
immigrant #10 leave
Spectator #2 spectate
Spectator #2 leave
Spectator #3 enter
Spectator #3 spectate
Spectator #3 leave
judge #2 enter
judge #2 leave
judge #3 enter
judge #3 leave
imm_num:12 jud_num:4 spec_num:4

```
You can know how many threads are running by the last line of the output.

## santa
### Iinitialization
You can intialize the four parts in the `santa.c` file, and then compile the code.
```shell
#define threadnum 20
#define max_sleep 200
#define sleeptime usleep(rand()%max_sleep*1000)//in linux,sleep refers to s not ms,so we use usleep
#define longsleeptime usleep(rand()%(max_sleep*10)*1000)
```
You can change the threadnum to control the number of threads, and change the max_sleep to control the sleep time of the threads.

### Test
You can use this command to test the performance of the program:
```shell
./santa
```
This program will run infinite loop, and you can use `Ctrl+C` to stop it.Hre is an example of the output, this is the simplified version:
```shell
Santa: helpElves
Elf 8: getHelp
Elf 7: getHelp
Elf 4: getHelp
Santa: helpElves
Elf 2: getHelp
Elf 3: getHelp
Elf 1: getHelp
Santa: helpElves
Elf 9: getHelp
Elf 10: getHelp
Elf 5: getHelp
Santa: PrepareSleigh
reindeer 2: getHitched
reindeer 9: getHitched
reindeer 7: getHitched
reindeer 4: getHitched
reindeer 3: getHitched
reindeer 8: getHitched
reindeer 5: getHitched
reindeer 1: getHitched
reindeer 6: getHitched
Santa: helpElves
Elf 3: getHelp
Elf 4: getHelp
Elf 6: getHelp
Santa: helpElves
Elf 2: getHelp
Elf 1: getHelp
Elf 8: getHelp
Santa: PrepareSleigh
reindeer 9: getHitched
reindeer 1: getHitched
reindeer 2: getHitched
reindeer 7: getHitched
reindeer 8: getHitched
reindeer 4: getHitched
reindeer 5: getHitched
reindeer 3: getHitched
reindeer 6: getHitched
Santa: helpElves
Elf 7: getHelp
Elf 9: getHelp
Elf 5: getHelp
Santa: helpElves
Elf 10: getHelp
Elf 3: getHelp
Elf 6: getHelp
Santa: helpElves
Elf 1: getHelp
Elf 3: getHelp
Elf 8: getHelp
Santa: PrepareSleigh
reindeer 7: getHitched
reindeer 9: getHitched
reindeer 4: getHitched
reindeer 3: getHitched
reindeer 6: getHitched
reindeer 2: getHitched
reindeer 5: getHitched
reindeer 1: getHitched
reindeer 8: getHitched
Santa: helpElves
Elf 4: getHelp
Elf 1: getHelp
Elf 5: getHelp
Santa: helpElves
Elf 2: getHelp
Elf 6: getHelp
Elf 9: getHelp
Santa: helpElves
Elf 7: getHelp
Elf 3: getHelp
Elf 10: getHelp
Santa: PrepareSleigh
reindeer 2: getHitched
reindeer 4: getHitched
reindeer 5: getHitched
reindeer 7: getHitched
reindeer 9: getHitched
reindeer 1: getHitched
reindeer 6: getHitched
reindeer 8: getHitched
reindeer 3: getHitched
Santa: helpElves
Elf 5: getHelp
Elf 6: getHelp
Elf 8: getHelp
Santa: helpElves
Elf 2: getHelp
Elf 1: getHelp
Elf 9: getHelp
Santa: helpElves
Elf 5: getHelp
Elf 10: getHelp
Elf 7: getHelp
Santa: PrepareSleigh
reindeer 6: getHitched
reindeer 3: getHitched
reindeer 7: getHitched
reindeer 8: getHitched
reindeer 1: getHitched
reindeer 5: getHitched
reindeer 4: getHitched
reindeer 2: getHitched
reindeer 9: getHitched
Santa: helpElves
Elf 7: getHelp
Elf 3: getHelp
Elf 4: getHelp
Santa: helpElves
Elf 1: getHelp
Elf 9: getHelp
Elf 2: getHelp
Santa: PrepareSleigh
reindeer 7: getHitched
reindeer 8: getHitched
reindeer 1: getHitched
reindeer 4: getHitched
reindeer 3: getHitched
reindeer 2: getHitched
reindeer 9: getHitched
reindeer 6: getHitched
Santa: helpElves
reindeer 5: getHitched
Elf 6: getHelp
Elf 8: getHelp
Elf 5: getHelp
Santa: helpElves
Elf 5: getHelp
Elf 3: getHelp
Elf 1: getHelp
Santa: PrepareSleigh
reindeer 7: getHitched
reindeer 6: getHitched
reindeer 8: getHitched
reindeer 1: getHitched
reindeer 4: getHitched
reindeer 2: getHitched
reindeer 9: getHitched
reindeer 3: getHitched
reindeer 5: getHitched
Santa: helpElves
Elf 10: getHelp
Elf 2: getHelp
Elf 7: getHelp
Santa: helpElves
Elf 4: getHelp
Elf 9: getHelp
Elf 6: getHelp
Santa: helpElves
Elf 8: getHelp
Elf 5: getHelp
Elf 1: getHelp
Santa: PrepareSleigh
reindeer 1: getHitched
reindeer 7: getHitched
reindeer 4: getHitched
reindeer 8: getHitched
reindeer 2: getHitched
reindeer 6: getHitched
reindeer 9: getHitched
reindeer 3: getHitched
reindeer 5: getHitched
Santa: helpElves
Elf 2: getHelp
Elf 7: getHelp
Elf 6: getHelp
Santa: helpElves
Elf 3: getHelp
Elf 9: getHelp
Elf 10: getHelp
Santa: PrepareSleigh
reindeer 3: getHitched
reindeer 5: getHitched
reindeer 7: getHitched
reindeer 9: getHitched
reindeer 4: getHitched
reindeer 6: getHitched
reindeer 1: getHitched
reindeer 8: getHitched
reindeer 2: getHitched
Santa: helpElves
Elf 1: getHelp
Elf 4: getHelp
Elf 3: getHelp
Santa: helpElves
Elf 7: getHelp
Elf 8: getHelp
Elf 10: getHelp
Santa: helpElves
Elf 5: getHelp
Elf 9: getHelp
Elf 2: getHelp
Santa: helpElves
Elf 7: getHelp
Elf 3: getHelp
Elf 4: getHelp
Santa: PrepareSleigh
reindeer 8: getHitched
reindeer 5: getHitched
reindeer 6: getHitched
reindeer 9: getHitched
reindeer 7: getHitched
reindeer 1: getHitched
reindeer 3: getHitched
reindeer 4: getHitched
reindeer 2: getHitched
Santa: helpElves
Elf 6: getHelp
Elf 8: getHelp
Elf 9: getHelp
Santa: helpElves
Elf 1: getHelp
Elf 5: getHelp
Elf 2: getHelp
Santa: helpElves
Elf 4: getHelp
Elf 5: getHelp
Elf 10: getHelp
Santa: PrepareSleigh
reindeer 5: getHitched
reindeer 7: getHitched
reindeer 1: getHitched
reindeer 4: getHitched
reindeer 2: getHitched
reindeer 8: getHitched
reindeer 6: getHitched
reindeer 9: getHitched
reindeer 3: getHitched
Santa: helpElves
Elf 8: getHelp
Elf 3: getHelp
Elf 7: getHelp
Santa: helpElves
Elf 1: getHelp
Elf 2: getHelp
Elf 6: getHelp
Santa: PrepareSleigh
reindeer 2: getHitched
reindeer 1: getHitched
reindeer 9: getHitched
reindeer 7: getHitched
reindeer 5: getHitched
reindeer 6: getHitched
reindeer 8: getHitched
reindeer 3: getHitched
reindeer 4: getHitched
Santa: helpElves
Elf 4: getHelp
Elf 9: getHelp
Elf 5: getHelp
Santa: helpElves
Elf 3: getHelp
Elf 1: getHelp
Elf 8: getHelp
Santa: PrepareSleigh
reindeer 5: getHitched
reindeer 2: getHitched
reindeer 7: getHitched
reindeer 4: getHitched
reindeer 8: getHitched
reindeer 3: getHitched
reindeer 6: getHitched
reindeer 9: getHitched
reindeer 1: getHitched
Santa: helpElves
Elf 5: getHelp
Elf 10: getHelp
Elf 7: getHelp
Santa: helpElves
Elf 3: getHelp
Elf 6: getHelp
Elf 2: getHelp
Santa: PrepareSleigh
reindeer 3: getHitched
reindeer 8: getHitched
reindeer 9: getHitched
reindeer 7: getHitched
reindeer 2: getHitched
reindeer 4: getHitched
reindeer 6: getHitched
reindeer 1: getHitched
reindeer 5: getHitched
Santa: helpElves
Elf 9: getHelp
Elf 5: getHelp
Elf 4: getHelp
Santa: PrepareSleigh
reindeer 2: getHitched
reindeer 7: getHitched
reindeer 8: getHitched
reindeer 3: getHitched
reindeer 9: getHitched
reindeer 4: getHitched
reindeer 6: getHitched
reindeer 1: getHitched
reindeer 5: getHitched
Santa: helpElves
Elf 8: getHelp
Elf 7: getHelp
Elf 1: getHelp
Santa: helpElves
Elf 6: getHelp
Elf 2: getHelp
Elf 10: getHelp
Santa: PrepareSleigh
reindeer 6: getHitched
reindeer 5: getHitched
reindeer 1: getHitched
reindeer 8: getHitched
reindeer 9: getHitched
reindeer 7: getHitched
reindeer 4: getHitched
reindeer 3: getHitched
reindeer 2: getHitched
Santa: helpElves
Elf 5: getHelp
Elf 4: getHelp
Elf 3: getHelp
Santa: helpElves
Elf 8: getHelp
Elf 1: getHelp
Elf 10: getHelp
Santa: helpElves
Elf 2: getHelp
Elf 7: getHelp
Elf 6: getHelp
Santa: PrepareSleigh
reindeer 1: getHitched
reindeer 4: getHitched
reindeer 2: getHitched
reindeer 7: getHitched
reindeer 8: getHitched
reindeer 9: getHitched
reindeer 5: getHitched
reindeer 3: getHitched
reindeer 6: getHitched
Santa: helpElves
Elf 8: getHelp
Elf 9: getHelp
Elf 6: getHelp
Santa: helpElves
Elf 2: getHelp
Elf 3: getHelp
Elf 10: getHelp
Santa: helpElves
Elf 5: getHelp
Elf 1: getHelp
Elf 4: getHelp
Santa: PrepareSleigh
reindeer 5: getHitched
reindeer 4: getHitched
reindeer 9: getHitched
reindeer 1: getHitched
reindeer 6: getHitched
reindeer 8: getHitched
reindeer 7: getHitched
reindeer 2: getHitched
reindeer 3: getHitched
Santa: helpElves
Elf 3: getHelp
Elf 7: getHelp
Elf 8: getHelp
Santa: helpElves
Elf 10: getHelp
Elf 9: getHelp
Elf 7: getHelp
Santa: PrepareSleigh
reindeer 9: getHitched
reindeer 6: getHitched
reindeer 8: getHitched
reindeer 2: getHitched
reindeer 3: getHitched
reindeer 5: getHitched
reindeer 1: getHitched
reindeer 7: getHitched
reindeer 4: getHitched
Santa: helpElves
Elf 5: getHelp
Elf 6: getHelp
Elf 4: getHelp
Santa: helpElves
Elf 2: getHelp
Elf 1: getHelp
Elf 7: getHelp
Santa: helpElves
Elf 3: getHelp
Elf 9: getHelp
Elf 8: getHelp
Santa: PrepareSleigh
reindeer 9: getHitched
reindeer 8: getHitched
reindeer 5: getHitched
reindeer 7: getHitched
reindeer 3: getHitched
reindeer 4: getHitched
reindeer 2: getHitched
reindeer 6: getHitched
reindeer 1: getHitched
Santa: helpElves
Elf 3: getHelp
Elf 10: getHelp
Elf 8: getHelp
Santa: helpElves
Elf 4: getHelp
Elf 5: getHelp
Elf 1: getHelp
Santa: helpElves
Elf 7: getHelp
Elf 6: getHelp
Elf 9: getHelp
Santa: PrepareSleigh
reindeer 9: getHitched
reindeer 4: getHitched
reindeer 2: getHitched
reindeer 7: getHitched
reindeer 5: getHitched
reindeer 8: getHitched
reindeer 1: getHitched
reindeer 3: getHitched
reindeer 6: getHitched
Santa: helpElves
Elf 10: getHelp
Elf 7: getHelp
Elf 2: getHelp
Santa: helpElves
Elf 3: getHelp
Elf 5: getHelp
Elf 4: getHelp
Santa: helpElves
Elf 8: getHelp
Elf 6: getHelp
Elf 1: getHelp
Santa: PrepareSleigh
reindeer 9: getHitched
reindeer 7: getHitched
reindeer 8: getHitched
reindeer 3: getHitched
reindeer 6: getHitched
reindeer 2: getHitched
reindeer 1: getHitched
reindeer 5: getHitched
reindeer 4: getHitched
Santa: helpElves
Elf 7: getHelp
Elf 9: getHelp
Elf 8: getHelp
Santa: helpElves
Elf 2: getHelp
Elf 4: getHelp
Elf 10: getHelp
Santa: helpElves
Elf 8: getHelp
Elf 3: getHelp
Elf 2: getHelp
Santa: PrepareSleigh
reindeer 9: getHitched
reindeer 7: getHitched
reindeer 8: getHitched
reindeer 5: getHitched
reindeer 6: getHitched
Santa: helpElves
reindeer 4: getHitched
reindeer 1: getHitched
reindeer 3: getHitched
reindeer 2: getHitched
Elf 4: getHelp
Elf 1: getHelp
Elf 5: getHelp
Santa: helpElves
Elf 2: getHelp
Elf 6: getHelp
Elf 8: getHelp
Santa: PrepareSleigh
reindeer 6: getHitched
reindeer 8: getHitched
reindeer 9: getHitched
reindeer 7: getHitched
reindeer 1: getHitched
reindeer 3: getHitched
reindeer 4: getHitched
reindeer 2: getHitched
Santa: helpElves
reindeer 5: getHitched
Elf 7: getHelp
Elf 3: getHelp
Elf 5: getHelp
Santa: helpElves
Elf 9: getHelp
Elf 1: getHelp
Elf 10: getHelp
Santa: helpElves
Elf 6: getHelp
Elf 8: getHelp
Elf 4: getHelp
Santa: PrepareSleigh
reindeer 3: getHitched
reindeer 9: getHitched
reindeer 1: getHitched
reindeer 7: getHitched
reindeer 4: getHitched
reindeer 2: getHitched
reindeer 5: getHitched
reindeer 8: getHitched
reindeer 6: getHitched
Santa: helpElves
Elf 5: getHelp
Elf 2: getHelp
Elf 3: getHelp
Santa: helpElves
Elf 10: getHelp
Elf 7: getHelp
Elf 9: getHelp
Santa: helpElves
Elf 6: getHelp
Elf 1: getHelp
Elf 8: getHelp
Santa: PrepareSleigh
reindeer 9: getHitched
reindeer 2: getHitched
reindeer 7: getHitched
reindeer 6: getHitched
reindeer 8: getHitched
reindeer 1: getHitched
reindeer 5: getHitched
reindeer 4: getHitched
Santa: helpElves
reindeer 3: getHitched
Elf 7: getHelp
Elf 9: getHelp
Elf 3: getHelp
Santa: helpElves
Elf 5: getHelp
Elf 2: getHelp
Elf 4: getHelp
Santa: helpElves
Elf 10: getHelp
Elf 3: getHelp
Elf 6: getHelp
Santa: PrepareSleigh
reindeer 9: getHitched
reindeer 1: getHitched
reindeer 7: getHitched
reindeer 6: getHitched
reindeer 4: getHitched
reindeer 8: getHitched
reindeer 5: getHitched
reindeer 3: getHitched
reindeer 2: getHitched
Santa: helpElves
Elf 4: getHelp
Elf 5: getHelp
Elf 9: getHelp
Santa: helpElves
Elf 7: getHelp
Elf 8: getHelp
Elf 1: getHelp
Santa: PrepareSleigh
reindeer 8: getHitched
reindeer 7: getHitched
reindeer 3: getHitched
reindeer 9: getHitched
reindeer 2: getHitched
reindeer 1: getHitched
reindeer 5: getHitched
reindeer 6: getHitched
reindeer 4: getHitched
Santa: helpElves
Elf 10: getHelp
Elf 5: getHelp
Elf 7: getHelp
Santa: helpElves
Elf 6: getHelp
Elf 3: getHelp
Elf 2: getHelp
Santa: helpElves
Elf 1: getHelp
Elf 8: getHelp
Elf 4: getHelp
Santa: PrepareSleigh
reindeer 1: getHitched
reindeer 3: getHitched
reindeer 9: getHitched
reindeer 4: getHitched
reindeer 7: getHitched
reindeer 5: getHitched
reindeer 6: getHitched
reindeer 2: getHitched
reindeer 8: getHitched
Santa: helpElves
Elf 2: getHelp
Elf 8: getHelp
Elf 9: getHelp
Santa: helpElves
Elf 3: getHelp
Elf 4: getHelp
Elf 7: getHelp
Santa: helpElves
Elf 6: getHelp
Elf 1: getHelp
Elf 5: getHelp
Santa: sleep forever
reindeer 5: getHitched
Elf 3: getHelp
reindeer 1: getHitched
reindeer 6: getHitched
reindeer 4: getHitched
reindeer 9: getHitched
reindeer 7: getHitched
reindeer 2: getHitched
reindeer 8: getHitched
reindeer 3: getHitched

```

If you want to  see more details about the output, you can see
----
```shell
reindeer 5: reach the North Pole
reindeer 7: reach the North Pole
Elf 2: wait in line
Elf 3: wait in line
Elf 9: wait in line
Santa: helpElves
Elf 3: getHelp
Elf 9: getHelp
Elf 2: getHelp
reindeer 1: reach the North Pole
Elf 4: wait in line
Elf 7: wait in line
Elf 1: wait in line
reindeer 9: reach the North Pole
Santa: helpElves
Elf 1: getHelp
Elf 4: getHelp
Elf 7: getHelp
Elf 5: wait in line
Elf 6: wait in line
reindeer 3: reach the North Pole
reindeer 6: reach the North Pole
reindeer 4: reach the North Pole
reindeer 2: reach the North Pole
Elf 10: wait in line
reindeer 8: reach the North Pole
Santa: PrepareSleigh
reindeer 7: getHitched
reindeer 9: getHitched
reindeer 5: getHitched
reindeer 4: getHitched
reindeer 3: getHitched
reindeer 6: getHitched
reindeer 1: getHitched
reindeer 8: getHitched
reindeer 2: getHitched
Santa: helpElves
Elf 10: getHelp
Elf 5: getHelp
Elf 6: getHelp
Elf 8: wait in line
reindeer 4: reach the North Pole
reindeer 8: reach the North Pole
reindeer 1: reach the North Pole
reindeer 6: reach the North Pole
reindeer 2: reach the North Pole
Elf 4: wait in line
reindeer 9: reach the North Pole
Elf 1: wait in line
Santa: helpElves
Elf 1: getHelp
Elf 8: getHelp
Elf 4: getHelp
Elf 8: wait in line
Elf 3: wait in line
Elf 9: wait in line
reindeer 3: reach the North Pole
Santa: helpElves
Elf 8: getHelp
Elf 3: getHelp
Elf 9: getHelp
reindeer 7: reach the North Pole
Elf 7: wait in line
Elf 10: wait in line
Elf 5: wait in line
Santa: helpElves
Elf 7: getHelp
Elf 10: getHelp
Elf 5: getHelp
Elf 2: wait in line
reindeer 5: reach the North Pole
Santa: PrepareSleigh
reindeer 4: getHitched
reindeer 6: getHitched
reindeer 1: getHitched
reindeer 2: getHitched
reindeer 3: getHitched
reindeer 7: getHitched
reindeer 9: getHitched
reindeer 5: getHitched
reindeer 8: getHitched
reindeer 3: reach the North Pole
Elf 6: wait in line
Elf 1: wait in line
Santa: helpElves
Elf 6: getHelp
Elf 1: getHelp
Elf 2: getHelp
Elf 4: wait in line
reindeer 1: reach the North Pole
reindeer 4: reach the North Pole
Elf 8: wait in line
reindeer 6: reach the North Pole
reindeer 9: reach the North Pole
reindeer 7: reach the North Pole
Elf 9: wait in line
reindeer 5: reach the North Pole
Santa: helpElves
Elf 9: getHelp
Elf 4: getHelp
Elf 8: getHelp
reindeer 8: reach the North Pole
reindeer 2: reach the North Pole
Santa: PrepareSleigh
reindeer 3: getHitched
reindeer 6: getHitched
reindeer 1: getHitched
reindeer 5: getHitched
reindeer 4: getHitched
reindeer 9: getHitched
reindeer 7: getHitched
reindeer 2: getHitched
reindeer 3: reach the North Pole
reindeer 8: getHitched
reindeer 1: reach the North Pole
reindeer 2: reach the North Pole
Elf 10: wait in line
reindeer 7: reach the North Pole
reindeer 6: reach the North Pole
reindeer 8: reach the North Pole
Elf 5: wait in line
reindeer 4: reach the North Pole
reindeer 5: reach the North Pole
Elf 1: wait in line
Santa: helpElves
Elf 10: getHelp
Elf 5: getHelp
Elf 1: getHelp
Elf 3: wait in line
Elf 7: wait in line
Elf 2: wait in line
Santa: helpElves
Elf 3: getHelp
Elf 7: getHelp
Elf 2: getHelp
reindeer 9: reach the North Pole
Santa: PrepareSleigh
reindeer 3: getHitched
reindeer 2: getHitched
reindeer 6: getHitched
reindeer 7: getHitched
reindeer 4: getHitched
reindeer 9: getHitched
reindeer 5: getHitched
reindeer 1: getHitched
reindeer 8: getHitched
Elf 7: wait in line
reindeer 2: reach the North Pole
Elf 2: wait in line
Elf 9: wait in line
Santa: helpElves
Elf 2: getHelp
Elf 7: getHelp
Elf 9: getHelp
Elf 6: wait in line
reindeer 9: reach the North Pole
Elf 10: wait in line
reindeer 3: reach the North Pole
reindeer 1: reach the North Pole
reindeer 8: reach the North Pole
Elf 1: wait in line
Santa: helpElves
Elf 6: getHelp
Elf 10: getHelp
Elf 1: getHelp
reindeer 7: reach the North Pole
Elf 4: wait in line
Elf 8: wait in line
Elf 3: wait in line
Santa: helpElves
Elf 4: getHelp
Elf 3: getHelp
Elf 8: getHelp
reindeer 6: reach the North Pole
reindeer 5: reach the North Pole
reindeer 4: reach the North Pole
Santa: PrepareSleigh
reindeer 2: getHitched
reindeer 9: getHitched
reindeer 3: getHitched
reindeer 1: getHitched
reindeer 7: getHitched
reindeer 6: getHitched
reindeer 5: getHitched
reindeer 8: getHitched
reindeer 4: getHitched
reindeer 1: reach the North Pole
Elf 2: wait in line
reindeer 2: reach the North Pole
reindeer 3: reach the North Pole
reindeer 7: reach the North Pole
reindeer 5: reach the North Pole
Elf 5: wait in line
Elf 10: wait in line
Santa: helpElves
Elf 2: getHelp
Elf 5: getHelp
Elf 10: getHelp
reindeer 6: reach the North Pole
Elf 6: wait in line
Elf 8: wait in line
Elf 1: wait in line
Santa: helpElves
Elf 6: getHelp
Elf 8: getHelp
Elf 1: getHelp
Elf 9: wait in line
reindeer 4: reach the North Pole
Elf 7: wait in line
reindeer 9: reach the North Pole
Elf 3: wait in line
Santa: helpElves
Elf 3: getHelp
Elf 9: getHelp
Elf 7: getHelp
reindeer 8: reach the North Pole
Elf 4: wait in line
Elf 6: wait in line
Elf 10: wait in line
Santa: PrepareSleigh
reindeer 1: getHitched
reindeer 2: getHitched
reindeer 7: getHitched
reindeer 3: getHitched
reindeer 5: getHitched
reindeer 6: getHitched
reindeer 9: getHitched
reindeer 4: getHitched
reindeer 8: getHitched
reindeer 5: reach the North Pole
Santa: helpElves
Elf 4: getHelp
Elf 6: getHelp
Elf 10: getHelp
Elf 2: wait in line
Elf 5: wait in line
Elf 1: wait in line
Santa: helpElves
Elf 1: getHelp
Elf 5: getHelp
Elf 2: getHelp
reindeer 1: reach the North Pole
Elf 8: wait in line
Elf 3: wait in line
reindeer 7: reach the North Pole
reindeer 3: reach the North Pole
reindeer 6: reach the North Pole
reindeer 4: reach the North Pole
Elf 10: wait in line
Santa: helpElves
Elf 8: getHelp
Elf 3: getHelp
Elf 10: getHelp
Elf 5: wait in line
Elf 7: wait in line
reindeer 2: reach the North Pole
reindeer 8: reach the North Pole
reindeer 9: reach the North Pole
Santa: PrepareSleigh
reindeer 5: getHitched
reindeer 1: getHitched
reindeer 9: getHitched
reindeer 2: getHitched
reindeer 3: getHitched
reindeer 7: getHitched
reindeer 8: getHitched
reindeer 6: getHitched
reindeer 4: getHitched
Elf 6: wait in line
Santa: helpElves
Elf 7: getHelp
Elf 6: getHelp
Elf 5: getHelp
reindeer 4: reach the North Pole
Elf 9: wait in line
Elf 1: wait in line
Elf 8: wait in line
Santa: helpElves
Elf 9: getHelp
Elf 8: getHelp
Elf 1: getHelp
reindeer 5: reach the North Pole
Elf 2: wait in line
Elf 3: wait in line
Elf 4: wait in line
Santa: helpElves
Elf 4: getHelp
Elf 3: getHelp
Elf 2: getHelp
reindeer 1: reach the North Pole
reindeer 7: reach the North Pole
reindeer 2: reach the North Pole
reindeer 6: reach the North Pole
Elf 10: wait in line
Elf 1: wait in line
Elf 6: wait in line
reindeer 9: reach the North Pole
Santa: helpElves
Elf 10: getHelp
Elf 6: getHelp
Elf 1: getHelp
reindeer 8: reach the North Pole
reindeer 3: reach the North Pole
Santa: PrepareSleigh
reindeer 5: getHitched
reindeer 1: getHitched
reindeer 7: getHitched
reindeer 2: getHitched
reindeer 6: getHitched
reindeer 3: getHitched
reindeer 4: getHitched
reindeer 9: getHitched
reindeer 8: getHitched
Elf 2: wait in line
Elf 9: wait in line
Elf 10: wait in line
Santa: helpElves
Elf 9: getHelp
Elf 2: getHelp
Elf 10: getHelp
reindeer 4: reach the North Pole
reindeer 6: reach the North Pole
Elf 5: wait in line
Elf 4: wait in line
reindeer 1: reach the North Pole
reindeer 2: reach the North Pole
reindeer 5: reach the North Pole
reindeer 8: reach the North Pole
reindeer 3: reach the North Pole
Elf 3: wait in line
Santa: helpElves
Elf 4: getHelp
Elf 5: getHelp
Elf 3: getHelp
Elf 7: wait in line
reindeer 7: reach the North Pole
Elf 8: wait in line
reindeer 9: reach the North Pole
Elf 1: wait in line
Santa: PrepareSleigh
reindeer 4: getHitched
reindeer 6: getHitched
reindeer 9: getHitched
reindeer 2: getHitched
reindeer 7: getHitched
reindeer 1: getHitched
reindeer 3: getHitched
reindeer 8: getHitched
reindeer 5: getHitched
Santa: helpElves
Elf 7: getHelp
Elf 8: getHelp
Elf 1: getHelp
reindeer 8: reach the North Pole
reindeer 2: reach the North Pole
Elf 5: wait in line
Elf 4: wait in line
reindeer 5: reach the North Pole
Elf 1: wait in line
reindeer 1: reach the North Pole
reindeer 6: reach the North Pole
Santa: helpElves
Elf 4: getHelp
Elf 1: getHelp
Elf 5: getHelp
reindeer 3: reach the North Pole
Elf 9: wait in line
Elf 3: wait in line
Elf 2: wait in line
reindeer 4: reach the North Pole
reindeer 7: reach the North Pole
Santa: helpElves
Elf 2: getHelp
Elf 9: getHelp
Elf 3: getHelp
Elf 6: wait in line
Elf 8: wait in line
Elf 10: wait in line
Santa: helpElves
Elf 10: getHelp
Elf 6: getHelp
Elf 8: getHelp
reindeer 9: reach the North Pole
Santa: PrepareSleigh
reindeer 8: getHitched
reindeer 5: getHitched
reindeer 2: getHitched
reindeer 4: getHitched
reindeer 7: getHitched
reindeer 3: getHitched
reindeer 9: getHitched
reindeer 1: getHitched
reindeer 6: getHitched
Elf 7: wait in line
Elf 1: wait in line
reindeer 7: reach the North Pole
reindeer 2: reach the North Pole
Elf 9: wait in line
Santa: helpElves
Elf 9: getHelp
Elf 1: getHelp
Elf 7: getHelp
reindeer 8: reach the North Pole
reindeer 4: reach the North Pole
reindeer 6: reach the North Pole
Elf 5: wait in line
reindeer 9: reach the North Pole
reindeer 1: reach the North Pole
reindeer 5: reach the North Pole
Elf 7: wait in line
Elf 10: wait in line
Santa: helpElves
Elf 5: getHelp
Elf 10: getHelp
Elf 7: getHelp
reindeer 3: reach the North Pole
Santa: PrepareSleigh
reindeer 4: getHitched
reindeer 3: getHitched
reindeer 8: getHitched
reindeer 5: getHitched
reindeer 9: getHitched
reindeer 1: getHitched
reindeer 6: getHitched
reindeer 7: getHitched
Elf 2: wait in line
reindeer 2: getHitched
reindeer 1: reach the North Pole
Elf 9: wait in line
Elf 3: wait in line
Santa: helpElves
Elf 9: getHelp
Elf 2: getHelp
Elf 3: getHelp
Elf 8: wait in line
Elf 4: wait in line
reindeer 9: reach the North Pole
reindeer 7: reach the North Pole
reindeer 8: reach the North Pole
reindeer 5: reach the North Pole
reindeer 6: reach the North Pole
Elf 7: wait in line
Santa: helpElves
Elf 4: getHelp
Elf 7: getHelp
Elf 8: getHelp
reindeer 3: reach the North Pole
reindeer 4: reach the North Pole
Elf 9: wait in line
Elf 10: wait in line
Elf 1: wait in line
Santa: helpElves
Elf 1: getHelp
Elf 9: getHelp
Elf 10: getHelp
Elf 6: wait in line
Elf 8: wait in line
reindeer 2: reach the North Pole
Santa: PrepareSleigh
reindeer 1: getHitched
reindeer 9: getHitched
reindeer 5: getHitched
reindeer 6: getHitched
reindeer 3: getHitched
reindeer 4: getHitched
reindeer 7: getHitched
reindeer 8: getHitched
reindeer 2: getHitched
Elf 2: wait in line
Santa: helpElves
Elf 8: getHelp
Elf 2: getHelp
Elf 6: getHelp
Elf 3: wait in line
reindeer 3: reach the North Pole
Elf 5: wait in line
reindeer 5: reach the North Pole
reindeer 8: reach the North Pole
reindeer 2: reach the North Pole
Elf 7: wait in line
reindeer 9: reach the North Pole
Santa: helpElves
Elf 7: getHelp
Elf 5: getHelp
Elf 3: getHelp
Elf 8: wait in line
reindeer 7: reach the North Pole
Elf 6: wait in line
Elf 4: wait in line
Santa: helpElves
Elf 8: getHelp
Elf 6: getHelp
Elf 4: getHelp
Elf 7: wait in line
reindeer 6: reach the North Pole
reindeer 1: reach the North Pole
Elf 9: wait in line
reindeer 4: reach the North Pole
Santa: PrepareSleigh
reindeer 3: getHitched
reindeer 5: getHitched
reindeer 8: getHitched
reindeer 9: getHitched
reindeer 2: getHitched
reindeer 7: getHitched
reindeer 6: getHitched
reindeer 1: getHitched
reindeer 4: getHitched
Elf 1: wait in line
Santa: helpElves
Elf 7: getHelp
Elf 1: getHelp
Elf 9: getHelp
reindeer 9: reach the North Pole
Elf 10: wait in line
Elf 5: wait in line
Elf 8: wait in line
Santa: helpElves
Elf 10: getHelp
Elf 5: getHelp
Elf 8: getHelp
reindeer 6: reach the North Pole
Elf 4: wait in line
reindeer 1: reach the North Pole
reindeer 4: reach the North Pole
Elf 2: wait in line
reindeer 5: reach the North Pole
reindeer 7: reach the North Pole
reindeer 3: reach the North Pole
Elf 3: wait in line
Santa: helpElves
Elf 3: getHelp
Elf 4: getHelp
Elf 2: getHelp
reindeer 8: reach the North Pole
reindeer 2: reach the North Pole
Elf 6: wait in line
Elf 7: wait in line
Santa: PrepareSleigh
reindeer 6: getHitched
reindeer 1: getHitched
reindeer 3: getHitched
reindeer 5: getHitched
reindeer 8: getHitched
reindeer 9: getHitched
reindeer 7: getHitched
reindeer 4: getHitched
reindeer 2: getHitched
Elf 5: wait in line
Santa: helpElves
Elf 6: getHelp
Elf 7: getHelp
Elf 5: getHelp
reindeer 8: reach the North Pole
reindeer 4: reach the North Pole
reindeer 3: reach the North Pole
Elf 1: wait in line
Elf 10: wait in line
reindeer 9: reach the North Pole
Elf 9: wait in line
Santa: helpElves
Elf 1: getHelp
Elf 10: getHelp
Elf 9: getHelp
reindeer 2: reach the North Pole
reindeer 6: reach the North Pole
reindeer 1: reach the North Pole
Elf 8: wait in line
Elf 4: wait in line
reindeer 5: reach the North Pole
reindeer 7: reach the North Pole
Santa: PrepareSleigh
reindeer 1: getHitched
reindeer 6: getHitched
reindeer 2: getHitched
reindeer 4: getHitched
reindeer 8: getHitched
reindeer 3: getHitched
reindeer 5: getHitched
reindeer 7: getHitched
reindeer 9: getHitched
reindeer 8: reach the North Pole
Elf 3: wait in line
Santa: helpElves
Elf 8: getHelp
Elf 3: getHelp
Elf 4: getHelp
reindeer 1: reach the North Pole
Elf 2: wait in line
reindeer 4: reach the North Pole
reindeer 9: reach the North Pole
reindeer 3: reach the North Pole
reindeer 2: reach the North Pole
Elf 6: wait in line
reindeer 5: reach the North Pole
Elf 5: wait in line
Santa: helpElves
Elf 6: getHelp
Elf 5: getHelp
Elf 2: getHelp
reindeer 6: reach the North Pole
Elf 10: wait in line
Elf 1: wait in line
Elf 4: wait in line
Santa: helpElves
Elf 4: getHelp
Elf 10: getHelp
Elf 1: getHelp
Elf 9: wait in line
Elf 7: wait in line
reindeer 7: reach the North Pole
Santa: PrepareSleigh
reindeer 1: getHitched
reindeer 4: getHitched
reindeer 2: getHitched
reindeer 6: getHitched
reindeer 3: getHitched
reindeer 9: getHitched
reindeer 7: getHitched
reindeer 8: getHitched
Elf 5: wait in line
Santa: helpElves
reindeer 5: getHitched
Elf 9: getHelp
Elf 5: getHelp
Elf 7: getHelp
reindeer 3: reach the North Pole
reindeer 5: reach the North Pole
Elf 3: wait in line
Elf 8: wait in line
reindeer 1: reach the North Pole
reindeer 4: reach the North Pole
reindeer 2: reach the North Pole
Elf 10: wait in line
Santa: helpElves
Elf 3: getHelp
Elf 8: getHelp
Elf 10: getHelp
Elf 2: wait in line
Elf 4: wait in line
Elf 1: wait in line
Santa: helpElves
Elf 4: getHelp
Elf 2: getHelp
Elf 1: getHelp
reindeer 6: reach the North Pole
reindeer 7: reach the North Pole
reindeer 8: reach the North Pole
Elf 5: wait in line
reindeer 9: reach the North Pole
Santa: PrepareSleigh
reindeer 3: getHitched
reindeer 4: getHitched
reindeer 2: getHitched
reindeer 5: getHitched
reindeer 1: getHitched
reindeer 6: getHitched
reindeer 7: getHitched
reindeer 9: getHitched
reindeer 8: getHitched
reindeer 7: reach the North Pole
Elf 6: wait in line
Elf 2: wait in line
Santa: helpElves
Elf 2: getHelp
Elf 5: getHelp
Elf 6: getHelp
reindeer 6: reach the North Pole
Elf 8: wait in line
Elf 1: wait in line
Elf 7: wait in line
Santa: helpElves
Elf 8: getHelp
Elf 7: getHelp
Elf 1: getHelp
reindeer 1: reach the North Pole
Elf 9: wait in line
reindeer 8: reach the North Pole
reindeer 4: reach the North Pole
Elf 4: wait in line
reindeer 5: reach the North Pole
Elf 1: wait in line
Santa: helpElves
Elf 4: getHelp
Elf 9: getHelp
Elf 1: getHelp
reindeer 2: reach the North Pole
reindeer 9: reach the North Pole
reindeer 3: reach the North Pole
Santa: PrepareSleigh
reindeer 6: getHitched
reindeer 7: getHitched
reindeer 4: getHitched
reindeer 8: getHitched
reindeer 1: getHitched
reindeer 5: getHitched
reindeer 2: getHitched
reindeer 9: getHitched
Elf 2: wait in line
reindeer 3: getHitched
reindeer 9: reach the North Pole
Elf 3: wait in line
reindeer 3: reach the North Pole
reindeer 1: reach the North Pole
Elf 10: wait in line
Santa: helpElves
Elf 3: getHelp
Elf 2: getHelp
Elf 10: getHelp
Elf 8: wait in line
Elf 6: wait in line
Elf 7: wait in line
Santa: helpElves
Elf 8: getHelp
Elf 6: getHelp
Elf 7: getHelp
reindeer 8: reach the North Pole
reindeer 5: reach the North Pole
Elf 9: wait in line
Elf 4: wait in line
reindeer 2: reach the North Pole
Elf 2: wait in line
Santa: helpElves
Elf 9: getHelp
Elf 4: getHelp
Elf 2: getHelp
Elf 1: wait in line
reindeer 4: reach the North Pole
reindeer 7: reach the North Pole
Elf 5: wait in line
reindeer 6: reach the North Pole
Santa: PrepareSleigh
reindeer 3: getHitched
reindeer 2: getHitched
reindeer 9: getHitched
reindeer 1: getHitched
reindeer 5: getHitched
reindeer 4: getHitched
reindeer 7: getHitched
reindeer 6: getHitched
reindeer 8: getHitched
reindeer 2: reach the North Pole
reindeer 9: reach the North Pole
reindeer 4: reach the North Pole
Elf 2: wait in line
Santa: helpElves
Elf 5: getHelp
Elf 2: getHelp
Elf 1: getHelp
reindeer 8: reach the North Pole
reindeer 3: reach the North Pole
reindeer 7: reach the North Pole
reindeer 6: reach the North Pole
Elf 5: wait in line
Elf 4: wait in line
Elf 8: wait in line
Santa: helpElves
Elf 8: getHelp
Elf 5: getHelp
Elf 4: getHelp
Elf 3: wait in line
Elf 2: wait in line
Elf 7: wait in line
reindeer 5: reach the North Pole
Santa: helpElves
Elf 3: getHelp
Elf 2: getHelp
Elf 7: getHelp
reindeer 1: reach the North Pole
Santa: PrepareSleigh
reindeer 3: getHitched
reindeer 8: getHitched
reindeer 6: getHitched
reindeer 5: getHitched
reindeer 1: getHitched
reindeer 4: getHitched
reindeer 7: getHitched
reindeer 2: getHitched
reindeer 9: getHitched
Elf 9: wait in line
reindeer 1: reach the North Pole
Elf 10: wait in line
Elf 1: wait in line
Santa: helpElves
Elf 9: getHelp
Elf 1: getHelp
Elf 10: getHelp
Elf 4: wait in line
reindeer 9: reach the North Pole
reindeer 6: reach the North Pole
reindeer 2: reach the North Pole
Elf 6: wait in line
Elf 3: wait in line
Santa: helpElves
Elf 4: getHelp
Elf 3: getHelp
Elf 6: getHelp
reindeer 8: reach the North Pole
reindeer 5: reach the North Pole
Elf 7: wait in line
Elf 1: wait in line
Elf 6: wait in line
Santa: helpElves
Elf 6: getHelp
Elf 1: getHelp
Elf 7: getHelp
reindeer 7: reach the North Pole
reindeer 4: reach the North Pole
reindeer 3: reach the North Pole
Santa: PrepareSleigh
reindeer 9: getHitched
reindeer 6: getHitched
reindeer 2: getHitched
reindeer 1: getHitched
reindeer 7: getHitched
reindeer 5: getHitched
reindeer 3: getHitched
reindeer 4: getHitched
Elf 2: wait in line
reindeer 2: reach the North Pole
reindeer 8: getHitched
reindeer 5: reach the North Pole
Elf 4: wait in line
reindeer 6: reach the North Pole
reindeer 9: reach the North Pole
Elf 5: wait in line
Santa: helpElves
Elf 2: getHelp
Elf 5: getHelp
Elf 4: getHelp
Elf 8: wait in line
Elf 10: wait in line
Elf 9: wait in line
Santa: helpElves
Elf 8: getHelp
Elf 9: getHelp
Elf 10: getHelp
reindeer 4: reach the North Pole
reindeer 3: reach the North Pole
Elf 6: wait in line
Elf 1: wait in line
reindeer 1: reach the North Pole
reindeer 7: reach the North Pole
reindeer 8: reach the North Pole
Santa: PrepareSleigh
reindeer 2: getHitched
reindeer 6: getHitched
reindeer 5: getHitched
reindeer 4: getHitched
reindeer 9: getHitched
reindeer 3: getHitched
reindeer 7: getHitched
reindeer 1: getHitched
reindeer 8: getHitched
Elf 4: wait in line
Santa: helpElves
Elf 1: getHelp
Elf 4: getHelp
Elf 6: getHelp
Elf 5: wait in line
Elf 3: wait in line
reindeer 6: reach the North Pole
Elf 2: wait in line
reindeer 4: reach the North Pole
Santa: helpElves
Elf 5: getHelp
Elf 3: getHelp
Elf 2: getHelp
Elf 9: wait in line
Elf 10: wait in line
reindeer 1: reach the North Pole
Elf 7: wait in line
reindeer 3: reach the North Pole
reindeer 8: reach the North Pole
Santa: helpElves
Elf 7: getHelp
Elf 10: getHelp
Elf 9: getHelp
reindeer 9: reach the North Pole
reindeer 5: reach the North Pole
reindeer 2: reach the North Pole
reindeer 7: reach the North Pole
Santa: PrepareSleigh
reindeer 4: getHitched
reindeer 6: getHitched
reindeer 2: getHitched
reindeer 9: getHitched
reindeer 1: getHitched
reindeer 8: getHitched
reindeer 7: getHitched
reindeer 5: getHitched
reindeer 3: getHitched
Elf 2: wait in line
reindeer 2: reach the North Pole
reindeer 3: reach the North Pole
Elf 8: wait in line
reindeer 8: reach the North Pole
Elf 5: wait in line
Santa: helpElves
Elf 5: getHelp
Elf 8: getHelp
Elf 2: getHelp
reindeer 4: reach the North Pole
reindeer 7: reach the North Pole
Elf 7: wait in line
reindeer 9: reach the North Pole
Elf 9: wait in line
Elf 3: wait in line
Santa: helpElves
Elf 9: getHelp
Elf 3: getHelp
Elf 7: getHelp
Elf 1: wait in line
Elf 4: wait in line
reindeer 5: reach the North Pole
reindeer 6: reach the North Pole
reindeer 1: reach the North Pole
Elf 6: wait in line
Santa: PrepareSleigh
reindeer 2: getHitched
reindeer 6: getHitched
reindeer 1: getHitched
reindeer 3: getHitched
reindeer 5: getHitched
reindeer 7: getHitched
reindeer 9: getHitched
reindeer 4: getHitched
reindeer 8: getHitched
Santa: helpElves
Elf 6: getHelp
Elf 4: getHelp
Elf 1: getHelp
reindeer 6: reach the North Pole
Elf 9: wait in line
Elf 10: wait in line
reindeer 1: reach the North Pole
reindeer 3: reach the North Pole
reindeer 5: reach the North Pole
Elf 6: wait in line
reindeer 2: reach the North Pole
Santa: helpElves
Elf 9: getHelp
Elf 10: getHelp
Elf 6: getHelp
Elf 8: wait in line
reindeer 7: reach the North Pole
Elf 2: wait in line
reindeer 8: reach the North Pole
Elf 5: wait in line
Santa: helpElves
Elf 8: getHelp
Elf 2: getHelp
Elf 5: getHelp
reindeer 4: reach the North Pole
reindeer 9: reach the North Pole
Santa: PrepareSleigh
reindeer 4: getHitched
reindeer 6: getHitched
reindeer 1: getHitched
reindeer 2: getHitched
reindeer 7: getHitched
reindeer 3: getHitched
reindeer 9: getHitched
reindeer 8: getHitched
reindeer 5: getHitched
Elf 7: wait in line
Elf 3: wait in line
Elf 10: wait in line
Santa: helpElves
Elf 7: getHelp
Elf 3: getHelp
Elf 10: getHelp
Elf 1: wait in line
Elf 4: wait in line
Elf 2: wait in line
Santa: helpElves
Elf 1: getHelp
Elf 4: getHelp
Elf 2: getHelp
reindeer 6: reach the North Pole
Elf 5: wait in line
reindeer 8: reach the North Pole
reindeer 5: reach the North Pole
reindeer 7: reach the North Pole
Elf 4: wait in line
reindeer 4: reach the North Pole
reindeer 1: reach the North Pole
reindeer 3: reach the North Pole
Elf 7: wait in line
Santa: helpElves
Elf 5: getHelp
Elf 4: getHelp
Elf 7: getHelp
Elf 8: wait in line
reindeer 9: reach the North Pole
reindeer 2: reach the North Pole
Santa: PrepareSleigh
reindeer 9: getHitched
reindeer 4: getHitched
reindeer 1: getHitched
reindeer 8: getHitched
reindeer 5: getHitched
reindeer 6: getHitched
reindeer 7: getHitched
reindeer 3: getHitched
reindeer 2: getHitched
Elf 2: wait in line
Elf 6: wait in line
Santa: helpElves
Elf 6: getHelp
Elf 2: getHelp
Elf 8: getHelp
reindeer 6: reach the North Pole
Elf 9: wait in line
reindeer 1: reach the North Pole
Elf 10: wait in line
reindeer 3: reach the North Pole
reindeer 7: reach the North Pole
reindeer 8: reach the North Pole
reindeer 4: reach the North Pole
reindeer 9: reach the North Pole
Elf 3: wait in line
reindeer 2: reach the North Pole
Santa: helpElves
Elf 10: getHelp
Elf 9: getHelp
Elf 3: getHelp
reindeer 5: reach the North Pole
Santa: PrepareSleigh
reindeer 6: getHitched
reindeer 3: getHitched
reindeer 8: getHitched
reindeer 9: getHitched
reindeer 1: getHitched
reindeer 7: getHitched
reindeer 4: getHitched
reindeer 5: getHitched
reindeer 2: getHitched
Elf 2: wait in line
Elf 1: wait in line
Elf 4: wait in line
Santa: helpElves
Elf 2: getHelp
Elf 1: getHelp
Elf 4: getHelp
Elf 7: wait in line
reindeer 7: reach the North Pole
reindeer 9: reach the North Pole
reindeer 5: reach the North Pole
Elf 5: wait in line
reindeer 6: reach the North Pole
reindeer 1: reach the North Pole
Elf 6: wait in line
Santa: helpElves
Elf 5: getHelp
Elf 7: getHelp
Elf 6: getHelp
reindeer 8: reach the North Pole
Elf 10: wait in line
reindeer 3: reach the North Pole
reindeer 4: reach the North Pole
reindeer 2: reach the North Pole
Santa: PrepareSleigh
reindeer 6: getHitched
reindeer 9: getHitched
reindeer 5: getHitched
reindeer 7: getHitched
reindeer 8: getHitched
Elf 8: wait in line
reindeer 2: getHitched
reindeer 3: getHitched
reindeer 1: getHitched
reindeer 4: getHitched
reindeer 4: reach the North Pole
Elf 9: wait in line
Santa: helpElves
Elf 10: getHelp
Elf 9: getHelp
Elf 8: getHelp
Elf 2: wait in line
reindeer 9: reach the North Pole
reindeer 8: reach the North Pole
Elf 5: wait in line
reindeer 3: reach the North Pole
Elf 8: wait in line
reindeer 7: reach the North Pole
Santa: helpElves
Elf 5: getHelp
Elf 2: getHelp
Elf 8: getHelp
reindeer 5: reach the North Pole
reindeer 6: reach the North Pole
Elf 6: wait in line
Elf 7: wait in line
Elf 1: wait in line
Santa: helpElves
Elf 7: getHelp
Elf 1: getHelp
Elf 6: getHelp
Elf 4: wait in line
Elf 3: wait in line
reindeer 1: reach the North Pole
reindeer 2: reach the North Pole
Santa: PrepareSleigh
reindeer 4: getHitched
reindeer 3: getHitched
reindeer 6: getHitched
reindeer 5: getHitched
reindeer 2: getHitched
reindeer 1: getHitched
reindeer 9: getHitched
reindeer 7: getHitched
reindeer 8: getHitched
Elf 9: wait in line
Santa: helpElves
Elf 4: getHelp
Elf 3: getHelp
Elf 9: getHelp
reindeer 3: reach the North Pole
reindeer 9: reach the North Pole
reindeer 5: reach the North Pole
Elf 10: wait in line
Elf 8: wait in line
Elf 7: wait in line
Santa: helpElves
Elf 10: getHelp
Elf 8: getHelp
Elf 7: getHelp
Elf 2: wait in line
reindeer 2: reach the North Pole
Elf 4: wait in line
Elf 5: wait in line
Santa: helpElves
Elf 4: getHelp
Elf 2: getHelp
Elf 5: getHelp
reindeer 6: reach the North Pole
reindeer 4: reach the North Pole
Elf 1: wait in line
Elf 6: wait in line
reindeer 8: reach the North Pole
reindeer 1: reach the North Pole
reindeer 7: reach the North Pole
Santa: sleep forever
reindeer 3: getHitched
Elf 6: getHelp
reindeer 9: getHitched
reindeer 2: getHitched
reindeer 5: getHitched
reindeer 6: getHitched
Elf 1: getHelp
reindeer 4: getHitched
reindeer 8: getHitched
reindeer 7: getHitched
reindeer 1: getHitched

```
