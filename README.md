# MyWebsite
This repository contains the file to built a simple website support following features.
## Phase 1
### exchange message between server and client
1. Use the follow command to compile and run server
```shell
gcc server.c -o server
./server
```
2. Use the follow command to compile and run client
```shell
gcc client.c -o client
./client
```
3. Then, we can type in whatever sentences want to sent in client and server in turns. If you want to close/stop the connection, just enter "exit" in the client.

### view my profile with browser
1. Use the follow command to compile and run server(My server has been running on workstation of NTU CSIE.)
```shell
gcc server.c -o server
./server
```
2. Copy the url below to your browser(choose one of them). The port number I choose is 9971(randomly).
```
linux1.csie.ntu.edu.tw:9971
http://140.112.30.32:9971/
```

## Phase 2
### Environment Requirement
To install required python module, run the following instruction
```shell
pip install -r requirement.txt
```
### Feature Exploration
I implement following 3 features using python socket and make it an desktop application(.exe).
* message board
* video streaming
* audio streaming

To explore these features, you have to run server.py and a corresponding client.py
```shell
python3 server.py

python3 client.py # if you want a exe version try the following command
```
```shell
pyinstaller client.py
./dist/client
```
Then, client will ask you to choose the features you want to use first.
* board - message board
* video - video streaming
* audio - audio streaming

After that, you can just follow the command show in terminal and enjoy these features

demo: https://youtu.be/q8MDz0_sJGI
