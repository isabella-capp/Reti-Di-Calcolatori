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

int send_temperature(unsigned char unit, float value) {
    int sockfd, n;
    struct sockaddr_in serv_addr;
    struct hostent *server;

    unsigned char recv_unit = 0;
    float result = 0;

    printf("Sending request: value=%f, unit=%s\n",
           value, (unit == 1 ? "Celsius" : "Fahrenheit"));

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

    // Invia unità
    n = write(sockfd, &unit, sizeof(unsigned char));
    if (n < 0) error("ERROR writing unit to socket");

    // Invia valore float
    n = write(sockfd, &value, sizeof(float));
    if (n < 0) error("ERROR writing value to socket");

    // Ricevi unità risposta
    n = read(sockfd, &recv_unit, sizeof(unsigned char));
    if (n < 0) error("ERROR reading unit from socket");

    // Ricevi float risposta
    n = read(sockfd, &result, sizeof(float));
    if (n < 0) error("ERROR reading result from socket");

    close(sockfd);

    printf("Server replied: value=%f, unit=%s\n\n",
           result, (recv_unit == 1 ? "Celsius" : "Fahrenheit"));

    return 1;
}

int main() {
    // Test vari
    send_temperature(1, 0.0f);     // 0°C -> 32°F
    send_temperature(1, 100.0f);   // 100°C -> 212°F
    send_temperature(2, 32.0f);    // 32°F -> 0°C
    send_temperature(2, 212.0f);   // 212°F -> 100°C
    send_temperature(1, -40.0f);   // -40°C -> -40°F

    return 0;
}
