#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include "Adafruit_Si7021.h"

// ApisLM IoT Edge Node - Telemetry Collector
// Zero-Cost Solar-Powered ESP32

const char* ssid = "APIARY_NETWORK";
const char* password = "zero_cost_swarm";
const char* serverName = "http://192.168.0.153:8000/api/iot/ingest";
const String DEVICE_TOKEN = "tenant-123-esp32";
const String DEVICE_ID = "Hive_001";

// Sensors
Adafruit_Si7021 sensor = Adafruit_Si7021();
const int MIC_PIN = 34; // Analog microphone for acoustic frequency

// Mock Load Cell (Weight)
float readWeight() {
  // In reality, read from HX711 Load Cell Amplifier
  return 45.2 + (random(-5, 5) / 10.0);
}

// Extract dominant acoustic frequency (FFT simulation for simplicity)
int readAcousticFrequency() {
  int peak = analogRead(MIC_PIN);
  // Simulated Queenright Hive Frequency
  return 235 + (peak % 20); 
}

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  
  Serial.println("Connecting to Apiary Mesh Network...");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nApisLM Edge Node Connected!");
  
  if (!sensor.begin()) {
    Serial.println("Si7021 sensor not found!");
  }
}

void loop() {
  if(WiFi.status() == WL_CONNECTED){
    HTTPClient http;
    http.begin(serverName);
    
    // Auth Header
    http.addHeader("x-device-token", DEVICE_TOKEN);
    http.addHeader("Content-Type", "application/json");
    
    // Gather Telemetry
    float temp = sensor.readTemperature();
    float humidity = sensor.readHumidity();
    float weight = readWeight();
    int frequency = readAcousticFrequency();
    
    // Construct JSON Payload
    String jsonPayload = "{\"device_id\":\"" + DEVICE_ID + "\",\"timestamp_ms\":" + String(millis()) + ",\"sensors\":{";
    jsonPayload += "\"brood_temp_c\":" + String(temp) + ",";
    jsonPayload += "\"humidity_rh\":" + String(humidity) + ",";
    jsonPayload += "\"weight_kg\":" + String(weight) + ",";
    jsonPayload += "\"acoustic_hz\":" + String(frequency);
    jsonPayload += "}}";
    
    Serial.println("Sending Telemetry: " + jsonPayload);
    
    // Post to Local Backend
    int httpResponseCode = http.POST(jsonPayload);
    if(httpResponseCode > 0){
      Serial.println("Response Code: " + String(httpResponseCode));
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  }
  
  // Enter Deep Sleep for 3 minutes to save solar battery
  Serial.println("Entering Deep Sleep...");
  delay(180000); 
}
