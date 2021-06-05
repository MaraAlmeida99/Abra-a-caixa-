#include <SPI.h>
#include <Wire.h>

#include "Adafruit_STMPE610.h"

#define STMPE_CS 8 //code to initialize tft touch resistive
#define D 10 //delay between each read
#define NUMBER_INPUTS 5 //number of touches needed to submit to raspberry
#define MAX_SHORT 200 //threshold between SHORT touch and LONG touch

int nTouch = 0; //number of touches received
String seq = ""; //full input received
int time = 0; //duration of the current touch

Adafruit_STMPE610 touch = Adafruit_STMPE610(STMPE_CS);

/******************/

void setup() { 
  Serial.begin(9600);
  Serial.flush();
  pinMode(10, OUTPUT);

  if (! touch.begin()) {
    Serial.println("STMPE not found!");
    while(1);
  }
}

void loop() {
  if (touch.touched()) {
    time++;
    touch.writeRegister8(STMPE_INT_STA, 0xFF); //reset all ints
  }
  else { //touch screen no longer touched
    if ( time > 0 && time <= MAX_SHORT ){ //SHORT touch
      seq = seq + "S";
      nTouch++;
    }
    else if ( time > MAX_SHORT ){ //LONG touch
      seq = seq + "L";
      nTouch++;
    }
    if ( nTouch == NUMBER_INPUTS ){ //submits code to raspberry
      Serial.println( "TOUCHPAD " + seq );
      nTouch = 0;
      seq = "";
    }  
   time = 0;
  }
  delay(D);
}
