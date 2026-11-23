---
name: factory-pr-publish
description: 検証済みの候補を初めて PR として公開するとき、Walden 判定・対象差分・既存 PR を照合する。
---

# 検証済みの候補を PR として公開する

1. 実装担当の worktree で候補 SHA、ベース、差分、未コミットの変更、同じブランチの既存 PR を確認する。QA、該当するセキュリティ確認、未検証事項を候補 SHA に結びつける。
2. 統括が候補の worktree または PR を対象に、利用中の CLI に登録された `my-walden-review` を実行する。Codex ではその Skill の Codex 向け手順にも従う。Walden レビューを実行できない場合は、理由と確認できた範囲を伝え、対象リポジトリの PR ルールに従う。
3. `REQUEST_CHANGES` や、QA・セキュリティ確認で修正が必要になった項目は、[統括の指摘対応](../../../factory-orchestrate/SKILL.md#指摘対応)で扱う。`NEEDS_DISCUSSION` は判断が必要な点をユーザーに伝える。判定と残る未確認事項を踏まえて、依頼された PR 作成を進める。
4. リポジトリの PR テンプレートに沿って目的、変更、関連 Issue、検証結果、証跡、未確認事項を書く。依頼された範囲で候補を push し、同じブランチの PR があれば再利用する。PR URL と公開したコミット SHA を返す。マージはユーザーから依頼されたときに扱う。

GitHub CLI を使う場合は、対象リポジトリで `gh pr view <番号> --json url,author,baseRefName,headRefOid,headRefName` を読み、対象と作業記録を照合する。PR 本文には「何が変わるか」「その挙動をどの条件で確認したか」「残る未確認事項」を具体的に書く。証跡がローカルの絶対パスだけなら、PR 読者が読める結果の要約を本文に入れる。

## 判断例

公開直前に head が進んだら、検証済み SHA と新しい head の差分を確認する。候補が変わった場合は、その変更に必要な QA・レビューの結果をそろえて公開する。PR URL と実際に公開した SHA を組にして返す。

## 出典と採用した観点

公開前の差分・チェックの確認は Factory AI、Walden レビューの担当はこの Factory の設計による。[Factory-AI / create-pr](https://github.com/Factory-AI/factory-plugins/blob/e63e519a736140c86f37be95a529a0c44dc9a96e/plugins/code-review/skills/create-pr/SKILL.md)・[この Factory の Herdr 運用設計](../../../../docs/herdr-workflow.md)
