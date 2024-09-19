// Define motor pins for the DC GEAR motor (X-axis)
#define X_MOTOR_PIN1 1                                   //  --------- change prob
#define X_MOTOR_PIN2 2                              //--------- change prob
#define X_ENABLE_PIN 3                             // --------- change prob

// Define motor pins for the DC motor (y-axis)
#define Y_MOTOR_PIN1 7                                   //  --------- change prob
#define Y_MOTOR_PIN2 8                              //--------- change prob
#define Y_ENABLE_PIN 9                             // --------- change prob

// Define solenoid control pin
#define RELAY_PIN 15             //pin B5                         --------- change prob

int currentX = 100;  // Current position of the DC GEAR Motor
int currentY = 0;  // Current position of the DC motor

const int motorSpeed1 = 100;  // Speed of the DC GEAR motor (units per second)     //tr 10 RPM                  --------- change prob
const int motorSpeed2 = 100;  // Speed of the DC motor (units per second)     //tr 350, 178, adn 140000 RPM                  --------- change prob

void setup() {
  // Setup the DC GEAR motor
  pinMode(X_MOTOR_PIN1, OUTPUT);
  pinMode(X_MOTOR_PIN2, OUTPUT);
  pinMode(X_ENABLE_PIN, OUTPUT);
  digitalWrite(x_ENABLE_PIN, HIGH); // Enable the DC motor driver

  // Setup the DC motor
  pinMode(Y_MOTOR_PIN1, OUTPUT);
  pinMode(Y_MOTOR_PIN2, OUTPUT);
  pinMode(Y_ENABLE_PIN, OUTPUT);
  digitalWrite(Y_ENABLE_PIN, HIGH); // Enable the DC motor driver
  moveToPosition(currentX, currentY);

  // Setup relay control pin
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW); // Ensure relay is initially off
}

void loop() {
  // Example coordinates to move to (x, y)
  int targetX = 50;  // Example x-coordinate
  int targetY = 150;  // Example y-coordinate

  moveToPosition(targetX, targetY);

  // Update current positions after movement
  currentX = targetX;
  currentY = targetY;

  // Operate solenoid for one push set
  operateSolenoid();

  // Add a delay or other logic as needed
  delay(5000);                                             //--------- change prob
}

// Function to operate the solenoid for one push set
void operateSolenoid() {
  digitalWrite(RELAY_PIN, HIGH);  // Activate relay (solenoid extends)
  //Somehow dispense string, cut it (only on the closing part string), and glue it using solidifying liquid
  delay(100);  // Adjust delay for solenoid operation time (extend)                 --------- change prob
  digitalWrite(RELAY_PIN, LOW);   // Deactivate relay (solenoid retracts)
}

// Function to move GEAR motor and DC motor to specified (x, y) coordinates
void moveToPosition(int x, int y) {
  // Move DC motor (x-axis) to position x
  int deltaX = x - currentX;
  int duration1 = abs(deltaX) / motorSpeed1 * 1000;  // Convert to milliseconds

  if (deltaX > 0) {
    digitalWrite(X_MOTOR_PIN1, HIGH);
    digitalWrite(X_MOTOR_PIN2, LOW);
  } else {
    digitalWrite(X_MOTOR_PIN1, LOW);
    digitalWrite(X_MOTOR_PIN2, HIGH);
  }

  delay(duration1);  // Move for the calculated duration
  
  // Stop the DC motor
  digitalWrite(Y_MOTOR_PIN1, LOW);
  digitalWrite(Y_MOTOR_PIN2, LOW);

  // Move DC motor (y-axis) to position y
  int deltaY = y - currentY;
  int duration2 = abs(deltaY) / motorSpeed2 * 1000;  // Convert to milliseconds

  if (deltaY > 0) {
    digitalWrite(Y_MOTOR_PIN1, HIGH);
    digitalWrite(Y_MOTOR_PIN2, LOW);
  } else {
    digitalWrite(Y_MOTOR_PIN1, LOW);
    digitalWrite(Y_MOTOR_PIN2, HIGH);
  }

  delay(duration2);  // Move for the calculated duration
  
  // Stop the DC motor
  digitalWrite(Y_MOTOR_PIN1, LOW);
  digitalWrite(Y_MOTOR_PIN2, LOW);
}
