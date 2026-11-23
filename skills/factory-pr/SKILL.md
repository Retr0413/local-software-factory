---
name: factory-pr
description: Publish or follow up on a Factory-managed GitHub PR when requested. Run the existing Walden review and return fixes to the original Herdr implementation session.
---

# Factory の PR 作成とフォローアップ

統括が、ユーザーの依頼に含まれる PR 作成、レビュー指摘や CI 失敗への対応に使う。対象リポジトリと Issue または PR、ベース、候補 SHA、元の Herdr 実装担当、許可された GitHub 操作を確認する。

## PR を作成する

1. 実装担当の worktree で候補 SHA、ベース、差分、未コミットの変更、同じブランチの既存 PR を確認する。QA、該当するセキュリティ確認、未検証事項を候補 SHA に結びつける。
2. 統括が候補の worktree または PR を対象に、利用中の CLI に登録された `my-walden-review` を実行する。Codex ではその Skill の Codex 向け手順にも従う。Walden レビューを実行できない場合は、理由と確認できた範囲を伝え、対象リポジトリの PR ルールに従う。
3. `REQUEST_CHANGES` や、QA・セキュリティ確認で修正が必要になった項目は、[統括の指摘対応](../factory-orchestrate/SKILL.md#指摘対応)で扱う。`NEEDS_DISCUSSION` は判断が必要な点をユーザーに伝える。判定と残る未確認事項を踏まえて、依頼された PR 作成を進める。
4. リポジトリの PR テンプレートに沿って目的、変更、関連 Issue、検証結果、証跡、未確認事項を書く。依頼された範囲で候補を push し、同じブランチの PR があれば再利用する。PR URL と公開したコミット SHA を返す。マージはユーザーから依頼されたときに扱う。

## 既存の PR に対応する

1. PR の作成者、現在の head SHA、未解決の指摘と CI の結果を確認する。他人の PR の扱いは `my-walden-review` の作成者判定に従う。CI の失敗原因はログで確認し、コード変更が必要なものと環境側の失敗を区別する。
2. 関連 Issue と [Factory の作業記録](../factory-record/SKILL.md) を使って元の Herdr 実装担当を特定する。担当が停止している場合は、同じ仕事の作業環境と会話を照合してから再開する。対応を依頼された指摘は、[統括の指摘対応](../factory-orchestrate/SKILL.md#指摘対応)で扱う。
3. push の前に、現在の PR の head が確認済みの head と一致し、公開するコミットが検証済みの候補 SHA と一致することを確かめる。新しい変更があれば対象と確認結果を見直す。必要な Walden レビューを経て依頼された範囲で PR を更新し、更新後の CI を確認する。再確認の結果と残る対応を作業記録に渡す。
