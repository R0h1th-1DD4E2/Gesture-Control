#include <ESP8266WiFi.h>
#include <WebSocketsServer.h>

// Wifi
const char* ssid = "81NE-S010404 4362";
const char* password = "9054Nw&0";

// Web Socket Instance
WebSocketsServer webSocket = WebSocketsServer(8080);

void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length) {
  switch(type){
    case WStype_DISCONNECTED:
      Serial.printf("[%u] Disconnected!\n", num);
      break;
    case WStype_TEXT:
      Serial.printf("[%u] get Text: %s\n", num, payload);

      // Forward the received command to Arduino Uno via serial
      Serial.write(payload, length);
      Serial.println(); // End the command with a newline
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
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  // Check if connected or maximum attempts reached
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("Connected to WiFi");
  } else {
    Serial.println("Failed to connect to WiFi");
  }
}
