// Driver 1
// PWM Pins
#define in1u 2
#define in2u 4 
#define enau 3 
#define in3u 7
#define in4u 8
#define enbu 5 

// Driver 2
#define in1d 10
#define in2d 11 
#define enad 6 
#define in3d 12
#define in4d 13 
#define enbd 9

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
    move("STP", 0, 0, 0, 0);
    lastReceivedCommand = "STP";
    Serial.println("STOP");
  }
}

void receiveCommand() {
  char command[5];
  int speed1, speed2, speed3, speed4;
  String message;

  if (Serial.available() > 0) {
    // Read command from ESP8266
    message = Serial.readStringUntil('\n');
    Serial.println(message);

    if (sscanf(message.c_str(), "%s %d %d %d %d", command, &speed1, &speed2, &speed3, &speed4) == 5) {
        // Call the move function with the extracted values
        move(command, speed1, speed2, speed3, speed4);
        // Update the last received command time
        lastReceivedCommandTime = millis();
        lastReceivedCommand = String(command);
        Serial.println(command);
      } 
    else {
      Serial.println("Invalid message format");
    }
  }
}

void move(String command, int speed1, int speed2, int speed3, int speed4) {
  analogWrite(enau, speed1);
  analogWrite(enbu, speed2);
  analogWrite(enad, speed3);
  analogWrite(enbd, speed4);
  
  if (command.equals("FWD")) {
    // Move forward
    digitalWrite(in1u, HIGH);
    digitalWrite(in2u, LOW);
    digitalWrite(in3u, HIGH);
    digitalWrite(in4u, LOW);
    digitalWrite(in1d, HIGH);
    digitalWrite(in2d, LOW);
    digitalWrite(in3d, HIGH);
    digitalWrite(in4d, LOW);
  } else if (command.equals("BWD")) {
    // Move backward
    digitalWrite(in1u, LOW);
    digitalWrite(in2u, HIGH);
    digitalWrite(in3u, LOW);
    digitalWrite(in4u, HIGH);
    digitalWrite(in1d, LOW);
    digitalWrite(in2d, HIGH);
    digitalWrite(in3d, LOW);
    digitalWrite(in4d, HIGH);
  } else if (command.equals("RT")) {
    // Turn right
    digitalWrite(in1u, LOW);
    digitalWrite(in2u, HIGH);
    digitalWrite(in3u, HIGH);
    digitalWrite(in4u, LOW);
    digitalWrite(in1d, LOW);
    digitalWrite(in2d, HIGH);
    digitalWrite(in3d, HIGH);
    digitalWrite(in4d, LOW);
  } else if (command.equals("LT")) {
    // Turn left
    digitalWrite(in1u, HIGH);
    digitalWrite(in2u, LOW);
    digitalWrite(in3u, LOW);
    digitalWrite(in4u, HIGH);
    digitalWrite(in1d, HIGH);
    digitalWrite(in2d, LOW);
    digitalWrite(in3d, LOW);
    digitalWrite(in4d, HIGH);
  } else if (command.equals("STP")) {
    // Stop
    digitalWrite(in1u, LOW);
    digitalWrite(in2u, LOW);
    digitalWrite(in3u, LOW);
    digitalWrite(in4u, LOW);
    digitalWrite(in1d, LOW);
    digitalWrite(in2d, LOW);
    digitalWrite(in3d, LOW);
    digitalWrite(in4d, LOW);
  } else if (command.equals("DFLT")) {
    // Diagonal forward left
    digitalWrite(in1u, HIGH);
    digitalWrite(in2u, LOW);
    digitalWrite(in3u, LOW);
    digitalWrite(in4u, LOW);
    digitalWrite(in1d, LOW);
    digitalWrite(in2d, HIGH);
    digitalWrite(in3d, LOW);
    digitalWrite(in4d, LOW);
  } else if (command.equals("DFRT")) {
    // Diagonal forward right
    digitalWrite(in1u, LOW);
    digitalWrite(in2u, HIGH);
    digitalWrite(in3u, LOW);
    digitalWrite(in4u, LOW);
    digitalWrite(in1d, HIGH);
    digitalWrite(in2d, LOW);
    digitalWrite(in3d, LOW);
    digitalWrite(in4d, LOW);
  } else if (command.equals("DWLT")) {
    // Diagonal backward left
    digitalWrite(in1u, LOW);
    digitalWrite(in2u, LOW);
    digitalWrite(in3u, HIGH);
    digitalWrite(in4u, LOW);
    digitalWrite(in1d, LOW);
    digitalWrite(in2d, LOW);
    digitalWrite(in3d, LOW);
    digitalWrite(in4d, HIGH);
  } else if (command.equals("DWRT")) {
    // Diagonal backward right
    digitalWrite(in1u, LOW);
    digitalWrite(in2u, LOW);
    digitalWrite(in3u, LOW);
    digitalWrite(in4u, HIGH);
    digitalWrite(in1d, LOW);
    digitalWrite(in2d, HIGH);
    digitalWrite(in3d, LOW);
    digitalWrite(in4d, LOW);
  } else {
    Serial.println("Unknown Command");
  }
}


