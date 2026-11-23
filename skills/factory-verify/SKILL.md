---
name: factory-verify
description: Factory の候補コミットを独立した QA セッションで検証し、動作証跡・未確認の条件・変更に関係する防御上の確認結果を返す。
---

# Factory の独立検証

指定の候補 SHA、比較元の必須チェック、受入条件を確認する。変更した使い方・設定は文書の手順でも試す。各条件に該当する手順を開く。

## Description から読む Skill を選ぶ

今の判断に合う行のリンクを開く。次の条件が生じたら、この表から選び直す。

| Description（使う場面） | 読む Skill・資料 |
| --- | --- |
| UI・CLI・API の操作を再現し、利用者から見える結果と証跡を記録する。 | [動作確認と証跡](procedures/factory-verify-qa-evidence/SKILL.md) |
| 候補が認可・外部入力・依存関係に影響するとき、変更範囲の防御上の確認結果を返す。 | [防御上の確認](procedures/factory-verify-security/SKILL.md) |
| Factory の Hook 判定の入力と観測結果の記載例が必要 | [Hook の検証例](references/hook-example.md) |
| 候補のテスト・モック・前提不足の結果を、受入条件ごとに合格・不合格・未確認へ分ける。 | [条件別の合否・未確認の判定](procedures/factory-verify-verdict/SKILL.md) |

統括へ候補 SHA、条件別の結果、コマンド・環境、証跡、指摘を返す。
