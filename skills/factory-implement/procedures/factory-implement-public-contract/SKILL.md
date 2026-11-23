---
name: factory-implement-public-contract
description: API・設定・CLI・保存形式を変えるとき、既存利用者への影響と更新する利用手順を決める。
---

# 公開契約・既存データ・利用手順を更新する

起動方法、設定、API、ユーザー操作が変わる場合は、該当する README や利用手順とコードを同じ候補に含める。手順や例を実際のコマンドと照合する。リリースノートの記載は、依頼やリポジトリの規約に該当するときに行う。

公開 API を変更したときは利用者が書く引数・レスポンス例を更新する。リリースノートが対象なら、利用者への影響、移行前後の呼び方、旧データの扱いを記す。内部実装だけの変更で利用者向けの変更点を作らない。

旧データや設定の省略値に影響する場合は、変更前から利用している呼び出し方と新しい指定を同じ候補で試す。報告には使用した入力と読み戻した結果を添える。

## 判断例

設定を追加する例なら「旧ファイルにキーなし」「明示的に false」「新規作成」の各入力で読み戻しを記録する。旧形式をサポートしない仕様なら、利用者が実行する移行手順と失敗時のメッセージを確認する。

## 出典と採用した観点

利用手順を実コマンドと照合し、移行対象の旧形式と利用箇所を整理する。[CognitionAI / readme-hygiene](https://github.com/CognitionAI/team-marketplace-template/blob/2169376ccdf4ebb84a166f867be176b194fa0361/plugins/docs-and-release/skills/readme-hygiene/SKILL.md)・[CognitionAI / migration-helper](https://github.com/CognitionAI/windsurf-demo/blob/d4e661ab8b52c0b3c1d6099292d6f415fcd755b8/.windsurf/skills/migration-helper/SKILL.md)
