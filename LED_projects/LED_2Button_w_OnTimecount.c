#include <stdio.h>
#include <pigpio.h>
int i = 0;
unsigned int gpio = 18;

int current_time=0, prev_time=0;

int main(void) {
    gpioInitialise();

    printf("Set\n");
    gpioSetMode(18, PI_INPUT);
 audo
 
 
     gpioSleep(PI_TIME_RELATIVE, 0, 100000);  // sleep for 100,000us, 100ms, 0.1s

    int secs, mics;
    
    if ((gpioGetMode(2) != PI_OUTPUT) | (gpioGetMode(18) != PI_INPUT)) {  // check for wrong I/O mode
        printf("Wrong PIN Mode on Pin 2 or 18\n");
    }
    else {
        printf("Started\n");
//      gpioSetISRFunc(gpio, state, a, f);  // I think I tried to insert an interrupt
        while (1) {
            current_time = 0;

            if (gpioRead(18)) {  // if 1
                gpioWrite(2, 0);
            }   
            else {
                printf("Button Input detected\n");
                gpioWrite(2, 1);
                int i = 1;
                
                while (gpioRead(18) == 0) {       //gpioTime(0, &secs, &mics);   //first parameter is PI_TIME_RELATIVE, 0 means PI_TIME_RELATIVE
                    //printf("Current time is %dseconds, %dmicroseconds\n", secs, mics);
                      // current time in mics'';;
                    //Current time = gpioTime
                    
                    if (current_time - prev_time > 1000000) {
                        if (prev_time != 0){
                            printf("%ds has elapsed\n", i);
                            i++;
                        }
                        prev_time = current_time;
                    }
                    gpioTime(0, &secs, &mics);
                    current_time = secs*1000000 + mics;
                }
                prev_time = 0;
                printf("Looks like button is released\n\n");
            }
        }
    }

    gpioTerminate();
    return 0;
}

// I think the code below is... to add an interrupt through register but idk how to do that yet. I'll learn tomorrow.
//int gpioSetISRFunc(gpio, state, a, f);

// typedef void (*f) {
//     (gpio, 1, uint32_t tick);
// }   
//   printf("stopped");

//(if current_time - previous_time > 1,000,000us){
    //previous_time = current_time
