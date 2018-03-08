#include "HX711.h"
#include <Servo.h>


#define calibration_factor_1 -18740.0//This value is how to calibrate scales
#define calibration_factor_2 -19600.0
#define calibration_factor_3 -19520.0 //?????
#define calibration_factor_4 -19650.00 //?????

#define DAT1  2 //DAT Pin on HX711
#define CLK1  3 //CLK Pin on HX711
#define DAT2  6 
#define CLK2  5
#define DAT3  8
#define CLK3  7
#define DAT4  10
#define CLK4  9
#define OVR  12
#define LCK  13


// If it's false, it'll only show lock/unlock messages
#define COLLECT_DATA false

// If we do enable this, it might mess up our classification
#define ENABLE_THIRD_SENSOR false

Servo myservo;  // create servo object to control a servo

HX711 scale1(DAT1, CLK1);
HX711 scale2(DAT2, CLK2);
HX711 scale3(DAT3, CLK3);
HX711 scale4(DAT4, CLK4);

int num_sensors = 4;
int num_cent = 3;
int lastClass = -1;
boolean override = false;

 
float cen[][4] = {{ 0.0, 0.0, 0.0, 0.0},{ 0.0263620387, 0.0957820738,  0.0466559266,  0.869210115 }, {0.292228095, 0.315707749, 0.0502654492 , 0.342342627 }};

float recent_avg_total = 0;

int curr_state = -1; // 0 = unlock, 1 = lock

 
void setup() {


  Serial.begin(9600);
  
 
  scale1.set_scale(calibration_factor_1);
  scale2.set_scale(calibration_factor_2);
  scale3.set_scale(calibration_factor_3);
  scale4.set_scale(calibration_factor_4);
  
  scale1.tare(); //reset the scale to 0
  scale2.tare(); //reset the scale to 0
  scale3.tare(); //reset the scale to 0
  scale4.tare(); //reset the scale to 0

}

float euc_dist(float a[], float b[]) {
  float run_tot = 0;
  for (int i = 0; i < num_sensors; i++) {
    run_tot += sq((a[i] - b[i]));
  }

  return sqrt(run_tot);
}

int classify(float input[]) {
  int lowestClass = 0;
  float lowestDist = 100000.0;
  
  for (int classifier = 0; classifier < num_cent; classifier++) {
    float dist = euc_dist(input, cen[classifier]);
    if (dist < lowestDist) {
      lowestDist = dist;
      lowestClass = classifier;
    }
  }
  
  return lowestClass;
}

int pos = 0; 

void loop() {
  
  float scale1_val = 0.00;
  float scale2_val = 0.00;
  float scale3_val = 0.00;
  float scale4_val = 0.00;

  float scale1_perc = 0.00;
  float scale2_perc = 0.00;
  float scale3_perc = 0.00;
  float scale4_perc = 0.00;

  float total = 0.00;

  scale1_val = abs(scale1.get_units()), 1;
  scale2_val = abs(scale2.get_units()), 1;
  scale3_val = 0;

  if (ENABLE_THIRD_SENSOR) {
    scale3_val = abs(scale3.get_units()), 1;  
  }

  scale4_val = abs(scale4.get_units()), 1;

  total = (scale1_val + scale2_val + scale3_val + scale4_val);


  if (scale1_val < 1.5) {
    scale1_val = 0;
  }

   if (scale2_val < 1.5) {
    scale2_val = 0;
  }

   if (scale3_val < 1.5) {
    scale3_val = 0;
  }

   if (scale4_val < 1.5) {
    scale4_val = 0;
  }

  int over_int = digitalRead(OVR);
  override = true ? over_int == 1 : override;
  
   if (COLLECT_DATA) {
    Serial.print(scale1_val, 1);    Serial.print(",");
    Serial.print(scale2_val, 1);    Serial.print(",");
    Serial.print(scale3_val, 1);    Serial.print(",");
    Serial.print(scale4_val, 1);    Serial.print(",");
    Serial.println(scale1_val + scale2_val + scale3_val + scale4_val, 1);
  }
  
  scale1_perc = scale1_val/total;
  scale2_perc = scale2_val/total;
  scale3_perc = scale3_val/total;
  scale4_perc = scale4_val/total;

  float scales[] = {scale1_perc, scale2_perc, scale3_perc, scale4_perc};

  int currClass = classify(scales);

  if (override) {
    if (!COLLECT_DATA) Serial.println("Override Lock");
    digitalWrite(LCK, LOW);
  }

  if (curr_state != 1 && (currClass == 1 || currClass == 0) && lastClass != 0) {
    
    if (total / recent_avg_total < 0.7) {
      if (!COLLECT_DATA) Serial.println("Lock");
      digitalWrite(LCK, LOW);  
      curr_state = 1;
    }
  } else if (curr_state != 0 && lastClass != 2 && currClass != 0) {

    if (recent_avg_total / total < 0.7) {
        delay(250);
        if (!COLLECT_DATA) Serial.println("Unlock");
        digitalWrite(LCK, HIGH);  
        curr_state = 0;
    }
    

  }
  
  recent_avg_total = total;
  
  lastClass = currClass;


}
