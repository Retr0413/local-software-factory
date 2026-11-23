---
name: factory-orchestrate
description: Coordinate implementation of GitHub Issues or named tasks through Local Software Factory in Herdr. Applies to ordinary requests such as Issueを実装してください and to explicit Factory invocations.
---

# Factory の統括

1. 依頼と既存の会話から対象リポジトリと Issue を特定する。Issue 番号だけの場合は、対象リポジトリを確認する。対象が特定できなければ質問する。Issue 調査だけの依頼は調査として扱う。
2. 目的、受入条件、作業範囲、依存関係を整理する。コードベースに調べるべき点があれば、先に [factory-investigate](../factory-investigate/SKILL.md) で調査する。独立した Issue は同じバッチにまとめる。依存する Issue は、先行変更を含む完全なコミット SHA を `base` に渡して起動する。
3. Herdr 内の統括ペインで、隣接する [herdr-factory-dispatch](../herdr-factory-dispatch/SKILL.md) の手順を使う。起動先の指定を優先し、指定がなければ統括と同じ CLI を使う。1 Issue または安定した ID を持つ1タスクにつき1実装担当を割り当てる。実装役には [factory-implement](../factory-implement/SKILL.md) の手順、受入条件、確認コマンド、承認された GitHub 操作を渡す。
4. Herdr で `mode: verify` と候補 SHA を `base` に指定し、実装担当とは別のペインで [factory-verify](../factory-verify/SKILL.md) を使う。受入条件とベースコミットを渡し、指定されたセキュリティ確認の範囲があれば添える。修正が必要な指摘は[指摘対応](#指摘対応)の手順で扱う。
5. 依頼に PR 作成や既存 PR への対応が含まれる場合は、Walden レビューの実施も含めて [factory-pr](../factory-pr/SKILL.md) の手順に進む。それ以外の実装依頼では、統括が `my-walden-review` を使う。
6. 完了または中断時は [factory-record](../factory-record/SKILL.md) で、検証結果、PR、手戻り、改善につながる観測を記録する。統括がテスト済みのコミット、未確認事項、Herdr の作業場所を伝える。

Herdr 外で実行を求められた場合は、対象と完了条件を整理できる範囲で進め、起動は意図した Herdr セッションの統括ペインから行う。子セッションでこの Skill を受け取った場合は、割り当てられた役割だけを実行する。

## 指摘対応

統括は、QA・セキュリティ確認・レビュー・CI で修正が必要になった項目を、該当箇所、期待する結果、確認方法とともに元の実装担当へ返す。新しい候補 SHA を受け取ったら、変更の影響を受ける確認とリポジトリで必須のチェックをやり直し、その SHA に結果をひも付ける。
