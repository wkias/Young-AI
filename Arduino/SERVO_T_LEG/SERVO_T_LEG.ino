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

#define SERVOMIN  255
#define SERVOMID  307
#define SERVOMAX  359
#define SERVO_FREQ 50

void setup() {

  rPWM.begin();
  rPWM.setPWMFreq(SERVO_FREQ);
  lPWM.begin();
  lPWM.setPWMFreq(SERVO_FREQ);

}

void loop() {
  initPosition();
}

void initPosition() {

  rPWM.setPWM(0, 0, SERVOMID);
  rPWM.setPWM(1, 0, SERVOMID);
  rPWM.setPWM(2, 0, SERVOMID);
//  for (int i = 0; i < 3; i++) {
//    for (int j = 0; j < 3; j++) {
//      rPWM.setPWM(3 * i + j, 0, SERVOMIN);
//      delay(500);
//    }
//  }
//  
//  for (int i = 0; i < 3; i++) {
//    for (int j = 0; j < 3; j++) {
//      rPWM.setPWM(3 * i + j, 0, SERVOMID);
//      delay(500);
//    }
//  }
//  
//  for (int i = 0; i < 3; i++) {
//    for (int j = 0; j < 3; j++) {
//      rPWM.setPWM(3 * i + j, 0, SERVOMAX);
//      delay(500);
//    }
//  }
  
}
