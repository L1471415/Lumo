#include "pico/stdlib.h"
#include "hardware/adc.h"
#include <stdio.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <unistd.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/select.h>


int main() {

    //const uint input_pin = 20;
    const uint output_pin = 21;
    // note this HAS to be 26
    const uint audio_input_pin = 26; 

    //gpio_init(input_pin);
    //gpio_set_dir(input_pin, GPIO_IN);

    gpio_init(output_pin);
    gpio_set_dir(PICO_DEFAULT_LED_PIN, GPIO_OUT);

    // ok so it has to be pwm
    gpio_set_function(output_pin, GPIO_FUNC_PWM);
    uint slice_num = pwm_gpio_to_slice_num(output_pin);

    pwm_set_wrap(slice_num, 255);
    pwn_set_clkdiv(slice_num, 1.0);
    pwn_set_enabled(slice_num, true);

    // audio input setup
    adc_init();
    adc_gpio_init(audio_input_pin);
    adc_select_input(0);





    // C server Stuff

    // setup
    int sockfd, newsockfd;
    struct sockaddr_in my_addr, client_addr;
    int bufferSize = 1024;
    char buffer[bufferSize];

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
  
    memset(&my_addr, 0, sizeof(struct sockaddr_in));
    my_addr.sin_family = AF_INET;
    my_addr.sin_port = htons(9090);
    bind(sockfd, (struct sockaddr *)&my_addr, sizeof(struct sockaddr_in));
  
    // Listen for connections
    listen(sockfd, 5);
  
    // Accept a connection request
    int client_len = sizeof(client_addr);
    newsockfd = accept(sockfd, (struct sockaddr *)&client_addr, &client_len);

    while(true){
        //uint16_t raw_audioData = adc_read();

        ssize_t totalBytes = recv(sockfd, buffer, bufferSize, 0)

        if (totalBytes == 0){
            perror("uh oh")
            close(newsockfd);
            close(sockfd);
            return EXIT_FAILURE;
        }

        //unneeded... for now...
        //uint slice_num = pwm_gpio_to_slice_num(output_pin);

        // note each char of bufferneeds to be uint8_t value
        for (int i = 0; i < totalBytes; i++){
            pwm_set_gpio_level(output_pin, buffer[i]);
            sleep_us(100);
        }

        sleep_us(30);
    }

      
    close(newsockfd); 
    close(sockfd);

}