# 公開 Skill 調査と採否

GitHub の公開組織7件から、汎用 Skill カタログ、公式プラグイン配布、以前に参照したサンプル、Issue 修正用の関連コレクションを合わせて13リポジトリ選んだ。各既定ブランチのコミットを固定し、Git ツリー上のファイル名が厳密に `SKILL.md` となる全990パスを列挙した。本文バイト列の SHA-256 は986種類。テンプレートや外部作者が提供したプラグインも配布元の件数に含む。

全件から名前・パス・description を抽出し、回帰、CI、レビュー、受入条件、worktree、引き継ぎ等の用語で候補を抽出した。既知の出典と関連する同系列の Skill を手作業で追加した。一次候補は83パス。うち35件について下表に本文または特定箇所を照合した理由を示す。残る一次候補は用途・見出しで選別した。残りの全件はメタデータ段階の選別。企業の全リポジトリ、社内限定 Skill、名前の異なる独自フォーマットは集計範囲外。

[全件の目録と調査深度](skill-inventory.csv)。「本文＋補助資料」は本文と下記の関連資料、「節」は対象に関係する記述の確認を表す。各社のスクリプトは実行せずに参照し、手順は日本語でローカル向けに記述した。

| 固定したリポジトリ | SKILL.md |
| --- | ---: |
| [openai/skills](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431) | 44 |
| [openai/plugins](https://github.com/openai/plugins/tree/981b02c0c44058b595f3b4180002c3ae3c806d40) | 541 |
| [anthropics/skills](https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba) | 20 |
| [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/73c8cf3ea7e296057b467990f2f5d61b4c922260) | 57 |
| [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins/tree/0e0fcacddcc892eb92a1b7873ff9d68159c47571) | 252 |
| [Factory-AI/factory-plugins](https://github.com/Factory-AI/factory-plugins/tree/e63e519a736140c86f37be95a529a0c44dc9a96e) | 17 |
| [Factory-AI/skills](https://github.com/Factory-AI/skills/tree/21a74dec467a1424e3e067712d004cd987d6a0ce) | 6 |
| [CognitionAI/windsurf-demo](https://github.com/CognitionAI/windsurf-demo/tree/d4e661ab8b52c0b3c1d6099292d6f415fcd755b8) | 4 |
| [CognitionAI/team-marketplace-template](https://github.com/CognitionAI/team-marketplace-template/tree/2169376ccdf4ebb84a166f867be176b194fa0361) | 5 |
| [google-gemini/gemini-skills](https://github.com/google-gemini/gemini-skills/tree/c4d0c62c1240e08a90546186bf320600ab6a039a) | 4 |
| [huggingface/skills](https://github.com/huggingface/skills/tree/5291c2b9365e06b175dc04817610c778623f4836) | 26 |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills/tree/5a37a6329fbad3666c3207392a6a7c0110e92efb) | 9 |
| [vercel-labs/next-maintainer-skills](https://github.com/vercel-labs/next-maintainer-skills/tree/7996fe9b91e6fbcba7d892a9540446c3572a1a10) | 5 |

## 工程ごとの採否

| 担当 | 原本 | 確認範囲 | 採否と根拠 |
| --- | --- | --- | --- |
| 統括 | [openai / define-goal](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/define-goal/SKILL.md) | 本文 | 性能・調査の完了条件を追加。専用 goal 操作は起動フローの対象外 |
| 統括 | [openai / dispatching-parallel-agents](https://github.com/openai/plugins/blob/981b02c0c44058b595f3b4180002c3ae3c806d40/plugins/superpowers/skills/dispatching-parallel-agents/SKILL.md) | 本文 | 独立性と明確な引き継ぎは統括が既に担当。追加の並列化指示を省略 |
| Herdr 起動 | [openai / using-git-worktrees](https://github.com/openai/plugins/blob/981b02c0c44058b595f3b4180002c3ae3c806d40/plugins/superpowers/skills/using-git-worktrees/SKILL.md) | 節 | 復旧時の worktree / branch 照合に採用。新しい worktree を作る機能は既存 dispatcher が担当 |
| 調査 | [CognitionAI / codebase-onboarding](https://github.com/CognitionAI/windsurf-demo/blob/d4e661ab8b52c0b3c1d6099292d6f415fcd755b8/.windsurf/skills/codebase-onboarding/SKILL.md) | 本文＋補助資料 | 入口・データ経路と実行前提の調査は既存手順に統合 |
| 調査 | [anthropics / debug](https://github.com/anthropics/knowledge-work-plugins/blob/0e0fcacddcc892eb92a1b7873ff9d68159c47571/engineering/skills/debug/SKILL.md) | 本文 | 症状・直近の差分・仮説を切り分ける。実行が必要な確認を QA へ渡す |
| 調査 | [CognitionAI / migration-helper](https://github.com/CognitionAI/windsurf-demo/blob/d4e661ab8b52c0b3c1d6099292d6f415fcd755b8/.windsurf/skills/migration-helper/SKILL.md) | 本文＋補助資料 | 解決済みバージョン・旧 API の利用箇所・挙動変更を特定する手順を採用 |
| 実装 | [CognitionAI / generate-tests](https://github.com/CognitionAI/windsurf-demo/blob/d4e661ab8b52c0b3c1d6099292d6f415fcd755b8/.windsurf/skills/generate-tests/SKILL.md) | 本文＋補助資料 | 既存テストの入力・期待値・独立性を実装担当の確認に集約 |
| 実装 | [anthropics / testing-strategy](https://github.com/anthropics/knowledge-work-plugins/blob/0e0fcacddcc892eb92a1b7873ff9d68159c47571/engineering/skills/testing-strategy/SKILL.md) | 本文 | 境界をまたぐ契約とデータ処理の再実行に適したテスト選択を追加 |
| 実装 | [vercel-labs / nextjs-create-regression-test](https://github.com/vercel-labs/next-maintainer-skills/blob/7996fe9b91e6fbcba7d892a9540446c3572a1a10/skills/nextjs-create-regression-test/SKILL.md) | 本文 | アサーションが期待する理由で失敗することを確認。Next.js 固有の canary 要件は対象外 |
| 実装 | [CognitionAI / release-notes](https://github.com/CognitionAI/team-marketplace-template/blob/2169376ccdf4ebb84a166f867be176b194fa0361/plugins/docs-and-release/skills/release-notes/SKILL.md) | 本文 | 互換性に影響する変更には利用者の移行手順を載せる |
| 実装 | [CognitionAI / readme-hygiene](https://github.com/CognitionAI/team-marketplace-template/blob/2169376ccdf4ebb84a166f867be176b194fa0361/plugins/docs-and-release/skills/readme-hygiene/SKILL.md) | 本文 | README と実コマンドの照合は既存。追加のドキュメント担当を設けない |
| 実装 | [anthropics / documentation](https://github.com/anthropics/knowledge-work-plugins/blob/0e0fcacddcc892eb92a1b7873ff9d68159c47571/engineering/skills/documentation/SKILL.md) | 本文 | 公開 API の入力・応答例を採用。Quickstart の全案件への強制は対象外 |
| QA | [vercel-labs / nextjs-reproduce-issue](https://github.com/vercel-labs/next-maintainer-skills/blob/7996fe9b91e6fbcba7d892a9540446c3572a1a10/skills/nextjs-reproduce-issue/SKILL.md) | 本文 | 報告された版・操作・実測を比較条件に反映 |
| QA | [vercel-labs / nextjs-verify-canary](https://github.com/vercel-labs/next-maintainer-skills/blob/7996fe9b91e6fbcba7d892a9540446c3572a1a10/skills/nextjs-verify-canary/SKILL.md) | 本文 | ベースが再現しない場合と、準備に失敗した場合の判定を追加 |
| 調査・QA | [vercel-labs / nextjs-bisect-regression](https://github.com/vercel-labs/next-maintainer-skills/blob/7996fe9b91e6fbcba7d892a9540446c3572a1a10/skills/nextjs-bisect-regression/SKILL.md) | 本文 | 両端を判定できないときの因果推定を保留。全案件での bisect は対象外 |
| QA | [anthropics / webapp-testing](https://github.com/anthropics/skills/blob/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/webapp-testing/SKILL.md) | 本文＋補助資料 | 描画後の操作対象の特定を採用 |
| QA | [openai / playwright](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/playwright/SKILL.md) | 本文 | 遷移後に操作対象を取り直す手順を既存 QA 資料に統合 |
| QA | [Factory-AI / droid-control](https://github.com/Factory-AI/factory-plugins/blob/e63e519a736140c86f37be95a529a0c44dc9a96e/plugins/droid-control/skills/droid-control/SKILL.md) | 本文＋補助資料 | 画像・動画を開き主張と実際の値を照合。撮影環境の導入は対象外 |
| QA | [anthropics / skill-creator](https://github.com/anthropics/skills/blob/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/skill-creator/SKILL.md) | 節＋補助資料 | grader の成果物・期待値の照合を QA に反映。専任の評価担当は追加しない |
| QA・PR | [openai / test-triage](https://github.com/openai/plugins/blob/981b02c0c44058b595f3b4180002c3ae3c806d40/plugins/build-macos-apps/skills/test-triage/SKILL.md) | 本文 | セットアップとアサーションの失敗は既存の QA / CI 手順がカバー。macOS 専用コマンドは対象外 |
| QA | [CognitionAI / dependency-audit](https://github.com/CognitionAI/team-marketplace-template/blob/2169376ccdf4ebb84a166f867be176b194fa0361/plugins/security-guardrails/skills/dependency-audit/SKILL.md) | 本文 | 依存グラフを確認する手順はセキュリティ参照資料が担当 |
| PR | [Factory-AI / create-pr](https://github.com/Factory-AI/factory-plugins/blob/e63e519a736140c86f37be95a529a0c44dc9a96e/plugins/code-review/skills/create-pr/SKILL.md) | 本文 | リポジトリ固有の必須チェックと PR テンプレートを優先。固定の書式を追加しない |
| PR | [Factory-AI / follow-up-on-pr](https://github.com/Factory-AI/factory-plugins/blob/e63e519a736140c86f37be95a529a0c44dc9a96e/plugins/code-review/skills/follow-up-on-pr/SKILL.md) | 本文 | 解決済み・未解決の区別をスレッド対応に統合。一律の rebase や外部投稿は対象外 |
| PR | [openai / gh-address-comments](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/gh-address-comments/SKILL.md) | 本文＋補助資料 | スレッド単位のページング・古い差分の識別を独自の読み取り専用ヘルパーに導入 |
| PR | [openai / gh-fix-ci](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/gh-fix-ci/SKILL.md) | 本文 | GitHub Actions と外部 CI の区別は既存の CI 表が担当 |
| レビュー | [CognitionAI / git-pr-review](https://github.com/CognitionAI/windsurf-demo/blob/d4e661ab8b52c0b3c1d6099292d6f415fcd755b8/.windsurf/skills/git-pr-review/SKILL.md) | 本文 | 差分のレビューは既存 Walden が担当。第二のレビュー経路を追加しない |
| 記録 | [anthropics / session-report](https://github.com/anthropics/claude-plugins-official/blob/73c8cf3ea7e296057b467990f2f5d61b4c922260/plugins/session-report/skills/session-report/SKILL.md) | 本文 | CLI 固有の会話集計と HTML 化は対象外。記録は既存 runs.jsonl に集約 |
| 記録 | [anthropics / receipts](https://github.com/anthropics/claude-plugins-official/blob/73c8cf3ea7e296057b467990f2f5d61b4c922260/plugins/receipts/skills/receipts/SKILL.md) | 節 | 共有履歴の二重計上回避、不明とゼロの区別を記録手順へ反映 |
| 対象外 | [huggingface / hf-mem](https://github.com/huggingface/skills/blob/5291c2b9365e06b175dc04817610c778623f4836/skills/hf-mem/SKILL.md) | 本文 | 用途は GPU メモリ見積り。汎用の作業記録とは異なる |
| 対象外 | [huggingface / huggingface-community-evals](https://github.com/huggingface/skills/blob/5291c2b9365e06b175dc04817610c778623f4836/skills/huggingface-community-evals/SKILL.md) | 節 | モデルとデータセットの評価。今回の汎用 QA の比較は既存手順が担当 |
| 対象外 | [google-gemini / gemini-api-cli](https://github.com/google-gemini/gemini-skills/blob/c4d0c62c1240e08a90546186bf320600ab6a039a/skills/gemini-api-cli/SKILL.md) | 節 | Gemini API を呼び出す CLI。汎用の工程に製品依存を持ち込まない |
| 統括 | [anthropics / write-spec](https://github.com/anthropics/knowledge-work-plugins/blob/0e0fcacddcc892eb92a1b7873ff9d68159c47571/product-management/skills/write-spec/SKILL.md) | 節 | 前提・操作・期待値への分解は統括の受入条件でカバー |
| 調査 | [openai / systematic-debugging](https://github.com/openai/plugins/blob/981b02c0c44058b595f3b4180002c3ae3c806d40/plugins/superpowers/skills/systematic-debugging/SKILL.md) | 節 | 仮説を区別する最小の観測は調査担当が既に記載 |
| 記録 | [Factory-AI / autoresearch](https://github.com/Factory-AI/factory-plugins/blob/e63e519a736140c86f37be95a529a0c44dc9a96e/plugins/autoresearch/skills/autoresearch/SKILL.md) | 節 | 実験ループは対象外。試した条件と結果の蓄積は記録担当に集約 |
| 実装 | [vercel-labs / nextjs-fix-issue](https://github.com/vercel-labs/next-maintainer-skills/blob/7996fe9b91e6fbcba7d892a9540446c3572a1a10/skills/nextjs-fix-issue/SKILL.md) | 本文 | 期待する失敗と修正後の結果は回帰テスト手順に集約 |

## 照合した補助資料

- [gh-address-comments/scripts/fetch_comments.py](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/gh-address-comments/scripts/fetch_comments.py)
- [webapp-testing/examples/element_discovery.py](https://github.com/anthropics/skills/blob/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/webapp-testing/examples/element_discovery.py)
- [skill-creator/agents/grader.md](https://github.com/anthropics/skills/blob/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/skill-creator/agents/grader.md)
- [codebase-onboarding/questions.md](https://github.com/CognitionAI/windsurf-demo/blob/d4e661ab8b52c0b3c1d6099292d6f415fcd755b8/.windsurf/skills/codebase-onboarding/questions.md)
- [generate-tests/test-patterns.md](https://github.com/CognitionAI/windsurf-demo/blob/d4e661ab8b52c0b3c1d6099292d6f415fcd755b8/.windsurf/skills/generate-tests/test-patterns.md)
- [migration-helper/migration-plan.md](https://github.com/CognitionAI/windsurf-demo/blob/d4e661ab8b52c0b3c1d6099292d6f415fcd755b8/.windsurf/skills/migration-helper/migration-plan.md)
- [droid-control/atoms/verify/ATOM.md](https://github.com/Factory-AI/factory-plugins/blob/e63e519a736140c86f37be95a529a0c44dc9a96e/plugins/droid-control/skills/droid-control/atoms/verify/ATOM.md)

## 導入後の検証

- 全990行のパス・コミット・本文ハッシュを取得したスナップショットに照合した。調査表からリンクした補助資料も同じコミットのツリーに存在することを確認した。
- 7件の Skill 形式検証および `python3 -B -m unittest discover -s tests -v` の8テストが通過した。PR ヘルパーのテストでは、古い未解決スレッド、解決済み、ページ境界での同一 ID、二枚目の取得失敗、カーソルの停滞を扱った。
- 読み取り専用のヘルパーで公開 PR を照会し、調査時点で未解決インラインスレッドが [#102218](https://github.com/vercel/next.js/pull/102218) では0件、[#102183](https://github.com/vercel/next.js/pull/102183) では2件で、後者には最初と最新のコメントを取得できた。件数は PR 側の更新で変わる。
- 模擬 PR の仕分けでは、古い未解決コメントの対処済み判定、同じ期待値を求める2件の集約、runner 不足によるテスト未実行を区別できた。依存移行の模擬引き継ぎでは、既定値の変更、直接呼び出しとラッパー、再送時の検証、旧版のセットアップ失敗を区別できた。いずれも担当の読み取り・判断を確認した机上評価である。
