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

int send_string(const char *str) {
    int sockfd, n;
    struct sockaddr_in serv_addr;
    struct hostent *server;

    uint16_t len = strlen(str);
    uint16_t len_be = htons(len);   // big endian
    uint16_t recv_len;
    char buffer[1024];              // buffer risposta

    printf("Sending request: \"%s\"\n", str);

    // Creazione socket
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) error("ERROR opening socket");

    server = gethostbyname(server_name);
    if (server == NULL) {
        fprintf(stderr, "ERROR, no such host\n");
        exit(0);
    }

    bzero((char *) &serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    bcopy((char *) server->h_addr, (char *) &serv_addr.sin_addr.s_addr, server->h_length);
    serv_addr.sin_port = htons(server_port);

    if (connect(sockfd, (const struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0)
        error("ERROR connecting");

    // Invia lunghezza
    n = write(sockfd, &len_be, sizeof(uint16_t));
    if (n < 0) error("ERROR writing length to socket");

    // Invia stringa
    n = write(sockfd, str, len);
    if (n < 0) error("ERROR writing string to socket");

    // Ricevi lunghezza risposta
    n = read(sockfd, &recv_len, sizeof(uint16_t));
    if (n < 0) error("ERROR reading length from socket");
    recv_len = ntohs(recv_len);

    // Ricevi stringa
    bzero(buffer, sizeof(buffer));
    n = read(sockfd, buffer, recv_len);
    if (n < 0) error("ERROR reading string from socket");

    buffer[recv_len] = '\0'; // assicurare terminazione

    printf("Server replied: \"%s\"\n", buffer);

    close(sockfd);
    return 1;
}

int main() {
    const char *tests[] = {
        "ciao mondo",
        "Prova",
        "stringa con numeri 123!",
        "utf8: àèìòù"
    };
    int ntests = sizeof(tests) / sizeof(tests[0]);

    for (int i = 0; i < ntests; i++) {
        send_string(tests[i]);
    }

    return 0;
}
