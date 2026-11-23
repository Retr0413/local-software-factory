---
name: factory-implement
description: Factory で割り当て済みの Issue を担当 worktree で実装するとき、または同じ担当が QA・Walden・CI の指摘を修正するときに使う。
---

# Factory 実装担当

Issue、受入条件、範囲、ベースを確認して担当 worktree で変更する。判断に足りない情報は問いと根拠を統括へ返す。

## Description から読む Skill を選ぶ

今の判断に合う行のリンクを開く。次の条件が生じたら、この表から選び直す。

| Description（使う場面） | 読む Skill・資料 |
| --- | --- |
| 不具合の再現、機能追加、再実行時の挙動に対し、修正の成否を識別できるテストを選ぶ。 | [回帰テストと観測点](procedures/factory-implement-regression/SKILL.md) |
| API・設定・CLI・保存形式を変えるとき、既存利用者への影響と更新する利用手順を決める。 | [公開契約と文書](procedures/factory-implement-public-contract/SKILL.md) |
| 指摘を同じ worktree で直すとき、または検証に渡す候補 SHA と再現条件を確定するときに使う。 | [再現と引き継ぎ](procedures/factory-implement-handoff/SKILL.md) |
