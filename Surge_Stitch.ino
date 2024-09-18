// Define motor pins for the stepper motor (x-axis)
#define COIL1_PIN1 4                          //--------- change prob
#define COIL1_PIN2 5                           //--------- change prob
#define COIL2_PIN1 6                          //--------- change prob
#define COIL2_PIN2 7                        //--------- change prob

// Define motor pins for the DC motor (y-axis)
#define Y_MOTOR_PIN1 7                                   //  --------- change prob
#define Y_MOTOR_PIN2 8                              //--------- change prob
#define Y_ENABLE_PIN 9                             // --------- change prob

// Define solenoid control pin
#define RELAY_PIN 15             //pin B5                         --------- change prob

int currentX = 100;  // Current position of the stepper motor in steps //we start here, because stepper motor will bring the track set towards it sicne it does nto the have the ability to push it, it will jsut pull it fro mbehind
int currentY = 0;  // Current position of the DC motor

const int motorSpeed = 100;  // Speed of the DC motor (units per second)     //tr 350, 178, adn 140000 RPM                  --------- change prob

void setup() {
  // Setup the stepper motor
  pinMode(COIL1_PIN1, OUTPUT);
  pinMode(COIL1_PIN2, OUTPUT);
  pinMode(COIL2_PIN1, OUTPUT);
  pinMode(COIL2_PIN2, OUTPUT);

  // Initial state
  digitalWrite(COIL1_PIN1, LOW);
  digitalWrite(COIL1_PIN2, LOW);
  digitalWrite(COIL2_PIN1, LOW);
  digitalWrite(COIL2_PIN2, LOW);

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
  delay(5000);                                             --------- change prob
}

// Function to operate the solenoid for one push set
void operateSolenoid() {
  digitalWrite(RELAY_PIN, HIGH);  // Activate relay (solenoid extends)
  delay(100);  // Adjust delay for solenoid operation time (extend)                 --------- change prob
  digitalWrite(RELAY_PIN, LOW);   // Deactivate relay (solenoid retracts)
}

// Function to move stepper and DC motor to specified (x, y) coordinates
void moveToPosition(int x, int y) {
  // Move stepper motor (x-axis) to position x
  int steps = x - currentX;
  int stepDelay = 5;  // Delay between steps (milliseconds)

  for (int i = 0; i < abs(steps); i++) {
    if (steps > 0) {
      stepForward();
    } else {
      stepBackward();
    }
    delay(stepDelay);
  }

  // Move DC motor (y-axis) to position y
  int deltaY = y - currentY;
  int duration = abs(deltaY) / motorSpeed * 1000;  // Convert to milliseconds

  // Example: move motor in the correct direction
  if (deltaY > 0) {
    digitalWrite(Y_MOTOR_PIN1, HIGH);
    digitalWrite(Y_MOTOR_PIN2, LOW);
  } else {
    digitalWrite(Y_MOTOR_PIN1, LOW);
    digitalWrite(Y_MOTOR_PIN2, HIGH);
  }

  delay(duration);  // Move for the calculated duration
  
  // Stop the DC motor
  digitalWrite(Y_MOTOR_PIN1, LOW);
  digitalWrite(Y_MOTOR_PIN2, LOW);
}

void stepForward() {
  static int stepState = 0;
  stepState = (stepState + 1) % 4;
  setStep(stepState);
}

void stepBackward() {
  static int stepState = 0;
  stepState = (stepState + 3) % 4;  // -1 is equivalent to +3 in modulo 4
  setStep(stepState);
}

void setStep(int step) {
  switch (step) {
    case 0:  // 1st step
      digitalWrite(COIL1_PIN1, HIGH);
      digitalWrite(COIL1_PIN2, LOW);
      digitalWrite(COIL2_PIN1, HIGH);
      digitalWrite(COIL2_PIN2, LOW);
      break;
    case 1:  // 2nd step
      digitalWrite(COIL1_PIN1, LOW);
      digitalWrite(COIL1_PIN2, HIGH);
      digitalWrite(COIL2_PIN1, HIGH);
      digitalWrite(COIL2_PIN2, LOW);
      break;
    case 2:  // 3rd step
      digitalWrite(COIL1_PIN1, LOW);
      digitalWrite(COIL1_PIN2, HIGH);
      digitalWrite(COIL2_PIN1, LOW);
      digitalWrite(COIL2_PIN2, HIGH);
      break;
    case 3:  // 4th step
      digitalWrite(COIL1_PIN1, HIGH);
      digitalWrite(COIL1_PIN2, LOW);
      digitalWrite(COIL2_PIN1, LOW);
      digitalWrite(COIL2_PIN2, HIGH);
      break;
  }
}
