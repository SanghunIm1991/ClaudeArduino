#include <Arduino.h>

const uint8_t SWITCH_PIN = 2;  // プルダウン方式: 押下時HIGH、非押下時LOW
const uint8_t LED_PIN = 8;

// chatter_measurement.cppでの実測（約1msの間に生信号が2回反転する事例を確認）を踏まえ、
// 時間ベースデバウンスを採用する。遅延時間はチャタリング収束時間に対し十分な余裕を持つ50ms。
const unsigned long DEBOUNCE_DELAY_US = 50000UL;

int lastFlickerableState = LOW;
int debouncedState = LOW;
unsigned long lastDebounceTime = 0;

void setup() {
  pinMode(SWITCH_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  int currentState = digitalRead(SWITCH_PIN);

  if (currentState != lastFlickerableState) {
    lastDebounceTime = micros();
    lastFlickerableState = currentState;
  }

  if ((micros() - lastDebounceTime) > DEBOUNCE_DELAY_US) {
    if (debouncedState != currentState) {
      debouncedState = currentState;
      digitalWrite(LED_PIN, debouncedState);
    }
  }
}
