"""チャタリング計測用スケッチ(chatter_measurement.cpp)のシリアル出力をCSVファイルに保存する。

事前に `pio run -e uno_chatter_test --target upload` で計測用ファームウェアを書き込んでおくこと。
このスクリプトを起動するとシリアルポートを開く際にArduinoがリセットされ、
計測がmicros()=0から再スタートする。

使い方: py -3.11 capture_chatter_log.py [COMポート] [計測秒数] [出力ファイル名]
例:     py -3.11 capture_chatter_log.py COM3 20 chatter_log.csv
"""

import sys
import time

import serial

DEFAULT_PORT = "COM3"
DEFAULT_DURATION_SEC = 20
DEFAULT_BAUD = 115200
DEFAULT_OUT_PATH = "chatter_log.csv"


def main():
    port = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PORT
    duration_sec = float(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_DURATION_SEC
    out_path = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_OUT_PATH

    with serial.Serial(port, DEFAULT_BAUD, timeout=1) as ser, open(
        out_path, "w", newline="", encoding="utf-8"
    ) as f:
        # ポートオープン直後のリセットが安定するまで少し待つ
        time.sleep(2)
        ser.reset_input_buffer()

        print(f"Capturing on {port} for {duration_sec}s -> {out_path}")
        start = time.time()
        while time.time() - start < duration_sec:
            line = ser.readline().decode("utf-8", errors="replace").strip()
            if line:
                f.write(line + "\n")
                print(line)

    print("done")


if __name__ == "__main__":
    main()
