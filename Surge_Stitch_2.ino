#include<avr/io.h>          //Header file for AVR microcontroller
#include<util/delay.h>      //Header file for delay
#define setbit(x,y)(x|=y)   //Define macro to make bit/bits high
#define clearbit(x,y)(x&=~y)  // Define macro to make bit/bits low
#define bitn(p)(0x01 <<(p))   // Define macro for bit position
#define checkbit(x,y)((x)&(y))   //Define macro to checking the bit of register
#include <LCD.h>                  //include LCD library

int c = 0;
int d = 0;
int main(void)              
{
  DDRB=0xFF;
  DDRD=0xF0; 
  //Note: a stepper motor's step is about pi/24 mm for distance since a stepper motor takes 48 steps fro fool revolution andthe diameter of axel is 2 mm             
  int currentX = 1430;         // Current position of the stepper motor in steps (range is 0 to 1436 steps)  //we start here, because stepper motor will bring the track set towards it sicne it does nto the have the ability to push it, it will jsut pull it fro mbehind
  int currentY = 0;          // Current position of the DC motor in stepper motor steps units   (range is 0 to 947 steps)
  int motorSpeed = 100;     // Speed of the DC motor (units per second)     //tr 350, 178, adn 140000 RPM                  --------- change prob  
  int duration = 0;
  while(1)
    {
      int targetX = 100;
      int targetY = 900;
      
      deltaX = currentX - targetX
      if (deltaX < 0)
        {
          for(int i=0; i<abs(deltaX); i++)
          {
            c++;
            antistepper();
            _delay_ms(50);
          }
        }
      else
        {
          for(int i=0; i<deltaX; i++)
          {
            d++;
            clkstepper();
            _delay_ms(50);
          }
        }
    
      deltaY = currentY - targetY
      duration = abs(deltaY) / motorSpeed * 1000;  // Convert to milliseconds
      if (deltaY < 0) 
      {
        PORTB = 0x40;        //PB7 is LOW. PB6 is HIGH. Anticlockwise. Downward Y-movement
      } 
      else 
      {
        PORTB = 0x80;       //PB7 is HIGH. PB6 is LOW. Clockwise. Upward Y-movement
      }
      _delay_ms(duration);  // Move for the calculated duration
      // Stop the DC motor
      PORTB = 0x00;     //PB7,6 are LOW. No movement

      //Relay control for solenoid
      PORTB = 0x20;        //PB5(relay) is HIGH meaning Solenoid Extends
      _delay_ms(50);
      PORTB = 0x00;        //PB5(relay) is LOW meaning Solenoid Retracts
    }
}

void antistepper()
  {
    if (c==1)
        {
          PORTD=0xE0;
        }
    if (c==2)
        {
          PORTD=0xD0;
        }
    if (c==3)
        {
          PORTD=0xB0;
        }
    if (c==4)
        {
          PORTD=0x70;
          c=0;
        }
  }

void clkstepper()
  {
    if (d==1)
        {
          PORTD=0x70;
        }
    if (d==2)
        {
          PORTD=0xB0;
        }
    if (d==3)
        {
          PORTD=0xD0;
        }
    if (d==4)
        {
          PORTD=0xE0;
          d=0;
        }
  }
