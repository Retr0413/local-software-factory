---
name: factory-investigate
description: Factory Issue について、コードの入口・影響範囲・既存テストを読み取り調査するとき、またはバージョンや環境による差を切り分けるときに使う。
---

# Factory 調査担当

対象コミットの README と作業ルールを確認し、問いに合う手順を開く。調査役は読み取りを担当する。

## Description から読む Skill を選ぶ

今の判断に合う行のリンクを開く。次の条件が生じたら、この表から選び直す。

| Description（使う場面） | 読む Skill・資料 |
| --- | --- |
| 報告された利用者操作から実際の入口・データ経路・対応する既存テストを特定する。 | [入口からテストまでの追跡](procedures/factory-investigate-trace/SKILL.md) |
| 更新後だけ、または特定環境だけで起きる症状について、解決済みの版と互換性の変化を調べる。 | [版と環境の比較](procedures/factory-investigate-versions/SKILL.md) |

統括に対象 SHA、根拠のファイル・行、再利用できる箇所、未確定の仮説を返す。実行や外部資料での追試が必要なら、その条件も渡す。
