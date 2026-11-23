# Local Software Factory

Herdr、Codex、Claude Code を使い、ローカルでソフトウェア開発の調査・実装・検証を進める Factory です。

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

## セットアップ

Herdr と対象の CLI を利用できる環境で、このリポジトリを clone し、次を実行します。Python 3.9 以降が必要です。

```sh
python3 scripts/install.py
```

Codex と Claude Code に共通の Skill とユーザー用 Hook を登録します。片方だけに登録する場合は `--client codex` または `--client claude` を指定できます。登録済み Hook は維持されます。Skill はこの clone へのリンクなので、同じ場所に置いて更新します。

Herdr 内で対象プロジェクトを開き、Codex または Claude Code を起動します。Codex が新しい Hook の確認を求めたら `/hooks` から `user_prompt_submit.py` を確認して有効にします。 [Codex の Hook 設定](https://learn.chatgpt.com/docs/hooks#review-and-trust-hooks)

次のように依頼すると、統括が対象 Issue を確認して Factory の実装を始めます。

```text
Issue #101 と #102 を実装してください。
```

会話に対象 Issue がある場合は、「普通にIssueを実装して下さい。」でもその Issue を使います。Codex は `$factory-orchestrate`、Claude Code は `/factory-orchestrate` で明示的にも呼び出せます。

失敗、指摘、検証結果は対象リポジトリの共通 Git ディレクトリ内に記録します。集めた情報の分析と改善の自動化は、後続の設計対象です。
