---
name: herdr-factory-dispatch
description: Factory の統括が Herdr で Codex・Claude Code の担当を起動するとき、既存の割り当てや送信不明のジョブを確認・再開するときに使う。
---

# Herdr で割り当てる

対象リポジトリと Issue またはジョブ名を特定し、現在の状態に合う手順を開く。

## Description から読む Skill を選ぶ

今の判断に合う行のリンクを開く。次の条件が生じたら、この表から選び直す。

| Description（使う場面） | 読む Skill・資料 |
| --- | --- |
| Herdr で新しい実装・調査・独立 QA のジョブを割り当てる。 | [ジョブの形式・起動例](procedures/herdr-factory-dispatch-launch/SKILL.md) |
| 割り当て済み、空き枠不足、送信不明、部分失敗のジョブを照合して再開する。 | [状態ごとの照合と復旧](procedures/herdr-factory-dispatch-recover/SKILL.md) |

統括にはジョブごとの agent、pane_id、cwd、state と、保留なら再開条件を返す。
