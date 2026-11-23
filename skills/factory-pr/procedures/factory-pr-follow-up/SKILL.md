---
name: factory-pr-follow-up
description: 既存 PR に修正を反映する依頼を受け、元の実装担当・現在の head・再確認範囲を特定する。
---

# 既存 PR を元の実装担当と更新する

1. PR の作成者、現在の head SHA、レビューのスレッドと CI の結果を確認する。他人の PR の扱いは `my-walden-review` の作成者判定に従う。CI の失敗原因はログで確認し、コード変更が必要なものと環境側の失敗を区別する。
2. 関連 Issue と [Factory の作業記録](../../../factory-record/SKILL.md) を使って元の Herdr 実装担当を特定する。担当が停止している場合は、同じ仕事の作業環境と会話を照合してから再開する。対応を依頼された指摘は、[統括の指摘対応](../../../factory-orchestrate/SKILL.md#指摘対応)で扱う。
3. push の前に、現在の PR の head が確認済みの head と一致し、公開するコミットが検証済みの候補 SHA と一致することを確かめる。新しい変更があれば対象と確認結果を見直す。必要な Walden レビューを経て依頼された範囲で PR を更新し、更新後の CI を確認する。再確認の結果と残る対応を作業記録に渡す。

## 判断例

PR を調べた後に別の人が更新していた場合は、前回読んだ head からの差分を確認する。既に取り込まれた修正と残件を切り分け、残件だけを元担当へ返す。

## 出典と採用した観点

既存 PR の文脈と指摘を読む観点を採用。更新先と元の担当の照合は Factory 側で追加した。[Factory-AI / follow-up-on-pr](https://github.com/Factory-AI/factory-plugins/blob/e63e519a736140c86f37be95a529a0c44dc9a96e/plugins/code-review/skills/follow-up-on-pr/SKILL.md)・[この Factory の Herdr 運用設計](../../../../docs/herdr-workflow.md)
