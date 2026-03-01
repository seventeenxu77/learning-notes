# <center>Project1 Typescript</center>
### some details about project 1
## Copy
### Usage
```shell
./copy <InputFile><OutputFile><BufferSize>
```
This command can copy content from InputFile to OutputFile
You should provide the path of InputFile and OutputFile, and the buffer size 
however, the path of OutputFile can be a directory, and the file itself does not exist, so it will be created.
for example, if you want to copy `src.txt` to `dest.txt` with a buffersize of `200`.
you can use this line of code:
```shell
./copy src.txt dest.txt 200
```
if all goes well, you will see the time used in milliseconds.
```shell
Read file end.
Write file end.
Time used 1.219000milisecond.
```
### Error Message
* Buffersize error
```shell
ERROR:Buffersize wrong: '<BufferSize>'
```
* Read file error
```shell
ERROR:could not open this file '<InputFile>'
```
* Pipe create error
```shell
ERROR:pipe failed
```
* Fork error
```shell
ERROR:failed to fork.
```
### Test
if you want to use diffefent buffer size to test the performance of the program, you can use this command:
it will create a file `'src00.txt'` which contains the time used in milliseconds for each buffer size.
```shell
./fcreate.sh
```
then run gnuplot command like this:
```shell
gnuplot
gnuplot> load 'copy.plt'
gnuplot> exit
```
then you can see the result in `re.png` file.
```shell
xdg-open re.png
```
## shell
### Usage
##### sever create
```shell
./shell <Port>
```
if executed successfully, you will see the following message:
```shell
Accepting connections......
```
##### client connect
This command will start a shell server on the specified port
you can use `telnet` to connect to it like this.
```shell
telnet localhost <Port>
```
You should run the shell server first, and then run the telnet command in client terminal.
if executed successfully, you will see the following message:
```shell
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
```
##### client send command
You can send any command to the server, and the server will execute it and return the result to you,for example:
```shell
ls -l | wc | wc
```
The server will execute the command and return the result to you, like this:
```shell
received command from ip:127.0.0.1 port:50300 :ls -l | wc | wc
```
The client will receive the result of the command, like this:
```shell
      1      3     24
```
You can use 'exit' to exit the client, and the server will close the connection with you.
The sever will show the message:
```shell
success:close client connection from ip: 127.0.0.1 port: 50300
```
The client will show the message:
```shell
Connection closed by foreign host.
```
You can use `Ctrl+C` to exit the server, and the server will close all connections with clients.
### Error Message
* socket error
```shell
ERROR:opening socket
```
* bind error
```shell
ERROR:binding socket
```
* listen error
```shell
ERROR:listen socket
```
* accept error
```shell
ERROR:accept socket
```
* fork error
```shell
ERROR:fork error
```
* pipe error
```shell
ERROR:pipe error
```
* Invalid commands or invalid arguments
```shell
ERROR:running command:'<Command>'
```

## Matrix
### Usage
There are three ways to run the program:
```shell
./single #read from data.in file, write to data.out file,run in single process
./multi #read from data.in file, write to data.out file,run in multi process
./multi <Size> #generate Size*Size matrix A and B, do A*B and write to random.out file
```
If you use the first way,you may see the following message:
```shell
thread:1  runtime:0.350000
```
If you use the second and third way,you may see the following message:
```shell
threads:2  runtime:0.350000
threads:3  runtime:0.152000
threads:4  runtime:0.116000
threads:5  runtime:0.187000
threads:6  runtime:0.253000
```
### Error Message
* File open error
```shell
ERROR:could not open this file : <FileName>
```
* Phread create error
```shell
RROR; return code from pthread_create(t1) is <ErrorCode>
```
* Phread join error
```shell
ERROR; return code from pthread_join(t1) is <ErrorCode>
```
### Test
if you want to test the performance of different thread number in different matrix size, you can use this command:
```shell
./mac.sh
```
then run gnuplot command like this:
```shell
gnuplot
gnuplot> load 'matrix.plt'
gnuplot> exit
```
then you can see the result in `matrix.png` file.
```shell
xdg-open matrix.png
```
