#include <Arduino.h>

// ボーレート9600bps: ATmega328P(16MHz)で誤差率が最も低く、最も互換性の高い設定。
const unsigned long BAUD_RATE = 9600;

unsigned long counter = 0;

void setup() {
  Serial.begin(BAUD_RATE);
}

void loop() {
  Serial.print("Hello from Arduino Uno! count=");
  Serial.println(counter);
  counter++;
  delay(1000);
}
