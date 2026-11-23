---
name: herdr-factory-dispatch-recover
description: 割り当て済み、空き枠不足、送信不明、部分失敗のジョブを照合して再開する。
---

# 割り当て・受領・起動状態を照合する

`herdr agent list` と `herdr agent read <agent> --source recent-unwrapped --lines 120` で状況を確認する。回答や許可の待機を尊重する。Herdr の待機状態に加え、報告、コミット、チェック結果を見て完了を判断する。

起動前に親の Herdr セッション名、workspace、対象リポジトリの `git rev-parse --show-toplevel` を照合する。復旧時は記録された作業場所で `git worktree list --porcelain` を読み、`worktree`・`branch`・`HEAD` を起動結果と突き合わせる。照合できた既存 worktree を Herdr から再開する。ユーザーに場所を伝えるときはセッション名と workspace・ペインを組にする。

| dispatch の返り値 | 統括が次に見るもの |
| --- | --- |
| `prompt_submitted` | 受領済みのプロンプトと担当の応答。候補コミットと報告が来てから作業結果を判定する |
| `existing_issue` | `recorded_state`、元のセッション、ブランチ。元のセッションで続きを依頼する。`recorded_state=prompt_unconfirmed` なら下の送信不明の行に従う |
| `capacity_limit` | 空き枠。バッチのうち未割り当ての仕事だけを保留する |
| `prepare_failed` / `start_failed` | 返却されたブランチ・ペインが実在するか、前景プロセスが起動済みか。途中まで作成された場所を特定する |
| `prompt_unconfirmed` | 記録されたセッションとペインの会話末尾を確認する。送信済みなら応答を待ち、未受領なら同じ担当へ送る。元セッションに接続できなければその仕事を保留する |

バッチで一部だけ失敗した場合は、プロセス全体の終了コードと各ジョブの結果を併せて読む。

worktree を閉じる場合は、未保存の変更や調査結果を確認し、自分が管理する作業場所だけを対象にする。

## 判断例

同じバッチで #10 が prompt_submitted、#11 が capacity_limit なら、#10 は元の担当を監視し、空き枠ができた時点で #11 だけを割り当てる。#10 の送信結果が不明なら、そのペインの会話末尾から受領を判定する。

## 出典と採用した観点

既存 worktree の検出は公開手順を参考にし、再開条件はローカルの台帳と返却状態から決めた。[openai / using-git-worktrees](https://github.com/openai/plugins/blob/981b02c0c44058b595f3b4180002c3ae3c806d40/plugins/superpowers/skills/using-git-worktrees/SKILL.md)・[この Factory の dispatch.py](../../scripts/dispatch.py)
