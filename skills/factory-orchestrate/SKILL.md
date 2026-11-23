---
name: factory-orchestrate
description: GitHub Issue や名前付きタスクの実装依頼（「Issue を実装して」など）を受け、Herdr で調査・実装・独立 QA・レビュー・記録を統括する。
---

# Factory の統括

1 Issue・1実装担当。次の工程に進んだ時点で該当する手順を開く。子セッションは割り当てられた役割を実行する。

## Description から読む Skill を選ぶ

今の判断に合う行のリンクを開く。次の条件が生じたら、この表から選び直す。

| Description（使う場面） | 読む Skill・資料 |
| --- | --- |
| 新規依頼の受入条件を決め、複数 Issue の並列可否と依存順を判断する。 | [受付と割り当て](procedures/factory-orchestrate-intake/SKILL.md) |
| コード側の仕様や影響範囲が不明 | [調査を依頼](../factory-investigate/SKILL.md) |
| 仕事を起動する。Herdr 内の統括ペインから CLI を指定する（既定は統括と同じ CLI） | [Herdr 起動](../herdr-factory-dispatch/SKILL.md) |
| 実装担当へ受入条件、確認コマンド、許可された GitHub 操作を渡す | [実装担当の手順](../factory-implement/SKILL.md) |
| 候補が届いた。別ペインに mode=verify、base=候補 SHA、比較元、受入条件、指定の確認範囲を渡す | [独立 QA](../factory-verify/SKILL.md) |
| QA・レビュー・CI から修正依頼が届いたとき、元の担当に戻す範囲と再検証対象を決める。 | [指摘対応](procedures/factory-orchestrate-findings/SKILL.md) |
| PR 作成・既存 PR 対応の依頼がある | [PR と Walden レビュー](../factory-pr/SKILL.md) |
| 完了・中断・保留になった。検証済み SHA、未確認事項、作業場所を報告する | [結果と改善材料の記録](../factory-record/SKILL.md) |

PR を扱わない実装依頼の Walden レビューは統括が実行する。Herdr 外では受付まで進め、起動は対象セッションの統括ペインに引き継ぐ。

## 指摘対応

[元の担当への差し戻しと再検証](procedures/factory-orchestrate-findings/SKILL.md)を使う。
