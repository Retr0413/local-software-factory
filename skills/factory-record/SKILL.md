---
name: factory-record
description: Save Factory task outcomes, evidence references, blockers and improvement observations in the local repository's shared Git metadata.
---

# Factory の作業記録

統括セッションから、対象リポジトリで `scripts/record.py` に報告を JSON オブジェクトとして渡す。必須項目は `task` と `outcome`。完了・保留・中断のいずれでも、分かる情報を記録する。

- `agent` と `herdr_session` に元の実装担当を、`candidate_commit` に確認した候補を、`pr` に関連する PR の URL を残す。
- `checks` と `evidence` に確認結果と証跡の参照を残す。検証用 worktree を片付ける場合は、必要な証跡を後から参照できる場所に保存する。
- `observations` に停止や手戻りの原因、再発した指摘、起動手順の不足などを、発生した工程と根拠とともに残す。推測は推測と分かるように書く。

ログ全文や認証情報を含めず、必要な参照と要約を保存する。改善ループの範囲は観測の蓄積まで。作業を引き継ぐときは記録と Herdr の実行状態を照合する。
