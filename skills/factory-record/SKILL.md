---
name: factory-record
description: Save Factory task outcomes, evidence references, blockers and improvement observations in the local repository's shared Git metadata.
---

# Factory の作業記録

統括セッションから、対象リポジトリで `scripts/record.py` に報告を JSON オブジェクトとして渡す。必須項目は `task` と `outcome`。対象コミット、担当 セッション名、検証結果、証跡の参照、失敗や停止の理由、改善につながる観測事項を分かる範囲で加える。

ログ全文や認証情報を含めず、必要な証跡の参照と短い要約を記録する。スクリプトが返すパスを使って人が後から参照できるようにする。
