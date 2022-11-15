#include <stdio.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdbool.h>
#define MAX 1024
#define PORT 9971

bool web = false;

int main(){
    int socket_fd, connection_fd;
	struct sockaddr_in servaddr, cli;
    int socket_opt = 1;

    // create socket
    if((socket_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
        printf("socket create failed...\n");
    else{
        printf("Socket successfully created...\n");
        memset(&servaddr, 0, sizeof(servaddr));

    	if(setsockopt(socket_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, (char *)&socket_opt, sizeof(socket_opt)) < 0){
			perror("setsockopt");
			exit(EXIT_FAILURE);
		}
    }
	servaddr.sin_family = AF_INET;
	servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
	servaddr.sin_port = htons(PORT);
    // Binding socket to given IP and verification
	if((bind(socket_fd, (struct sockaddr*)&servaddr, sizeof(servaddr))) < 0){
		printf("socket bind failed...\n");
		exit(0);
	}
	else
		printf("Socket successfully binded...\n");
    if((listen(socket_fd, 5)) < 0){
		printf("Listen failed...\n");
		exit(0);
	}
	else
		printf("Server listening..\n");
	int len = sizeof(cli);
	while(true){
		if((connection_fd = accept(socket_fd, (struct sockaddr*)&cli, &len)) < 0){
			printf("server accept failed...\n");
			exit(0);
		}
		else
			printf("server accept the client...\n");

		// communication between client and server using fork()
		if(fork() == 0){
			char buffer[MAX];
			int idx = 0;
			while(true){
				memset(buffer, 0, MAX);
				if(!web){
					read(connection_fd, buffer, sizeof(buffer));
					printf("From client: %s", buffer);
					if(strncmp("exit", buffer, 4) == 0){
					printf("Server Exit...\n");
					break;
				}
				}
				if(strncmp(buffer, "GET", 3) == 0){
					memset(buffer, 0, MAX);
					char *reply = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n<h1>I am Weiber. Welcome to my space.</h1><h2>E-mail: b09902123@ntu.edu.tw<h2>";
					sprintf(buffer, "%s", reply);
					write(connection_fd, buffer, sizeof(buffer));
					web = true;
					break;
				}

				// message to client
				printf("To client: ");
				memset(buffer, 0, MAX);
				idx = 0;
				while((buffer[idx++]=getchar()) != '\n');
				
				if(strncmp("exit", buffer, 4) == 0){
					printf("Server Exit...\n");
					break;
				}
				write(connection_fd, buffer, sizeof(buffer));
				// write(connection_fd, "<br>", sizeof("<br>"));
			}
			close(connection_fd);
			_exit(0);
		}
	}
    close(socket_fd);
    return 0;
}
