---
name: factory-record-resume
description: 中断していた仕事を再開するとき、記録から元の担当・候補・未確認条件を取り出す。
---

# 作業記録から元の担当と再開条件を特定する

対象 worktree で次のコマンドを実行する。例の `#101` を台帳で使ったタスク ID に置き換える。

```sh
records="$(git rev-parse --path-format=absolute --git-common-dir)/local-software-factory/runs.jsonl"
jq -c --arg task "#101" 'select(.task == $task)' "$records"
```

同じタスクの候補 SHA と未確認条件を拾い、現在のブランチ・PR・Herdr セッションと突き合わせる。作業途中で候補が変わっていれば、前の結果が適用できる範囲を示す。

記録が見つからなければ、Issue・PR と Herdr の実行状態から担当を照合し、確認できた範囲を統括に返す。

## 判断例

記録に候補 A の QA 成功があり、現在の PR は候補 B の場合、元のセッションと A→B の変更を照合する。「A で確認済み」と「B で追試が必要」を分けて引き継ぐ。

## 出典と採用した観点

共有 Git メタデータでの保存方法と元の担当で再開する設計を組み合わせた。[この Factory の record.py](../../scripts/record.py)・[この Factory の Herdr 運用設計](../../../../docs/herdr-workflow.md)
