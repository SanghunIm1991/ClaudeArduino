#include <Arduino.h>

// チャタリング対策の効果を検証するための計測用スケッチ。
// 生のdigitalRead値(R)と、時間ベースデバウンス後の値(D)を
// それぞれ変化のたびにシリアル出力し、後でPCでグラフ化する。
// 本番用のmain.cpp（デバウンスなし）とは別のビルド環境(uno_chatter_test)として管理する。

const uint8_t SWITCH_PIN = 2;
const uint8_t LED_PIN = 8;
const unsigned long BAUD_RATE = 115200;
const unsigned long DEBOUNCE_DELAY_US = 50000UL;  // 50ms

int lastFlickerableState = LOW;
int debouncedState = LOW;
unsigned long lastDebounceTime = 0;

void setup() {
  pinMode(SWITCH_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(BAUD_RATE);
  Serial.println("type,micros,value");
}

void loop() {
  int currentState = digitalRead(SWITCH_PIN);

  if (currentState != lastFlickerableState) {
    Serial.print("R,");
    Serial.print(micros());
    Serial.print(",");
    Serial.println(currentState);
    lastDebounceTime = micros();
    lastFlickerableState = currentState;
  }

  if ((micros() - lastDebounceTime) > DEBOUNCE_DELAY_US) {
    if (debouncedState != currentState) {
      debouncedState = currentState;
      digitalWrite(LED_PIN, debouncedState);
      Serial.print("D,");
      Serial.print(micros());
      Serial.print(",");
      Serial.println(debouncedState);
    }
  }
}
