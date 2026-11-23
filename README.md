# Local Software Factory

Herdr、Codex、Claude Code を使い、ローカルでソフトウェア開発の調査・実装・検証を進めるための設計です。

人間の依頼や GitHub Issue を受け、統括が仕事と依存関係を整理します。Issue または独立したタスクごとに1つの実装セッションと worktree を割り当て、調査・QA・レビューで支援します。検証結果や改善につながる情報は、後から参照できるよう記録します。

```text
依頼 / GitHub Issue
        ↓
統括 ── 依存関係と完了条件を整理
        ↓
Issue 単位の担当セッションと worktree
        ↓
調査 → 実装 → QA・独立レビュー → PR
        ↓
作業結果・証跡・改善情報を蓄積
```

## ドキュメント

- [Factory 全体設計](docs/architecture.md)
- [Herdr と実行フロー](docs/herdr-workflow.md)
- [検証と情報の蓄積](docs/verification-and-records.md)
- [参考資料](docs/references.md)

このリポジトリは構想と設計を記録するものです。Skill、Hook、Factory 本体は今後の設計・実装対象です。
