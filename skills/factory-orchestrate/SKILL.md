---
name: factory-orchestrate
description: Coordinate implementation of GitHub Issues or named tasks through Local Software Factory in Herdr. Applies to ordinary requests such as Issueを実装してください and to explicit Factory invocations.
---

# Factory の統括

1. 依頼と既存の会話から対象リポジトリと Issue を特定する。Issue 番号だけの場合は、対象リポジトリを確認する。対象が特定できなければ質問する。Issue 調査だけの依頼は調査として扱う。
2. 目的、受入条件、作業範囲、依存関係を整理する。独立した Issue は同じバッチにまとめる。依存する Issue は、先行変更を含む完全なコミット SHA を `base` に渡して起動する。
3. Herdr 内の統括ペインで、隣接する [herdr-factory-dispatch](../herdr-factory-dispatch/SKILL.md) の手順を使う。起動先の指定を優先し、指定がなければ統括と同じ CLI を使う。1 Issue または安定した ID を持つ1タスクにつき1実装担当を割り当てる。実装役には [factory-implement](../factory-implement/SKILL.md) の手順、受入条件、確認コマンド、承認された GitHub 操作を渡す。
4. 必要があれば [factory-investigate](../factory-investigate/SKILL.md) で調査を委任する。実装後はコミットを共有し、[factory-verify](../factory-verify/SKILL.md) を使って独立検証する。指摘は元の実装担当へ返し、変更後のコミットで必要な確認をやり直す。
5. 差分、テスト、証跡を確認する。PR や Issue への書き込みは依頼の範囲で行い、対象リポジトリの手順に従う。
6. 完了または中断時は [factory-record](../factory-record/SKILL.md) を使って記録する。統括がテスト済みのコミット、未確認事項、Herdr の作業場所を伝える。

Herdr 外で実行を求められた場合は、対象と完了条件を整理できる範囲で進め、起動は意図した Herdr セッションの統括ペインから行う。子セッションでこの Skill を受け取った場合は、割り当てられた役割だけを実行する。
