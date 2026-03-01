# <center>Project3 Typescript</center>
### some details about project 3
## step1
### Usage
first compile the code using the makefile in step1 directory
```shell
make
```
then run the disk program with the following command
```shell
 ./disk <#cylinders> <#sector per cylinder> <track-to-track delay> <#disk-storagefilename>
```
let me show you an example
```shell
./disk 3 4 1000 test.txt
```
the result:
![图 0](images/35555dc683f0aa5e9d45d83f6150a20a4c5f8b773aa0f572c0fa4cf0d2751e4f.png)  
and the disk.log file:
![图 1](images/db23523e45d35cee9daaf42ee6bfe704aaef064b73c3e8e85a35163582e3ae07.png)  
## step2
### Usage
first compile the code using the makefile in step1 directory
```shell
make
```
then run the disk program with the following command
```shell
 ./fs
```
let me show you an example
![图 2](images/06e16bca21b60de1db3c7c4ec1adf9673458eaf92739500d63e261c1ef34add1.png)  
the fs.log is like this:
![图 3](images/898ee445a3a50814f6333de9a7eeced00283ef24b83bf10412376b3cc2f7ea2e.png)  
## step3
### Usage
first compile the code using the makefile in step1 directory
```shell
make
```
then run the disk program with the following command
```shell
./disk1 <#cylinders> <#sector per cylinder> <track-to-track delay> <#disk-storagefilename> <disk port>
./fs <disk port> <fs port>
./client <fs port></fs>
```
then you can run the program.
some pictures are shown in the report.