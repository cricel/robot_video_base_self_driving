#include "Arduino.h"
#include "SDR_SUGV.h"
#include "Protocol.h"
#include "Localization.h"
#include "Sensing.h"
#include "Action.h"

int stopFlag = 0;
int autoFlag = -1;   // Auto or Manual Control

unsigned long sonarClock = 0;
unsigned long lineClock = 0;
unsigned long odometerClock = 0;
unsigned long currentMillis = 0;
unsigned long previousMillis = 0;
long cnt =9;
long cnt2 = 9;

void setup() {
  // put your setup code here, to run once:
  initialization();
}


void loop() {
  currentMillis = millis();
  if ((cnt++ % 1000) ==0){
    Serial.println(cnt);
  }
  updateCommand();
  updateSensors();  
  updatePlan();
  updateAction();
  previousMillis = currentMillis;  
}

void updatePlan(){
  autoFlag = 1;
  if (autoFlag == 1){ //Auto-driving    
  if((lineR == 0)  && (lineL == 0)){
    speedR = 245; speedL = 245;
  } else if((lineR == 1)  && (lineL == 0)){
    speedR = -245; speedL = 245;
  } else if((lineR == 0)  && (lineL == 1)){
    speedR = 245; speedL = -245;
  } else{
    speedR = -245; speedL = -245;
  }
  
  }else if (autoFlag == 0){
  }else{
  }
  
  
  if (stopFlag == 1 ){
    speedR = 0; speedL = 0;
  }

}

void updateAction(){

  updateMotor();
}



void updateSensors(){
    if ((cnt++ % 1000) ==0){
    sonar = updateSonar();
    sonar2 = updateSonar2();
    //Serial.print("Front Sonar: ");
    //Serial.println(sonar);
    //Serial.print("Back Sonar: ");
    //Serial.println(sonar2);
  }
  
 // Serial.print(lineR);
 // Serial.print("   ");
 // Serial.println();
 // Serial.print(lineL);
 // Serial.print("   ");
 // Serial.println();
  if((sonar < 7 && sonar != 0) || (sonar2 < 7 && sonar2 != 0)){
  stopFlag = 1;
  }
  else if(sonar > 7 || sonar2 > 7){
   stopFlag = 0;
  }
/*  
  if(lineR == 1 || lineL == 1){
      rotate();
  }
  else{
    speedR = 255; speedL = 255;
  }
  */
}
/*
void rotate(){
   if(lineR == 1 && lineL == 0){
   
       speedL = -255;
       speedR = 255;
   
   }
   else if(lineL == 1 && lineR == 0){
     speedR = -255;
     speedL = 255;
   }
  
}

*/

void initialization(){
  currentMillis = millis();
  init_communication();
  init_pin();
  
}

void init_communication(){
  Serial.begin(115200); Serial.println("Program Start...v04");
  init_buffer(); 
}

void init_pin(){
  //Motor pin setting
  pinMode(MOTOR_LEFT_ENABLE, OUTPUT); pinMode(MOTOR_LEFT_A, OUTPUT); pinMode(MOTOR_LEFT_B, OUTPUT);
  pinMode(MOTOR_RIGHT_ENABLE, OUTPUT); pinMode(MOTOR_RIGHT_A, OUTPUT); pinMode(MOTOR_RIGHT_B, OUTPUT);
  //Sonar pin setting
  pinMode(SONAR_ECHO, INPUT); pinMode(SONAR_TRIG, OUTPUT);
  pinMode(SONAR_ECHO2, INPUT); pinMode(SONAR_TRIG2, OUTPUT);
  //pinMode(LINE_LEFT, INPUT_PULLUP); pinMode(LINE_RIGHT, INPUT_PULLUP); 
  attachInterrupt(0, rightOdometer, CHANGE);
  attachInterrupt(1, leftOdometer, CHANGE);
}



