/*
   Hexapod

   Copyleft 2019 Willice @ SDNU Young AI Robit

*/

/***********************************************************************
             DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                     Version 2, December 2004
*                                                                      *
  Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
*                                                                      *
  Everyone is permitted to copy and distribute verbatim or modified
  copies of this license document, and changing it is allowed as long
  as the name is changed.
*                                                                      *
             DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
    TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
*                                                                      *
   0. You just DO WHAT THE FUCK YOU WANT TO.
*                                                                      *
***********************************************************************/

#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver rPWM = Adafruit_PWMServoDriver(0x40);
Adafruit_PWMServoDriver lPWM = Adafruit_PWMServoDriver(0x41);

#define SERVOMAX  255
#define SERVOMID  307
#define SERVOMIN  359
#define SERVO_FREQ 50 //in Hz

#define TRIG 22 //pin,beneth too.
#define ECHO 24
#define DISTANCE_LIMIT 50 //in cm

#define WAIT_TIME 400 //in ms

long dist;
int i,j; //for loop, no other function

void setup() {

  Serial.begin(9600);

  rPWM.begin();
  rPWM.setPWMFreq(SERVO_FREQ);
  lPWM.begin();
  lPWM.setPWMFreq(SERVO_FREQ);

  initPosition();

}

void loop() {
    if (distance() > 50) {
      forward();
    } else {
      backward();
      if (random() % 2) {
        left();
      } else {
        right();
      }
    }
}

void initPosition() {
  for (i = 0; i < 3; i++) {
    for (j = 0; j < 3; j++) {
      rPWM.setPWM(3 * i + j, 0, SERVOMID);
      delay(WAIT_TIME);
      lPWM.setPWM(3 * i + j, 0, SERVOMID);
      delay(WAIT_TIME);
    }
  }
}

void forward() {

  for(i=0;i<3;i++){
    rPWM.setPWM(i, 0, SERVOMAX);
    lPWM.setPWM(i, 0, SERVOMAX);
  }
  
  rPWM.setPWM(3, 0, SERVOMAX);
  lPWM.setPWM(4, 0, SERVOMIN);
  rPWM.setPWM(5, 0, SERVOMAX);
  delay(WAIT_TIME);

  rPWM.setPWM(0, 0, SERVOMAX);
  rPWM.setPWM(1, 0, SERVOMAX);
  rPWM.setPWM(2, 0, SERVOMAX);
  lPWM.setPWM(0, 0, SERVOMIN);
  lPWM.setPWM(1, 0, SERVOMIN);
  lPWM.setPWM(2, 0, SERVOMIN);
  delay(WAIT_TIME);

  rPWM.setPWM(3, 0, SERVOMID);
  lPWM.setPWM(4, 0, SERVOMID);
  rPWM.setPWM(5, 0, SERVOMID);
  delay(WAIT_TIME);

  lPWM.setPWM(3, 0, SERVOMIN);
  rPWM.setPWM(4, 0, SERVOMAX);
  lPWM.setPWM(5, 0, SERVOMIN);
  delay(WAIT_TIME);

  for(i=0;i<3;i++){
    rPWM.setPWM(i,0,SERVOMID);
    lPWM.setPWM(i,0,SERVOMID);
  }
  delay(WAIT_TIME);

  lPWM.setPWM(3, 0, SERVOMID);
  rPWM.setPWM(4, 0, SERVOMID);
  lPWM.setPWM(5, 0, SERVOMID);
  delay(WAIT_TIME);

}

