/*
 * BinClock.c
 * Jarrod Olivier
 * Modified by Keegan Crankshaw
 * Further Modified By: Mark Njoroge 
 *
 * 
 * <STUDNUM_1> <STUDNUM_2>
 * Date
*/

#include <signal.h> //for catching signals
#include <wiringPi.h>
#include <wiringPiI2C.h>
#include <stdio.h> //For printf functions
#include <stdlib.h> // For system functions

#include "BinClock.h"
#include "CurrentTime.h"

#define HOUR_BUTTON 17
#define MINUTE_BUTTON 27
#define RED_LED 16

//Global variables
int hours, mins, secs;
long lastInterruptTime = 0; //Used for button debounce
int RTC; //Holds the RTC instance

int HH,MM,SS;


// Clean up function to avoid damaging used pins

void changeHours(){
        if(hours<23){
                hours++;
        }
        else{
                hours = 0x00;
                mins = 0x00;
        }
        wiringPiI2CWriteReg8 (RTC, HOUR_REGISTER, hours) ;
}
void changeMins(){
        if(mins<59){
                mins++;
        }
        else{
                mins = 0;
                changeHours();
        }
        wiringPiI2CWriteReg8 (RTC, MIN_REGISTER, mins) ;
}
void CleanUp(int sig){
	printf("Cleaning up\n");
	
	//Set LED to low then input mode
	//Logic here
	digitalWrite(RED_LED,LOW);
	pinMode(RED_LED, INPUT);
	pinMode(HOUR_BUTTON,INPUT);
	pinMode(MINUTE_BUTTON,INPUT);
	pullUpDnControl(HOUR_BUTTON, PUD_DOWN);
	pullUpDnControl(MINUTE_BUTTON, PUD_DOWN);

	// for (int j=0; j < sizeof(BTNS)/sizeof(BTNS[0]); j++) {
	// 	pinMode(BTNS[j],INPUT);
	// }

	exit(0);

}

void initGPIO(void){
	/* 
	 * Sets GPIO using wiringPi pins. see pinout.xyz for specific wiringPi pins
	 * You can also use "gpio readall" in the command line to get the pins
	 * Note: wiringPi does not use GPIO or board pin numbers (unless specifically set to that mode)
	 */
	printf("Setting up\n");
	wiringPiSetupGpio(); //This is the BCM mode.
	

	RTC = wiringPiI2CSetup(RTCAddr); //Set up the RTC
	
	//Set up the LED
	//Write your Logic here
	pinMode(RED_LED, OUTPUT);
	digitalWrite(RED_LED, LOW);

	printf("LED and RTC done\n");
	
	//Set up the Buttons
	
	pinMode(HOUR_BUTTON,INPUT);
	pinMode(MINUTE_BUTTON,INPUT);
	pullUpDnControl(HOUR_BUTTON, PUD_UP);
	pullUpDnControl(MINUTE_BUTTON, PUD_UP);
	//Attach interrupts to Buttons
	//Write your logic here
	wiringPiISR(HOUR_BUTTON, INT_EDGE_BOTH, hourInc);
	wiringPiISR(MINUTE_BUTTON, INT_EDGE_BOTH, minInc);

	printf("BTNS done\n");
	printf("Setup done\n");
}


/*
 * The main function
 * This function is called, and calls all relevant functions we've written
 */
int main(void){
	signal(SIGINT,CleanUp);
	initGPIO();

	//Set random time (3:04PM)
	//You can comment this file out later
	wiringPiI2CWriteReg8(RTC, HOUR_REGISTER, 0x13+TIMEZONE);
	wiringPiI2CWriteReg8(RTC, MIN_REGISTER, 0x4);
	wiringPiI2CWriteReg8(RTC, SEC_REGISTER, 0x00);
	
	// Repeat this until we shut down
	for (;;){
		//Fetch the time from the RTC
		//Write your logic here
		wiringPiI2CReadReg8(hours, HOUR_REGISTER) ;
		wiringPiI2CReadReg8(mins, MIN_REGISTER) ;
		wiringPiI2CReadReg8(secs, SEC_REGISTER) ;
		
		//Toggle Seconds LED
		//Write your logic here
		if(digitalRead(RED_LED)){
			digitalWrite(RED_LED,LOW);
		}
		else{
			digitalWrite(RED_LED,HIGH);
		}
		
		// Print out the time we have stored on our RTC
		printf("The current time is: %02d:%02d:%02d\n", hours, mins, secs);

		//using a delay to make our program "less CPU hungry"
		delay(1000); //milliseconds
		if(secs<59){
                        secs++;
        }
        else{
                        secs = 0x00;
                        changeMins();
        }
        wiringPiI2CWriteReg8(RTC, SEC_REGISTER, secs);
	}
	return 0;
}

