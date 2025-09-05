#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <sys/types.h>
#include <sys/socket.h>

char *server_name = "localhost";
short int server_port = 3000;

void error(const char *msg) {
    perror(msg);
    exit(1);
}

int send_operation(unsigned char op, float a, float b) {
    int sockfd, n;
    struct sockaddr_in serv_addr;
    struct hostent *server;

    unsigned char recv_op = 0;
    float result = 0;

    printf("Sending request: op=%d, a=%f, b=%f\n", op, a, b);

    // Creazione socket
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) error("ERROR opening socket");

    server = gethostbyname(server_name);
    if (server == NULL) {
        fprintf(stderr, "ERROR, no such host\n");
        exit(0);
    }

    bzero((char *)&serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    bcopy((char *)server->h_addr, (char *)&serv_addr.sin_addr.s_addr, server->h_length);
    serv_addr.sin_port = htons(server_port);

    if (connect(sockfd, (const struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
        error("ERROR connecting");

    // Invia operazione
    n = write(sockfd, &op, sizeof(unsigned char));
    if (n < 0) error("ERROR writing op to socket");

    // Invia i due float (4 byte ciascuno)
    n = write(sockfd, &a, sizeof(float));
    if (n < 0) error("ERROR writing float a to socket");
    n = write(sockfd, &b, sizeof(float));
    if (n < 0) error("ERROR writing float b to socket");

    // Ricezione risposta
    n = read(sockfd, &recv_op, sizeof(unsigned char));
    if (n < 0) error("ERROR reading op from socket");
    n = read(sockfd, &result, sizeof(float));
    if (n < 0) error("ERROR reading result from socket");

    close(sockfd);

    // Stampa risultato
    const char *op_name;
    switch (op) {
        case 1: op_name = "sum"; break;
        case 2: op_name = "sub"; break;
        case 3: op_name = "mul"; break;
        case 4: op_name = "div"; break;
        default: op_name = "unknown"; break;
    }

    printf("Operation=%s [code=%d], Result=%f (server op=%d)\n",
           op_name, op, result, recv_op);

    return (recv_op == op);
}

int main() {
    // Test vari
    send_operation(1, 5.0f, 3.0f);   // somma
    send_operation(2, 10.0f, 4.0f);  // sottrazione
    send_operation(3, 2.5f, 4.0f);   // moltiplicazione
    send_operation(4, 20.0f, 5.0f);  // divisione
    send_operation(4, 7.0f, 2.0f);   // divisione non intera

    return 0;
}
