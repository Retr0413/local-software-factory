---
name: factory-orchestrate
description: Coordinate implementation of GitHub Issues or named tasks through Local Software Factory in Herdr. Applies to ordinary requests such as Issueを実装してください and to explicit Factory invocations.
---

# Factory の統括

1. 依頼と既存の会話から対象リポジトリと Issue を特定する。Issue 番号だけの場合は、対象リポジトリを確認する。対象が特定できなければ質問する。Issue 調査だけの依頼は調査として扱う。
2. 目的、受入条件、作業範囲、依存関係を整理する。コードベースに調べるべき点があれば、先に [factory-investigate](../factory-investigate/SKILL.md) で調査する。独立した Issue は同じバッチにまとめる。依存する Issue は、先行変更を含む完全なコミット SHA を `base` に渡して起動する。
3. Herdr 内の統括ペインで、隣接する [herdr-factory-dispatch](../herdr-factory-dispatch/SKILL.md) の手順を使う。起動先の指定を優先し、指定がなければ統括と同じ CLI を使う。1 Issue または安定した ID を持つ1タスクにつき1実装担当を割り当てる。実装役には [factory-implement](../factory-implement/SKILL.md) の手順、受入条件、確認コマンド、承認された GitHub 操作を渡す。
4. Herdr で `mode: verify` と候補 SHA を `base` に指定し、実装担当とは別のペインで [factory-verify](../factory-verify/SKILL.md) を使う。受入条件とベースコミットを渡し、認証、権限、外部入力、依存関係などに影響があればセキュリティ確認の対象も指定する。指摘は元の実装担当へ返し、変更後のコミットで該当する確認をやり直す。
5. コードレビューは、統括が既存の `my-walden-review` で進める。依頼に PR 作成や既存 PR の対応が含まれる場合は、レビューの実施から GitHub 操作まで [factory-pr](../factory-pr/SKILL.md) の手順を使う。
6. 完了または中断時は [factory-record](../factory-record/SKILL.md) で、検証結果、PR、手戻り、改善につながる観測を記録する。統括がテスト済みのコミット、未確認事項、Herdr の作業場所を伝える。

Herdr 外で実行を求められた場合は、対象と完了条件を整理できる範囲で進め、起動は意図した Herdr セッションの統括ペインから行う。子セッションでこの Skill を受け取った場合は、割り当てられた役割だけを実行する。
