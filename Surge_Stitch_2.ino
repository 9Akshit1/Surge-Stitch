#include<avr/io.h>          //Header file for AVR microcontroller
#include<util/delay.h>      //Header file for delay
#define setbit(x,y)(x|=y)   //Define macro to make bit/bits high
#define clearbit(x,y)(x&=~y)  // Define macro to make bit/bits low
#define bitn(p)(0x01 <<(p))   // Define macro for bit position
#define checkbit(x,y)((x)&(y))   //Define macro to checking the bit of register
#include <LCD.h>                  //include LCD library

int main(void)              
{
  DDRB=0xF0;
  DDRD=0xF0; 
  int currentX = 255;         // Current position of the GEAR motor in mm (the stage is all the way to the right)
  int currentY = 0;          // Current position of the DC motor in mm (this motor is at the bottom of its axis) (170 mm is full upwards)
  int motorSpeed1 = 10;     // Speed of the DC GEAR motor (units per second)     //tr 10, 350, 178, adn 140000 RPM                  --------- change prob  
  int motorSpeed2 = 100;     // Speed of the DC motor (units per second)     //tr 350, 178, adn 140000 RPM                  --------- change prob  
  int deltaX, deltaY, duration = 0;
  while(1)
    {
      int targetX = 0;    //full left
      int targetY = 170;  //full up
      
      deltaX = currentX - targetX;   //We will normally go from right to left (essentially pulling the stage towards motor)
      duration = abs(deltaX) / motorSpeed1 * 1000;  // Convert to milliseconds
      if (deltaX > 0) 
      {
        PORTD = 0x40;        //PD7 is LOW. PD6 is HIGH. Anticlockwise. Leftward X-movement
      } 
      else 
      {
        PORTD = 0x80;       //PD7 is HIGH. PD6 is LOW. Clockwise. Rightward X-movement
      }
      _delay_ms(duration);  // Move for the calculated duration
      // Stop the DC GEAR motor
      PORTD = 0x00;     //PD7,6 are LOW. Stop motors, hopefully no inertia.
    
      deltaY = currentY - targetY;   //We will go up and down depending on the borders of the wound
      duration = abs(deltaY) / motorSpeed2 * 1000;  // Convert to milliseconds
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
      PORTB = 0x00;     //PB7,6 are LOW. Stop motors, hopefully no inertia.

      //Relay control for solenoid
      PORTB = 0x20;        //PB5(relay) is HIGH meaning Solenoid Extends
      _delay_ms(100);                                                           //------change prob
      PORTB = 0x00;        //PB5(relay) is LOW meaning Solenoid Retracts
    }
}
