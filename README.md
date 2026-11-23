# Local Software Factory

Herdr 上の Codex と Claude Code を使って、GitHub Issue やローカルの開発タスクを進めるための Skill と Hook 集です。普段どおり「Issue #101 を実装してください」と依頼すると、統括セッションが完了条件と依存関係を確認し、Issue ごとに実装担当を1つずつ割り当てます。

- **独立した Issue を並行に進める。** Herdr が専用の Git worktree とペインを用意します。依存する Issue は、先行変更を含むコミットから順に始めます。
- **実装担当を固定する。** 同じ Issue を再依頼すると既存の割り当てを参照し、レビュー指摘への修正も元の担当に戻します。
- **実装結果を別の視点で確かめる。** 必要に応じて調査や独立検証を別セッションに任せ、対象コミットとともに検証結果や証跡を残します。

## セットアップ

**必要なもの**は Git、Python 3.9 以降、Herdr、認証済みの Codex CLI または Claude Code です。GitHub Issue を使う場合は、統括セッションに対象リポジトリと Issue を閲覧できる手段を用意します。

```sh
git clone https://github.com/Retr0413/local-software-factory.git
cd local-software-factory
python3 scripts/install.py
```

インストーラーは、既存の Hook と設定を保持しながら両方の CLI に登録します。片方だけ使う場合は `python3 scripts/install.py --client codex` または `python3 scripts/install.py --client claude` を実行します。

| CLI | Skill の登録先 | Hook の登録先 |
| --- | --- | --- |
| Codex | `~/.agents/skills/` | `~/.codex/hooks.json` |
| Claude Code | `~/.claude/skills/` | `~/.claude/settings.json` |

表は既定のパスです。Skill と Hook はこの clone 内のファイルを参照します。同じ場所で `git pull` すると中身を更新できます。Skill が増えたときはインストーラーを再実行して登録します。

