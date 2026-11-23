---
name: factory-verify
description: Independently verify a Factory candidate commit against acceptance conditions using checks, real behavior and evidence. Use for QA or review.
---

# Factory の独立検証

指定された候補コミットを確認する。ベース側で決めた受入条件と対象リポジトリの検証手順に沿って、必要なテスト、起動、画面確認、差分確認を行う。作業用の一時ファイルは自身の検証環境に置き、製品コードへの指摘は統括を通して実装担当に返す。

候補コミット、条件ごとの確認結果、実行コマンド、問題の再現方法、証跡の場所、未検証事項を報告する。検証前提が成立しない場合は理由を付けて保留を報告する。
