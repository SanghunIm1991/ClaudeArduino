# プログラム① シリアル通信のみ

初めて読む場合は、先に[入門ガイド（用語解説）](../../docs/beginner_guide.md)に目を通すことを推奨します。

## 概要

Arduino Uno から PC へ、1秒ごとにカウントアップするメッセージをシリアル通信で送信するだけの最小構成プログラム。電気工作（配線）は不要で、USBケーブルでの接続のみで動作する。

## 電気工作

なし。Arduino Uno を USB ケーブルで PC に接続するだけでよい。

## 動作仕様

- 起動後、1秒間隔で以下の形式の文字列をシリアル出力する。

  ```
  Hello from Arduino Uno! count=0
  Hello from Arduino Uno! count=1
  Hello from Arduino Uno! count=2
  ...
  ```

- `count` は起動からの送信回数（0始まり）。オーバーフローするまで増加し続ける。

## 通信設定

| 項目 | 値 |
|---|---|
| ボーレート | 9600 bps |
| データビット | 8 |
| パリティ | なし |
| ストップビット | 1 |

ボーレートは、ATmega328P（16MHz動作）において誤差率が最も低く、互換性の高い9600bpsを採用した。

## ファイル構成

```
programs/01_serial_only/
├── platformio.ini   PlatformIO設定（ボード: uno、書き込み・モニタ先: COM3、ボーレート: 9600）
├── src/main.cpp      本体プログラム
└── README.md         本ドキュメント
```

## ビルド・書き込み・動作確認手順

前提: VS Code + PlatformIO IDE拡張機能がインストール済みであること。

1. VS Code で `programs/01_serial_only/` フォルダを開く（PlatformIOプロジェクトとして認識される）。
2. Arduino Uno をUSBケーブルでPCに接続する。
3. PlatformIOのUploadボタン（→アイコン）でビルド・書き込みを実行する。
   - CLIの場合: `pio run --target upload`
4. PlatformIOのSerial Monitorを開く（ボーレート9600に設定）。
   - CLIの場合: `pio device monitor`
5. 1秒ごとに `Hello from Arduino Uno! count=N` が表示されれば正常動作。

## 接続ポートについて

`platformio.ini` では `upload_port` / `monitor_port` を `COM3` に固定している。これは動作確認時にArduino UnoがCOM3として認識されていたためであり、USBポートの差し替えやPC再起動などによりCOM番号が変わった場合は、`platformio.ini` の該当箇所を実際のポート番号に書き換える必要がある。

現在のポート確認方法（PlatformIO CLI）:

```
pio device list
```

## 動作確認結果

2026-08-30、実機（Arduino Uno、COM3接続）にて書き込み・シリアル受信を確認済み。9600bpsでの通信は安定して動作した。
