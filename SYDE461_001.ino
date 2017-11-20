#include "HX711.h"
#include <Servo.h>


#define calibration_factor_1 -5060.0//This value is how to calibrate scales
#define calibration_factor_2 -6130.0
#define calibration_factor_3 -7000.0 //?????

#define DAT1  2 //DAT Pin on HX711
#define CLK1  3 //CLK Pin on HX711
#define DAT2  4 
#define CLK2  5
#define DAT3  6
#define CLK3  7

Servo myservo;  // create servo object to control a servo

HX711 scale1(DAT1, CLK1);
HX711 scale2(DAT2, CLK2);
HX711 scale3(DAT3, CLK3);

void setup() {

  Serial.begin(9600);

  myservo.attach(9);

  scale1.set_scale(calibration_factor_1);
  scale2.set_scale(calibration_factor_2);
  scale3.set_scale(calibration_factor_2);
  scale1.tare(); //reset the scale to 0
  scale2.tare(); //reset the scale to 0
  scale3.tare(); //reset the scale to 0

}

int pos = 0; 

void loop() {
  
  float scale1_val = 0.00;
  float scale2_val = 0.00;
  float scale3_val = 0.00;
  
  scale1_val = abs(scale1.get_units()), 1;
  Serial.print(scale1_val, 1); //scale.get_units() returns a float
  
  Serial.print(",");
  scale2_val = abs(scale2.get_units()), 1;
  Serial.print(scale2_val, 1); //scale.get_units() returns a float
   
  Serial.print(",");
  scale3_val = abs(scale3.get_units()), 1;
  Serial.print(scale3_val, 1); //scale.get_units() returns a float

  if(scale1_val + scale2_val + scale3_val <= 5 && pos == 0){
      for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
      // in steps of 1 degree
      myservo.write(pos);              // tell servo to go to position in variable 'pos'
      delay(15); 
      }
      pos = 180;
    }

   if(scale1_val + scale2_val + scale3_val >= 5 && pos == 180){
        for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
        myservo.write(pos);              // tell servo to go to position in variable 'pos'
        delay(15);                       // waits 15ms for the servo to reach the position
        }// waits 15ms for the servo to reach the position
        pos = 0;
      
  }
  delay(2000);
}