インストール後は CLI を新しく起動します。Codex が Hook の承認を求めた場合は、`/hooks` で `user_prompt_submit.py` を確認して許可します。[Codex の Hook 設定](https://learn.chatgpt.com/docs/hooks#review-and-trust-hooks)

## Issue を実装する

1. **対象プロジェクトを開く。** Herdr のペインで実装対象の Git リポジトリに移動し、`codex` または `claude` を起動します。このセッションが統括になります。worktree の出発点は既定で対象リポジトリの `HEAD` です。
2. **普段の言葉で依頼する。** 実装依頼を1行目に書くと Hook が拾います。依存関係や実装担当の指定は2行目以降に書けます。対象 Issue が会話で決まっていれば「普通にIssueを実装して下さい。」でも起動できます。

   ```text
   Issue #101 と #102 を実装してください。
   #102 は #101 に依存します。#101 は Codex、#102 は Claude Code に割り当ててください。
   ```

3. **進捗を確認する。** 統括に進捗を聞くか、同じ Herdr セッションのシェルで `herdr agent list` を実行します。出力にあるエージェント名を使って `herdr agent read <名前> --source recent-unwrapped --lines 120` で詳細を確認できます。
4. **結果を受け取る。** 統括から変更内容、対象コミット、検証結果、残る課題を受け取ります。PR 作成まで依頼したい場合は、その旨も依頼に含めます。

実装担当の CLI を指定しなければ、統括と同じ CLI が選ばれます。

## Skill を明示的に呼び出す

登録済みの Skill は、Codex では `$名前`、Claude Code では `/名前` を会話に入力して指定できます。Herdr で新しい実装セッションを起動する場合は、対象プロジェクトを開いた Herdr 内の統括ペインから依頼します。

| やりたいこと | Codex での入力例 | Claude Code での入力例 |
| --- | --- | --- |
| Issue を実装する | `$factory-orchestrate Issue #101 を実装してください` | `/factory-orchestrate Issue #101 を実装してください` |
| 影響範囲を調べる | `$factory-investigate Issue #101 の影響範囲と既存テストを調べてください` | `/factory-investigate Issue #101 の影響範囲と既存テストを調べてください` |
| 既存 PR の CI を調べる | `$factory-pr PR #45 の CI 失敗の原因を調べてください` | `/factory-pr PR #45 の CI 失敗の原因を調べてください` |

Issue 番号の代わりにローカルタスクの目的と完了条件も渡せます。実装、検証、Herdr 起動、記録の各 Skill は、通常は統括が必要な作業情報を添えて使います。

## 仕組み

```text
Issue 実装の依頼
    ↓
UserPromptSubmit Hook または統括 Skill の明示起動
    ↓
統括が対象・受入条件・依存関係を整理
    ↓
Herdr が worktree を作成 → CLI を起動 → タスクを送信
    ↓
実装担当がコード・テスト・文書を変更
    ↓
候補コミット ⇄ QA・セキュリティ確認・Walden レビュー
    ↓
依頼に応じて PR 作成・フォローアップ
    ↓
検証結果・停止理由・改善につながる観測を記録
```

Hook は依頼の1行目を判定し、統括に手順を追加します。対象や依存関係を判断して Herdr に仕事を渡すのは統括です。Plan モードと Factory が作成した子 worktree では、Hook による自動振り分けを抑止します。

## 7つの Skill の役割と出典

公開 Skill から取り入れた観点は、ローカルでの担当と引き継ぎに合わせて組み込んでいます。各社の原本、採用した手順と理由は[比較調査](docs/skill-survey.md)で確認できます。

| Skill | 担当と確認すること | 土台・参考資料 |
| --- | --- | --- |
| [`factory-orchestrate`](skills/factory-orchestrate/SKILL.md) | Issue の受入条件と依存関係を整理し、1タスクに1実装担当を割り当てる | この Factory の統括手順 |
| [`herdr-factory-dispatch`](skills/herdr-factory-dispatch/SKILL.md) | worktree とペインを用意し、Codex または Claude Code を起動する。既存の割り当ても確認する | ローカルの `herdr-parallel` と [Herdr CLI](https://herdr.dev/) |
| [`factory-investigate`](skills/factory-investigate/SKILL.md) | 処理の入口、影響範囲、再利用できる実装、既存テストを調べ、根拠を統括へ返す | Cognition の [codebase-onboarding](https://github.com/CognitionAI/windsurf-demo/tree/main/.windsurf/skills/codebase-onboarding) |
| [`factory-implement`](skills/factory-implement/SKILL.md) | コードを変更し、必要な回帰テストと利用手順を更新する。指摘修正も元の担当が受け持つ | Cognition の [generate-tests](https://github.com/CognitionAI/windsurf-demo/tree/main/.windsurf/skills/generate-tests) と [readme-hygiene](https://github.com/CognitionAI/team-marketplace-template/tree/main/plugins/docs-and-release/skills/readme-hygiene) |
| [`factory-verify`](skills/factory-verify/SKILL.md) | 別セッションで候補コミットを確認する。受入条件、UI・CLI・API の動作証跡、利用手順、変更に関係するセキュリティ項目を見る | Factory AI の [droid-control](https://github.com/Factory-AI/factory-plugins/tree/master/plugins/droid-control/skills/droid-control) と Cognition の [dependency-audit](https://github.com/CognitionAI/team-marketplace-template/tree/main/plugins/security-guardrails/skills/dependency-audit) |
| [`factory-pr`](skills/factory-pr/SKILL.md) | 検証済みのコミットを PR にひも付け、作成・更新、レビュー指摘、CI 失敗に対応する | Factory AI の [create-pr](https://github.com/Factory-AI/factory-plugins/tree/master/plugins/code-review/skills/create-pr) と [follow-up-on-pr](https://github.com/Factory-AI/factory-plugins/tree/master/plugins/code-review/skills/follow-up-on-pr) |
| [`factory-record`](skills/factory-record/SKILL.md) | 結果、証跡の参照、停止理由、手戻りを蓄積する | この Factory の記録手順。[Walden Yan と Zach Lloyd の講演](docs/references.md#code-summit-と関連講演)を参考にした |

QA は指摘と証跡を統括に渡します。統括は[共通の指摘対応手順](skills/factory-orchestrate/SKILL.md#指摘対応)で修正を元の実装担当へ戻し、新しい候補コミットで必要な確認を行います。PR を扱う依頼では `factory-pr` から、それ以外の実装依頼では統括から、別途登録した `my-walden-review` を呼び出します。

統括が記録 Skill を使うと、対象リポジトリの共通 Git ディレクトリ内の `local-software-factory/runs.jsonl` に追記されます。各 worktree から共通 Git ディレクトリを確認するには `git rev-parse --path-format=absolute --git-common-dir` を実行します。現段階の改善機能は情報の蓄積までです。

## 起動や再開で困ったとき

| 状況 | 確認すること |
| --- | --- |
| 依頼を送っても起動しない | 統括を Herdr 内のペインで開き、実装依頼を1行目に書きます。Codex では `/hooks` の承認状態を確認します。明示起動も使えます。 |
| `existing_issue` が返った | 登録済みの担当です。結果にある Herdr セッションとエージェント名で、元の作業を確認します。 |
| `capacity_limit` が返った | Factory と `herdr-parallel` が共有する、その Herdr セッションの起動枠が埋まっています。枠が空いてから対象タスクを再依頼します。 |
| 起動や指示送信の結果が不明 | 再送前に元のペインと会話を確認します。認証やツールの許可を待っている場合は、該当 CLI 上で対応します。 |

## 詳細と開発

- [Factory 全体設計](docs/architecture.md)
- [Herdr の実行フローと復旧](docs/herdr-workflow.md)
- [検証と情報の蓄積](docs/verification-and-records.md)
- [Code Summit の講演と各 CLI の参考資料](docs/references.md)

このリポジトリの Hook、インストーラー、起動時の再試行は、次のコマンドで確認できます。

```sh
python3 -B -m unittest discover -s tests -v
```
