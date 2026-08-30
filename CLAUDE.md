# ClaudeArduino プロジェクト

## 目的

AIエージェント（Claude Code）を用いた組み込み開発の可能性検証。生産用ソフトウェアではなく調査・実験が目的のため、正式な工程管理（waterfall-dev-workflow等）は導入せず、軽量な進め方を採る。

## ハードウェア

- マイコンボード: Arduino Uno R3（公式サイト: https://docs.arduino.cc/hardware/uno-rev3/）
- データシート: `A000066-datasheet.pdf`（プロジェクト直下に格納済み）
- 周辺部品: SWITCH SCIENCE「Arduinoをはじめよう」キット（内容物は `docs/overview.md` 参照）
- 電気工作（実配線・ブレッドボード組み立て）はユーザーが行う。Claudeは回路図をmermaid記法で作成し、**必ず電圧・電流計算を添える**。

## 開発環境

- エディタ: Visual Studio Code
- ビルド・書き込み・シリアルモニタ: PlatformIO IDE拡張機能
- マイコンとの通信: USBケーブル経由のシリアル通信

## 進め方

- 調査目的のため、セッションごとに段階的に進める。都度、概要資料やコードの内容を確認しながら次に進む。
- 現時点で構想している実験プログラム:
  1. シリアル通信のみ（電気工作なし）
  2. 単純なタクトスイッチとLED
  3. お任せ（内容はClaudeが提案）
- 各プログラムは `programs/<番号>_<内容>/` 以下にPlatformIOプロジェクトとして配置する想定（例: `programs/01_serial_only/`）。

## Git運用ルール

[git-conventions スキル](~/.claude/skills/git-conventions)に従う。要点:

- commit author: `ClaudeCode <noreply@anthropic.com>`、メッセージ先頭に `[claude] ` を付与
- 作業が完了した区切りで、ユーザーの都度許可を得ずコミットしてよい（対象はGitで復元可能な変更のみ）
- **push承認の粒度: 都度確認（デフォルト）**。`git push`は実行するたびに個別の承認を得る。
- amend / rebase / force push / reset --hard 等の破壊的・履歴改変操作は禁止（依頼があっても本方針を伝えて確認する）

## 電気的な作業の注意（このPCの機微性に関する全般ルールより）

このPCはクレジットカード情報の入力や証券取引に使われるため、出所不明の実行ファイル・拡張機能のインストールやセキュリティ設定変更を行う際は、目的とセキュリティへの影響を日本語で明示しユーザーの承認を得る（詳細はユーザーのグローバル`CLAUDE.md`を参照）。
