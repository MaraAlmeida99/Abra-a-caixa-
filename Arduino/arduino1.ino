#include <Key.h>
#include <Keypad.h>
#include <Servo.h> 

//sudo chmod a+rw /dev/ttyACM0

const byte ROWS = 4;
const byte COLS = 4;

char hexaKeys[ROWS][COLS] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'},
};

String input = ""; //keypad input

byte rowPins[ROWS] = {9,8,7,6};
byte colPins[COLS] = {5,4,3,2};

Keypad customKeypad = Keypad(makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS);


const int analogInPin1 = A0; // Analog input pin that the Joystick's firstpin is attached to (x)
const int analogInPin2 = A1; // Analog input pin that the Joystick's second pin is attached to (y)

int sensorValue1 = 0; //value read from analogInPin1 (x)
int sensorValue2 = 0; //value read from analogInPin2 (y)
int outputValue1 = 0; //x mapped value
int outputValue2 = 0; //y mapped value


String prev = "0"; //joystick previous position
String seq = ""; //full input from joystick
String pos = ""; //current joystick position

int servoPin = 11;
Servo Servo1; 

void setup() {
  Serial.begin(9600); // initialize serial communications at 9600 bps:
  Servo1.attach(servoPin);
  Servo1.write(115); //set start servo motor start position to close
}

void loop() {
/*
 * 
 *  KeyPad
 * 
 */
    char customKey = customKeypad.getKey(); //read input from keypad
  
    if (customKey == '*'){ //delete last key input
      if ( input.length() > 0 )
        input.remove(input.length()-1,1);
    }
    else if ( customKey == 'C' ){ //close the box
      Serial.println("CLOSE");
      Servo1.write(115);
      prev = "0";
      input = "";
    }
    else if (customKey && customKey != '#'){ //key input received
      input = String(input + customKey);
    }
    else if ( customKey == '#' ){ //input submited to raspberry
      Serial.println("KEYPAD " + input);
      input = "";
    }


  /*
   * 
   *  JOYSTICK
   * 
   */
// read the both analog in values:


    sensorValue1 = analogRead(analogInPin1); //read x
    sensorValue2 = analogRead(analogInPin2); //read y
  
  // map it to the range of the analog out:
    outputValue1 = map(sensorValue1, 0, 1023, 0, 255);
    outputValue2 = map(sensorValue2, 0, 1023, 0, 255);
  
    /*
     * centro X ( 115-140   ) Y ( 115-125 )
     * cima X ( 0 - 30 ) Y ( 2 - 200 )
     * baixo X ( 200 - 230 ) Y ( 2 - 220 )
     * esquerda ( 30 - 200 ) Y (2)
     * direita ( 30 - 200 ) Y (>200)
     */
    if ( ( outputValue1 >= 115 && outputValue1 < 140 ) && ( outputValue2 >= 115 && outputValue2 < 125 ) ){ //joystick centered
      pos = "0";
      if ( prev != pos ){ //if joystick changed position to center, submit input to raspberry
        Serial.println("JOYSTICK " + seq);
        seq = "";
        prev = "0";
      }
    }
    else if ( ( outputValue1 >= 0 && outputValue1 < 30 ) && ( outputValue2 >= 2 && outputValue2 < 220 ) ) //joystick is up
      pos = "U";
    else if ( ( outputValue1 >= 200 && outputValue1 < 230 ) && ( outputValue2 >= 2 && outputValue2 < 220 ) ) //joystick is down
      pos = "D";
    else if ( ( outputValue1 >= 40 && outputValue1 < 190 ) && ( outputValue2 <= 4 ) ) //joystick is left
      pos = "L";
    else if ( ( outputValue1 >= 40 && outputValue1 < 190 ) && ( outputValue2 >= 200 ) ) //joystick is right
      pos = "R";
    if ( pos != prev ){ //position changed, new input
        seq = seq + pos;
        prev = pos;
    }

    if (Serial.available() > 0){ //read instructions from raspberry
      String raspberry = Serial.readString();
      if ( raspberry == "RASPBERRY OPEN\n" ){
        Servo1.write(20);
        prev = "0";
      }
      else if ( raspberry == "RASPBERRY CLOSE\n" ){
        Servo1.write(115);
        prev = "0";
      }
    }  
}
