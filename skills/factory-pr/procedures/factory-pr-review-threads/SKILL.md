---
name: factory-pr-review-threads
description: 既存 PR の古い差分・重複・部分取得を含むレビュー指摘から、現行 head での残件を特定する。
---

# 未解決のレビュー指摘を整理する

GitHub のレビューを扱うときは、取得できる連携機能で未解決スレッドを列挙する。GitHub CLI からは、親の factory-pr の[読み取り専用スクリプト](../../scripts/list_review_threads.py) を使える。

```sh
python3 "$FACTORY_PR_SKILL/scripts/list_review_threads.py" OWNER REPO PR番号
```

`FACTORY_PR_SKILL` は親の factory-pr ディレクトリ。出力はインラインの未解決スレッドで、最初の指摘と最新の返答を含む。経緯が判断に影響する場合はコメント URL で中間の会話も読む。PR 全体へのレビュー本文・通常コメントは別途確認する。途中ページの取得失敗は未解決ゼロと区別する。

古い差分に付いた未解決の指摘は、最新 head の対応箇所と当初の期待を照合する。現行コードで対処済みなら、その箇所と確認結果を報告する。同じ修正で複数スレッドを扱える場合は、期待値ごとに一つの作業にまとめ、元の URL はすべて渡す。返信・スレッド解決などの外部操作は依頼範囲に従う。

ページの一部しか取得できていない場合、観測済みのスレッド数は下限として伝える。取得済みの同一指摘はまとめて元担当に渡せる。残件総数と解決判断は取得完了まで保留する。公開判断には、その時点の head に対応する QA と CI の状態を別々に記す。

## 判断例

同じ行への2件でも、一方が例外時の挙動、もう一方が説明文の誤りなら期待値が異なる。各 URL と確認方法を別々に引き継ぐ。

## 出典と採用した観点

スレッド単位の取得と未解決コメントの仕分けを採用。取得漏れの扱いは同梱ヘルパーに合わせた。[openai / gh-address-comments](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/gh-address-comments/SKILL.md)・[Factory-AI / follow-up-on-pr](https://github.com/Factory-AI/factory-plugins/blob/e63e519a736140c86f37be95a529a0c44dc9a96e/plugins/code-review/skills/follow-up-on-pr/SKILL.md)・[この Factory のスレッド取得処理](../../scripts/list_review_threads.py)
