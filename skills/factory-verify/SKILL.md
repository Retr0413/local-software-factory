---
name: factory-verify
description: Independently verify a Factory candidate commit with acceptance tests, runtime evidence, documentation checks, and targeted defensive security checks.
---

# Factory の独立検証

1. 検証用 worktree が指定された候補コミットを指していることを確認する。実装前に決めた受入条件、ベース側の必須チェック、対象リポジトリの検証手順を確認する。
2. 条件ごとに必要なテストと動作確認を行う。UI・CLI・API などの実動作を確認するときは [QA と動作証跡](references/qa-evidence.md) を使う。使い方や設定が変わった場合は、該当するドキュメントの手順も照合する。
3. 統括からセキュリティ確認を指定された場合や、変更に認証・権限、外部入力、依存関係などの影響がある場合は [セキュリティ確認](references/security.md) を使い、確認結果を統括へ渡す。

候補コミット、条件ごとの成否、実行コマンドと環境、証跡の場所、指摘、未検証事項を統括へ報告する。確認できない条件は理由付きで保留にする。
