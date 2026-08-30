#include <Arduino.h>

// ①のシリアル通信実績（9600bpsが最も誤差率が低く互換性が高い）を踏襲
const unsigned long BAUD_RATE = 9600;

const uint8_t SWITCH_PIN = 2;   // プルダウン方式: 押下時HIGH、非押下時LOW（②と同じ回路構成）
const uint8_t GATE_PIN = 9;     // MOS-FETゲート駆動（LOW=消灯、HIGH=点灯）
const uint8_t CDS_PIN = A0;     // CdS分圧回路（5V-10kΩ-A0-CdS-GND）。暗いほど読み取り値が大きくなる配線

// ②のchatter_measurement.cppでの実測（約1msの間に生信号が2回反転する事例）を踏まえ、
// 同じ時間ベースデバウンス(50ms)をスイッチ入力に採用する。
const unsigned long DEBOUNCE_DELAY_US = 50000UL;

// 暗さ判定のヒステリシス閾値（要実機調整）。
// CdSセルの個体差・設置環境の明るさにより適正値は変わるため、
// 動作確認時にシリアル出力される生値(cds=...)を見ながら調整すること。
const int DARK_THRESHOLD_ON = 600;   // この値を超えたら暗いと判定して点灯
const int DARK_THRESHOLD_OFF = 500;  // この値を下回ったら明るいと判定して消灯（ONより低く設定しチャタリング的な点滅を防止）

const unsigned long STATUS_INTERVAL_MS = 500UL;

enum Mode {
  MODE_AUTO = 0,   // CdSによる自動点灯/消灯
  MODE_FORCE_ON,   // 常時点灯
  MODE_FORCE_OFF,  // 常時消灯
  MODE_COUNT
};

const char* modeName(Mode m) {
  switch (m) {
    case MODE_AUTO: return "AUTO";
    case MODE_FORCE_ON: return "FORCE_ON";
    case MODE_FORCE_OFF: return "FORCE_OFF";
    default: return "?";
  }
}

Mode currentMode = MODE_AUTO;
bool autoLedOn = false;  // MODE_AUTO時のヒステリシス状態を保持

int lastFlickerableSwitchState = LOW;
int debouncedSwitchState = LOW;
unsigned long lastDebounceTime = 0;

unsigned long lastStatusTime = 0;

void setup() {
  Serial.begin(BAUD_RATE);
  pinMode(SWITCH_PIN, INPUT);
  pinMode(GATE_PIN, OUTPUT);
  digitalWrite(GATE_PIN, LOW);
}

void loop() {
  // --- スイッチ読み取り（デバウンス）とモード切替（立ち上がりエッジで進める） ---
  int currentSwitchState = digitalRead(SWITCH_PIN);

  if (currentSwitchState != lastFlickerableSwitchState) {
    lastDebounceTime = micros();
    lastFlickerableSwitchState = currentSwitchState;
  }

  if ((micros() - lastDebounceTime) > DEBOUNCE_DELAY_US) {
    if (debouncedSwitchState != currentSwitchState) {
      bool risingEdge = (debouncedSwitchState == LOW && currentSwitchState == HIGH);
      debouncedSwitchState = currentSwitchState;
      if (risingEdge) {
        currentMode = static_cast<Mode>((currentMode + 1) % MODE_COUNT);
      }
    }
  }

  // --- CdS読み取り ---
  int cdsValue = analogRead(CDS_PIN);

  // --- モードに応じてLED（MOS-FETゲート）の状態を決定 ---
  bool ledOn;
  switch (currentMode) {
    case MODE_FORCE_ON:
      ledOn = true;
      break;
    case MODE_FORCE_OFF:
      ledOn = false;
      break;
    case MODE_AUTO:
    default:
      if (cdsValue >= DARK_THRESHOLD_ON) {
        autoLedOn = true;
      } else if (cdsValue <= DARK_THRESHOLD_OFF) {
        autoLedOn = false;
      }
      // ON/OFF閾値の間はヒステリシスにより直前の状態を保持
      ledOn = autoLedOn;
      break;
  }

  digitalWrite(GATE_PIN, ledOn ? HIGH : LOW);

  // --- 動作確認用の定期シリアル出力 ---
  unsigned long now = millis();
  if (now - lastStatusTime >= STATUS_INTERVAL_MS) {
    lastStatusTime = now;
    Serial.print("mode=");
    Serial.print(modeName(currentMode));
    Serial.print(" cds=");
    Serial.print(cdsValue);
    Serial.print(" led=");
    Serial.println(ledOn ? "ON" : "OFF");
  }
}