/*
 * Changes the hour format to 12 hours
 */
int hFormat(int hours){
	/*formats to 12h*/
	if (hours >= 24){
		hours = 0;
	}
	else if (hours > 12){
		hours -= 12;
	}
	return (int)hours;
}


/*
 * hexCompensation
 * This function may not be necessary if you use bit-shifting rather than decimal checking for writing out time values
 * Convert HEX or BCD value to DEC where 0x45 == 0d45 	
 */
int hexCompensation(int units){

	int unitsU = units%0x10;

	if (units >= 0x50){
		units = 50 + unitsU;
	}
	else if (units >= 0x40){
		units = 40 + unitsU;
	}
	else if (units >= 0x30){
		units = 30 + unitsU;
	}
	else if (units >= 0x20){
		units = 20 + unitsU;
	}
	else if (units >= 0x10){
		units = 10 + unitsU;
	}
	return units;
}


/*
 * decCompensation
 * This function "undoes" hexCompensation in order to write the correct base 16 value through I2C
 */
int decCompensation(int units){
	int unitsU = units%10;

	if (units >= 50){
		units = 0x50 + unitsU;
	}
	else if (units >= 40){
		units = 0x40 + unitsU;
	}
	else if (units >= 30){
		units = 0x30 + unitsU;
	}
	else if (units >= 20){
		units = 0x20 + unitsU;
	}
	else if (units >= 10){
		units = 0x10 + unitsU;
	}
	return units;
}


/*
 * hourInc
 * Fetch the hour value off the RTC, increase it by 1, and write back
 * Be sure to cater for there only being 23 hours in a day
 * Software Debouncing should be used
 */
void hourInc(void){
        //Debounce
        long interruptTime = millis();

        if (interruptTime - lastInterruptTime>200){
                printf("Interrupt 1 triggered, %d\n", hours);
                //Fetch RTC Time
                if(hours<23){
                        wiringPiI2CWriteReg8(RTC, HOUR_REGISTER,++hours) ;
                }
                else{
                        hours = 0;
                        wiringPiI2CWriteReg8(RTC, HOUR_REGISTER,hours);
                }
                //printf("Interrupt 1 ending, %x\n", hours);
                //Increase hours by 1, ensuring not to overflow
                //Write hours back to the RTC
        }
        lastInterruptTime = interruptTime;
}

/* 
 * minInc
 * Fetch the minute value off the RTC, increase it by 1, and write back
 * Be sure to cater for there only being 60 minutes in an hour
 * Software Debouncing should be used
 */
void minInc(void){
        long interruptTime = millis();

        if (interruptTime - lastInterruptTime>200){
                printf("Interrupt 2 triggered, %d\n", mins);
                if(mins<59){
                        mins++ ;
                }
                else{
                        mins =0;
                        changeHours();
                }
                wiringPiI2CWriteReg8(RTC, MIN_REGISTER,mins);
                //Fetch RTC Time
                //Increase minutes by 1, ensuring not to overflow
                //Write minutes back to the RTC
        }
        lastInterruptTime = interruptTime;
}

//This interrupt will fetch current time from another script and write it to the clock registers
//This functions will toggle a flag that is checked in main
void toggleTime(void){
	long interruptTime = millis();

	if (interruptTime - lastInterruptTime>200){
		HH = getHours();
		MM = getMins();
		SS = getSecs();

		HH = hFormat(HH);
		HH = decCompensation(HH);
		wiringPiI2CWriteReg8(RTC, HOUR_REGISTER, HH);

		MM = decCompensation(MM);
		wiringPiI2CWriteReg8(RTC, MIN_REGISTER, MM);

		SS = decCompensation(SS);
		wiringPiI2CWriteReg8(RTC, SEC_REGISTER, 0b10000000+SS);

	}
	lastInterruptTime = interruptTime;
}
