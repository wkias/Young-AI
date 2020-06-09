#include <stdlib.h>
#include <at89x51.h>
#include <intrins.h>

#define TRIG P1_7
#define ECHO P1_6

#define FORWARD 0
#define LEFT 1
#define RIGHT 2

sbit L298N_EN1 = P1^0;
sbit L298N_EN2 = P1^1;
sbit L298N_IN1 = P1^2;
sbit L298N_IN2 = P1^3;
sbit L298N_IN3 = P1^4;
sbit L298N_IN4 = P1^5;
sbit infraredF = P2^5;
sbit infraredR = P2^7;
sbit infraredL = P2^6;

bit flag = 0;
bit directionFlag = FORWARD;

unsigned int time = 0;
unsigned long dist = 0;

void delay1ms(unsigned int i)
{
	unsigned char j, k;
	do
	{
		j = 10;
		do
		{
			k = 50;
			do
			{
				_nop_();
			} while (--k);
		} while (--j);
	} while (--i);
}

void delay10us(unsigned char i)
{
	unsigned char j;
	do
	{
		j = 10;
		do
		{
			_nop_();
		} while (--j);
	} while (--i);
}

void forward()
{
	L298N_IN1 = 1;
	L298N_IN2 = 0;
	L298N_IN3 = 1;
	L298N_IN4 = 0;
}

void backward()
{
	L298N_IN1 = 0;
	L298N_IN2 = 1;
	L298N_IN3 = 0;
	L298N_IN4 = 1;
}

void turnRight()
{
	L298N_IN1 = 0;
	L298N_IN2 = 1;
	L298N_IN3 = 1;
	L298N_IN4 = 0;
}

void turnLeft()
{
	L298N_IN1 = 1;
	L298N_IN2 = 0;
	L298N_IN3 = 0;
	L298N_IN4 = 1;
}

void stop()
{
	L298N_IN1 = 0;
	L298N_IN2 = 0;
	L298N_IN3 = 0;
	L298N_IN4 = 0;
}

int random(){
	srand(dist);
	return rand();
}

void startModule()
{
	TRIG = 1;
	delay10us(2);
	TRIG = 0;
}

void timer()
{
	TR1 = 1;
	while (ECHO)
		;
	TR1 = 0;
}

void zd0() interrupt 3
{
	flag = 1;
	ECHO = 0;
}

void distance()
{
	time = TH1 * 256 + TL1;
	TH1 = 0;
	TL1 = 0;
	dist = time * 0.34;
}

void turn(){
	if (directionFlag == LEFT)
		{
			turnLeft();
		}
		else if (directionFlag == RIGHT)
		{
			turnRight();
		}
		else
		{
			if (random() % 2)
			{
				turnLeft();
				directionFlag = LEFT;
			}
			else
			{
				turnRight();
				directionFlag = RIGHT;
			}
		}
		delay1ms(400);
}

void side(){
	if(!infraredF){
		stop();
		delay1ms(50);
		backward();
		delay1ms(600);
		stop();
		delay1ms(50);
		turn();
	}
	if(infraredL&&!infraredR){
		turnRight();
		delay1ms(200);
	}
	if(!infraredL&&infraredR){
		turnLeft();
		delay1ms(200);
	} 
}

void goo()
{
	side();
	switch (dist / 100)
	{
	case 0:
	case 1:
	case 2:
		stop();
		delay1ms(50);
		backward();
		delay1ms(400);
	case 3:
	case 4:
		stop();
		delay1ms(50);
		turn();
		break;
	default:
		forward();
		directionFlag = FORWARD;
	}
}

void main()
{
	unsigned int a;
	delay1ms(5);
	TMOD = TMOD | 0x10;
	EA = 1;
	TH1 = 0;
	TL1 = 0;
	ET1 = 1;
	while (1)
	{
		ECHO = 1;
		startModule();
		for (a = 951; a > 0; a--)
		{
			if (ECHO)
			{
				timer();
				distance();
				goo();
			}
		}
	}
}
