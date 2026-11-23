---
name: factory-pr
description: Factory の PR 作成・更新を依頼されたとき、または既存 PR の CI 失敗・未解決スレッドを調査して元の担当へ返すときに使う。
---

# Factory の PR 作成とフォローアップ

統括が、ユーザーの依頼に含まれる PR 作成、レビュー指摘や CI 失敗への対応に使う。対象リポジトリと Issue または PR、ベース、候補 SHA、元の Herdr 実装担当、許可された GitHub 操作を確認する。

## Description から読む Skill を選ぶ

今の判断に合う行のリンクを開く。次の条件が生じたら、この表から選び直す。

| Description（使う場面） | 読む Skill・資料 |
| --- | --- |
| 検証済みの候補を初めて PR として公開するとき、Walden 判定・対象差分・既存 PR を照合する。 | [Walden レビューと PR 作成](procedures/factory-pr-publish/SKILL.md) |
| 既存 PR に修正を反映する依頼を受け、元の実装担当・現在の head・再確認範囲を特定する。 | [元の担当への引き継ぎと更新](procedures/factory-pr-follow-up/SKILL.md) |
| PR のチェック失敗・結果待ち・再試行・古い実行が混在するとき、現在の head について判定する。 | [CI の切り分け](procedures/factory-pr-ci/SKILL.md) |
| 既存 PR の古い差分・重複・部分取得を含むレビュー指摘から、現行 head での残件を特定する。 | [レビュースレッドの確認](procedures/factory-pr-review-threads/SKILL.md) |

調査結果には対象 PR と head を添える。公開・返信・マージは依頼された操作の範囲に従う。
