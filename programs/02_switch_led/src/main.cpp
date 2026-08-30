#include <Arduino.h>

const uint8_t SWITCH_PIN = 2;  // プルダウン方式: 押下時HIGH、非押下時LOW
const uint8_t LED_PIN = 8;

void setup() {
  pinMode(SWITCH_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_PIN, digitalRead(SWITCH_PIN));
}
