#include<avr/io.h>          // Header file for AVR microcontroller
#include<util/delay.h>      // Header file for delay
#define setbit(x,y)(x|=y)   // Define macro to make bit/bits high
#define clearbit(x,y)(x&=~y)  // Define macro to make bit/bits low
#define bitn(p)(0x01 <<(p))   // Define macro for bit position
#define checkbit(x,y)((x)&(y))   // Define macro to check the bit of a register

int currentX = 255;         // Current position of the GEAR motor in mm
int currentY = 0;           // Current position of the DC motor in mm
int motorSpeed1 = (10 * 6 * 3.1415) / 60;     // Speed of the DC GEAR motor (mm per second)     
int motorSpeed2 = (200 * 40 * 3.1415) / 60;   // Speed of the DC motor (mm per second)     
int targetX, targetY, deltaX, deltaY = 0;

int main(void)
{
  DDRB = 0xF0;  // Set PB7 to PB4 as outputs for motor control
  DDRD = 0xF0;  // Set PD7 to PD4 as outputs for motor control
  float duration = 0.0;
  
  // Initialize Serial communication
  Serial.begin(9600);

  while (1)
  {
    if (Serial.available()) {    // Example input: 92,42,92,148;106,42,106,148;121,42,121,148;135,42,135,148;150,42,150,148;164,42,164,148;179,42,179,148;193,42,193,148;208,42,208,148;223,42,223,148
      Serial.println("Received Data");     // For some reason, even with manual input, it is not detecting any input
      String data = Serial.readStringUntil(';');  // Read data until ';' delimiter

      // Parsing the received string (data) to extract multiple pairs
      while (data.length() > 0) {
        int commaIndex = data.indexOf(',');
        if (commaIndex == -1) break; // No more commas

        targetX = data.substring(0, commaIndex).toInt();  // Extract x1
        data = data.substring(commaIndex + 1); // Remove processed part

        commaIndex = data.indexOf(',');
        if (commaIndex == -1) break; // No more commas

        targetY = data.substring(0, commaIndex).toInt();  // Extract y1
        data = data.substring(commaIndex + 1); // Remove processed part

        // Process the target coordinates here (targetX, targetY)
        Serial.println(targetX); // For debugging
        Serial.println(targetY); // For debugging

        // X-movement logic
        Serial.println("Starting GEAR Motor");
        deltaX = currentX - targetX;   // Right to left movement logic
        duration = abs(deltaX) / motorSpeed1 * 1000;  // Convert to milliseconds
        duration = 100.5;   // Normally, this would not be here, but Arduino will give error during compiling, if we don't have a cosntant value for duration
        if (deltaX > 0)
        {
          PORTB = 0x40;        // Move left (anticlockwise)
        }
        else
        {
          PORTB = 0x80;        // Move right (clockwise)
        }
        _delay_ms(duration);  // Delay for the movement duration
        PORTB = 0x00;         // Stop the motor
        Serial.println("Stopping GEAR Motor");
  
        // Y-movement logic
        Serial.println("Starting Blue Motor");
        deltaY = targetY - currentY;   // Up/down movement logic
        duration = abs(deltaY) / motorSpeed2 * 1000;  // Convert to milliseconds
        duration = 100.5;      // Normally, this would not be here, but Arduino will give error during compiling, if we don't have a cosntant value for duration
        if (deltaY < 0)
        {
          PORTD = 0x40;        // Move downward (anticlockwise)
        }
        else
        {
          PORTD = 0x80;        // Move upward (clockwise)
        }
        _delay_ms(duration);  // Delay for the movement duration
        PORTD = 0x00;         // Stop the motor
        Serial.println("Stopping Blue Motor");
  
        // Solenoid control
        Serial.println("Starting Solenoid");
        PORTB = 0x20;        // Activate solenoid
        _delay_ms(100);                                                           
        PORTB = 0x00;        // Deactivate solenoid
        Serial.println("Stopping Solenoid");
      }
    }
  }
}
