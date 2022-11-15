#include <arpa/inet.h> // inet_addr()
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <sys/socket.h>
#include <unistd.h>
#include <stdbool.h>
#define MAX 1024
#define PORT 9971

int main(){
    int socket_fd, connection_fd;
	struct sockaddr_in servaddr, cli;

	// socket create and verification
	if((socket_fd=socket(AF_INET, SOCK_STREAM, 0)) < 0){
		printf("socket creation failed...\n");
		exit(0);
	}
	else
		printf("Socket successfully created...\n");
    memset(&servaddr, 0, sizeof(servaddr));
	
	servaddr.sin_family = AF_INET;
	servaddr.sin_addr.s_addr = inet_addr("140.112.30.32"); // IP of workstation found with nslookup
	servaddr.sin_port = htons(PORT);

	if(connect(socket_fd, (struct sockaddr*)&servaddr, sizeof(servaddr)) < 0){
		printf("connection with the server failed...\n");
		exit(0);
	}
	else
		printf("connected to the server..\n");

	char buffer[MAX];
	int idx = 0;
	while(true){
        memset(buffer, 0, MAX);
		printf("To server: ");
		idx = 0;
		while ((buffer[idx++]=getchar()) != '\n');
		write(socket_fd, buffer, sizeof(buffer));
		if ((strncmp(buffer, "exit", 4)) == 0) {
			printf("Client Exit...\n");
			break;
		}
		memset(buffer, 0, MAX);
		read(socket_fd, buffer, sizeof(buffer));
		printf("From Server : %s", buffer);
		if ((strncmp(buffer, "exit", 4)) == 0) {
			printf("Client Exit...\n");
			break;
		}
	}

	close(socket_fd);
	return 0;
}
