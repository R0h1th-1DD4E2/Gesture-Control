// Driver 1
// PWM Pins
const int in1u = 2; 
const int in2u = 4; 
const int enau = 3; 
const int in3u = 7;
const int in4u = 8; 
const int enbu = 5; 

// Driver 2
const int in1d = 10;
const int in2d = 11; 
const int enad = 6; 
const int in3d = 12;
const int in4d = 13; 
const int enbd = 9;

// Time
const unsigned long commandTimeout = 5000;

// Last received command time
unsigned long lastReceivedCommandTime = 0;

// Define a variable to store the last command received
String lastReceivedCommand = "";

void setup() {
  Serial.begin(9600);

  // Pin Setup
  pinMode(in1u, OUTPUT); 
  pinMode(in2u, OUTPUT); 
  pinMode(enau, OUTPUT);
  pinMode(in3u, OUTPUT);
  pinMode(in4u, OUTPUT);
  pinMode(enbu, OUTPUT);

  pinMode(in1d, OUTPUT); 
  pinMode(in2d, OUTPUT); 
  pinMode(enad, OUTPUT);
  pinMode(in3d, OUTPUT);
  pinMode(in4d, OUTPUT);
  pinMode(enbd, OUTPUT);

  Serial.println("Arduino Uno motor control started");
}

void loop() {
  // Check for incoming commands from ESP8266
  receiveCommand();

  // Check if no command received for more than 5 seconds
  if (millis() - lastReceivedCommandTime >= commandTimeout && lastReceivedCommandTime != 0 && lastReceivedCommand != "STP") {
    // move("STP", 0, 0, 0, 0); // Stop the motors if no command received for more than 5 seconds and the previous command was not STP
    lastReceivedCommand = "STP";
    Serial.println("STOP");
  }
}

void receiveCommand() {
  if (Serial.available() > 0) {
    // Read command from ESP8266
    String command = Serial.readStringUntil('\n');
    Serial.print("Received command: ");
    Serial.println(command);
  }
}

