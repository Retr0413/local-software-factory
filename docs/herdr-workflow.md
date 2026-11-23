# Herdr を使う実行フロー

## 利用の考え方

Herdr はローカルのワークスペース、タブ、ペイン、エージェント、Git worktree を管理する。Factory の統括がタスクと依存関係を判断し、Herdr のコマンドを使って実装や支援のセッションを操作する。

確認時の Herdr は `herdr agent start --kind codex` と `--kind claude` を公開している。起動引数や動作はインストールされたバージョンのヘルプで確認する。Herdr からセッションを起動できることと、両 CLI の Skill、Hook、権限、認証の挙動が同一であることは別の検証事項である。

## タスクの開始から終了まで

1. 統括は対象リポジトリ、Issue またはローカルタスク、目的、受入条件、依存関係を確認する。
2. 独立して実装できるタスクに、個別の worktree と実装セッションを割り当てる。対象のベースコミットを記録する。
3. 必要な調査や QA の準備を行い、結果を担当へ渡す。
4. 担当が実装し、既存テストと必要な回帰テストを実行する。利用手順や設定が変われば同じ worktree で文書を更新する。
5. QA は候補 SHA をベースとする別 worktree から受入条件を確認する。変更に応じてセキュリティ確認も行う。修正が必要な指摘は[統括の共通手順](../skills/factory-orchestrate/SKILL.md#指摘対応)で扱う。
6. PR を扱う依頼では、[`factory-pr`](../skills/factory-pr/SKILL.md) の手順で Walden レビューから GitHub 操作まで進める。PR を扱わない実装依頼では、統括が `my-walden-review` を使う。
7. 実行結果を記録し、セッションと worktree の後始末を適切に行う。

## 起動と観測

インストール済み CLI のヘルプで構文を確認し、Herdr が返す workspace、pane、agent の ID を使用する。主な操作は `herdr worktree create`、`herdr agent start`、`herdr agent prompt`、`herdr agent list`、`herdr agent read`、`herdr agent wait` である。

起動の受領はタスク完了を意味しない。状態、出力、実際の差分と検証結果を確認する。起動結果が不明なときは、再起動前に既存セッションと worktree を調べる。停止や再開も担当の識別情報に結びつける。

## 明示起動と Hook

両 CLI の `UserPromptSubmit` Hook が「Issue #101 を実装してください」などの依頼に統括 Skill の指示を加える。明示起動の場合は統括 Skill を直接指定する。統括は依存関係を確認した後、Herdr 起動 Skill のスクリプトに仕事を渡す。Hook は Factory の子 worktree と Plan モードを対象外にする。

起動スクリプトは `herdr worktree create` の応答からペインを取り、`herdr agent start` と `herdr agent prompt` を順に実行する。登録先は `kind` で選べる。Issue の同時起動枠と割り当ては既存の `herdr-parallel` と共有する。登録済み Issue の状態は、元の Herdr セッションで確認する。

## 終了と復旧

タスク完了後も、未コミットの変更や未確認の成果を失わないよう、状態を確認してから、この Factory が作成したセッションと worktree を整理する。処理途中の失敗、重複起動、依存タスク待ち、認証・承認待ちを記録する。再実行が既存の割り当てを返したら、その `recorded_state`、ブランチ、ペインを照合し、元の担当に指示を追加する。送信結果が不明な場合は会話を見て受領済みか確認する。Herdr の待機状態と作業の完了は別々に確認する。
