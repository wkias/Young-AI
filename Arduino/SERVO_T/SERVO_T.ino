#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver rPWM = Adafruit_PWMServoDriver(0x40);
Adafruit_PWMServoDriver lPWM = Adafruit_PWMServoDriver(0x41);

#define SERVOMAX  255
#define SERVOMID  307
#define SERVOMIN  359
#define SERVO_FREQ 50

void setup() {

  rPWM.begin();
  rPWM.setPWMFreq(SERVO_FREQ);
  lPWM.begin();
  lPWM.setPWMFreq(SERVO_FREQ);

  iP();

}

void loop() {
//  initPosition();
  iP();
}

void initPosition() {
  
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      rPWM.setPWM(3 * i + j, 0, SERVOMIN);
      delay(500);
      lPWM.setPWM(3 * i + j, 0, SERVOMIN);
      delay(500);
    }
  }
  
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      rPWM.setPWM(3 * i + j, 0, SERVOMID);
      delay(500);
      lPWM.setPWM(3 * i + j, 0, SERVOMID);
      delay(500);
    }
  }
  
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      rPWM.setPWM(3 * i + j, 0, SERVOMAX);
      delay(500);
      lPWM.setPWM(3 * i + j, 0, SERVOMAX);
      delay(500);
    }
  }
  
}

void iP() {
  
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      rPWM.setPWM(3 * i + j, 0, SERVOMID);
      delay(500);
      lPWM.setPWM(3 * i + j, 0, SERVOMID);  
      delay(500);
    }
  }
  
}