void backward() {

  rPWM.setPWM(3, 0, SERVOMAX);
  lPWM.setPWM(4, 0, SERVOMIN);
  rPWM.setPWM(5, 0, SERVOMAX);
  delay(WAIT_TIME);

  rPWM.setPWM(0, 0, SERVOMIN);
  rPWM.setPWM(1, 0, SERVOMIN);
  rPWM.setPWM(2, 0, SERVOMIN);
  lPWM.setPWM(0, 0, SERVOMAX);
  lPWM.setPWM(1, 0, SERVOMAX);
  lPWM.setPWM(2, 0, SERVOMAX);
  delay(WAIT_TIME);

  rPWM.setPWM(3, 0, SERVOMID);
  lPWM.setPWM(4, 0, SERVOMID);
  rPWM.setPWM(5, 0, SERVOMID);
  delay(WAIT_TIME);

  lPWM.setPWM(3, 0, SERVOMIN);
  rPWM.setPWM(4, 0, SERVOMAX);
  lPWM.setPWM(5, 0, SERVOMIN);
  delay(WAIT_TIME);

  for(i=0;i<3;i++){
    rPWM.setPWM(i,0,SERVOMID);
    lPWM.setPWM(i,0,SERVOMID);
  }
  delay(WAIT_TIME);

  lPWM.setPWM(3, 0, SERVOMID);
  rPWM.setPWM(4, 0, SERVOMID);
  lPWM.setPWM(5, 0, SERVOMID);
  delay(WAIT_TIME);

}

void left() {
  
  rPWM.setPWM(3, 0, SERVOMAX);
  lPWM.setPWM(4, 0, SERVOMIN);
  rPWM.setPWM(5, 0, SERVOMAX);
  delay(WAIT_TIME);

  for(i=0;i<3;i++){
    rPWM.setPWM(i,0,SERVOMAX);
    lPWM.setPWM(i,0,SERVOMAX);
  }
  delay(WAIT_TIME);

  rPWM.setPWM(3, 0, SERVOMID);
  lPWM.setPWM(4, 0, SERVOMID);
  rPWM.setPWM(5, 0, SERVOMID);
  delay(WAIT_TIME);

  lPWM.setPWM(3, 0, SERVOMIN);
  rPWM.setPWM(4, 0, SERVOMAX);
  lPWM.setPWM(5, 0, SERVOMIN);
  delay(WAIT_TIME);

  for(i=0;i<3;i++){
    rPWM.setPWM(i,0,SERVOMID);
    lPWM.setPWM(i,0,SERVOMID);
  }
  delay(WAIT_TIME);


  lPWM.setPWM(3, 0, SERVOMID);
  rPWM.setPWM(4, 0, SERVOMID);
  lPWM.setPWM(5, 0, SERVOMID);
  delay(WAIT_TIME);
  
}

void right() {
  rPWM.setPWM(3, 0, SERVOMAX);
  lPWM.setPWM(4, 0, SERVOMIN);
  rPWM.setPWM(5, 0, SERVOMAX);
  delay(WAIT_TIME);

  for(i=0;i<3;i++){
    rPWM.setPWM(i,0,SERVOMIN);
    lPWM.setPWM(i,0,SERVOMIN);
  }
  delay(WAIT_TIME);

  rPWM.setPWM(3, 0, SERVOMID);
  lPWM.setPWM(4, 0, SERVOMID);
  rPWM.setPWM(5, 0, SERVOMID);
  delay(WAIT_TIME);

  lPWM.setPWM(3, 0, SERVOMIN);
  rPWM.setPWM(4, 0, SERVOMAX);
  lPWM.setPWM(5, 0, SERVOMIN);
  delay(WAIT_TIME);

  for(i=0;i<3;i++){
    rPWM.setPWM(i,0,SERVOMID);
    lPWM.setPWM(i,0,SERVOMID);
  }
  delay(WAIT_TIME);

  lPWM.setPWM(3, 0, SERVOMID);
  rPWM.setPWM(4, 0, SERVOMID);
  lPWM.setPWM(5, 0, SERVOMID);
  delay(WAIT_TIME);
}

long distance() {

  pinMode(TRIG, OUTPUT);
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(5);
  digitalWrite(TRIG, LOW);

  pinMode(ECHO, INPUT);
  dist = (double)pulseIn(ECHO, HIGH) * 0.017;

  Serial.print(dist);
  Serial.write("cm\n");

  return dist;

}
