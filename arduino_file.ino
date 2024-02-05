#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>

Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified();
int zero=0;
void setup() {
  Serial.begin(9600);
  pinMode(10, INPUT); // Setup for leads off detection LO +
  pinMode(11, INPUT); // Setup for leads off detection LO -

  if (!accel.begin()) {
    Serial.println("No valid accelerometer found");
    while (1);
  }
}

void loop() {
  // Check for leads off detection
  if ((digitalRead(10) == HIGH) || (digitalRead(11) == HIGH)) {
    Serial.print("ECG: ");
    Serial.print(zero);
  } 
  else {
    // Send the value of analog input 0 (ECG data)
    Serial.print("ECG: ");
    Serial.print(analogRead(A0));
  }
    // Read and send accelerometer data
    sensors_event_t event;
    accel.getEvent(&event);
    Serial.print(" X: ");
    Serial.print(event.acceleration.x);
    Serial.print(" Y: ");
    Serial.print(event.acceleration.y);
    Serial.print(" Z: ");
    Serial.print(event.acceleration.z);
    Serial.println(" m/s^2");

    
    // Wait for a bit to prevent serial data saturation
    delay(1);
  
}