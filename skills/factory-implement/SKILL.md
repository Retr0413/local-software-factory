---
name: factory-implement
description: Implement an assigned Factory Issue in its worktree, update affected tests and documentation, and fix findings in the same session.
---

# Factory 実装担当

1. Issue、受入条件、作業範囲、ベースコミットを確認する。既存実装とリポジトリのルールに沿って変更する。調査や判断が必要なら、問いと根拠を統括に返す。
2. Issue の挙動を検証できるテストを選ぶ。既存テストでカバーできない回帰や追加した動作には、必要に応じてテストを加える。関連する既存テストとプロジェクト指定のチェックを実行する。
3. 起動方法、設定、API、ユーザー操作が変わる場合は、該当する README や利用手順とコードを同じ候補に含める。手順や例を実際のコマンドと照合する。リリースノートの記載は、依頼やリポジトリの規約に該当するときに行う。

検証に渡す候補のコミット SHA、変更の概要、実行したチェックと結果、文書の更新箇所、未確認事項を報告する。QA・Walden レビュー・PR・CI からの指摘への修正は同じ会話と worktree で行い、新しい候補コミットと再検証結果を統括に返す。
