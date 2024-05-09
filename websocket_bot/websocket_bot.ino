#include <ESP8266WiFi.h>
#include <WebSocketsServer.h>

// Wifi
const char* ssid = "81NE-S010404 4362";
const char* password = "9054Nw&0";

// Driver 1
// PWM Pins
const int in1u = 5; 
const int in2u = 4; 
const int enau = 2; 
const int in3u = 14;
const int in4u = 12; 
const int enbu = 13; 

// Driver 2
const int in1d = 3;
const int in2d = 0; 
// const int enad = 12; 
const int in3d = 9;
const int in4d = 16; 
// const int enbd = 13;

// Web Socket Instance
WebSocketsServer webSocket = WebSocketsServer(8080); 


void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length) {
  // Define variables outside of the switch statement
  String message;
  char command[5];
  int speed1, speed2, speed3, speed4;

  switch(type){
    case WStype_DISCONNECTED:
      Serial.printf("[%u] Disconnected!\n", num);
      break;
    case WStype_TEXT:
      Serial.printf("[%u] get Text: %s\n", num, payload);

      // Convert the payload to a string
      message = String((char*)payload);
      

      if (sscanf(message.c_str(), "%s %d %d %d %d", command, &speed1, &speed2, &speed3, &speed4) == 5) {
        // Call the move function with the extracted values

        move(command, speed1, speed2, speed3, speed4);
      } else {
        Serial.println("Invalid message format");
      }
      
      break;
    default:
      break;
  }
}


void setup() {
  Serial.begin(9600);

  // Connect to WiFi
  connectToWiFi();

  // Start WebSocket server
  webSocket.begin();
  webSocket.onEvent(webSocketEvent);

  Serial.println("WebSocket server started");

  // Pin Setup
  pinMode(in1u, OUTPUT); 
  pinMode(in2u, OUTPUT); 
  pinMode(enau, OUTPUT);
  pinMode(in3u, OUTPUT);
  pinMode(in4u, OUTPUT);
  pinMode(enbu, OUTPUT);

  pinMode(in1d, OUTPUT); 
  pinMode(in2d, OUTPUT); 
  // pinMode(enad, OUTPUT);
  pinMode(in3d, OUTPUT);
  pinMode(in4d, OUTPUT);
  // pinMode(enbd, OUTPUT);
}

void loop() {
  webSocket.loop();

  // Check if WiFi connection is lost and reconnect if necessary
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi connection lost. Reconnecting...");
    connectToWiFi();
  }
}


void connectToWiFi() {
  // Attempt to connect to WiFi
  WiFi.begin(ssid, password);
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 5) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
    attempts++;
  }

  // Check if connected or maximum attempts reached
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("Connected to WiFi");
  } else {
    Serial.println("Failed to connect to WiFi");
  }
}


void move(String command, int speed1, int speed2, int speed3, int speed4) {
  
  analogWrite(enau, speed1);
  analogWrite(enbu, speed2);
  // analogWrite(enad, speed3);
  // analogWrite(enbd, speed4);
  
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
    // Unknown command
    // Serial.println("Command : \n");
    // Serial.println(command);
    // Serial.println("End Command\n");
    Serial.println("Unknown Command");
  }
}
/*
char ar[5];
switch(ar)
{
  case "";
}
*/

