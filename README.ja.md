# ソーシャルメディアデータ API：Weibo（微博）・小紅書（小红书）・抖音（Douyin）・Threads・ビリビリ・知乎・百度貼吧

[LargitData ソーシャルメディア API](https://www.largitdata.com/ja/social-media-api/) のコード例と OpenAPI 定義です。
**Weibo（微博）**、**小紅書（RED / RedNote）**、**抖音（Douyin）**、**Threads**、**ビリビリ（bilibili）**、
**知乎（Zhihu）**、**百度貼吧（Baidu Tieba）** の公開投稿、コメント、リポスト、
アカウントのタイムラインを JSON で取得できます。Weibo はキーワード購読による**英語の機械翻訳**にも対応しています。
PTT、Dcard、X、Reddit、Facebook、Instagram はアカウント単位の設定で提供しますので、お問い合わせください。

[English](README.md) · [繁體中文](README.zh-TW.md)

- データは各プラットフォームで公開されているコンテンツをウェブクローラーで収集したものです。当社はこれらのプラットフォームと
  提携しておらず、各プラットフォーム自身が提供する API ではありません。ご利用目的に適するかどうかは、用途と法域に応じて
  買い手側の法務部門でご判断ください。収集元と収集方法の説明はご提供できます。
- 商用 API です。API キーはトライアル申込後に発行します：**[トライアルを申し込む](https://www.largitdata.com/ja/social-media-api/#api-inquiry)**

## 仕組み

Base URL は `https://api.infominer.io/api/v2`、API キーは `auth-header` リクエストヘッダーで送信します。
収集は非同期です：`POST` でタスクを作成して `id` を受け取り、`GET` でステータスが `INIT` / `RUNNING` でなくなるまで
ポーリングし、`DONE` になると同じレスポンスに `data` と `total_count` が含まれます（`page` と `pageSize` でページ送り）。

```bash
curl -X POST https://api.infominer.io/api/v2/weibo/search/task \
  -H "auth-header: $LARGITDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "手冲咖啡", "start_date": "2026-06-01", "end_date": "2026-06-30", "max_pages": 3}'

curl "https://api.infominer.io/api/v2/weibo/search/task/$TASK_ID?page=1&pageSize=100" \
  -H "auth-header: $LARGITDATA_API_KEY"
```

## 機能別のエンドポイント

| 機能 | エンドポイント |
|---|---|
| [Weibo（微博）キーワード検索 API](https://www.largitdata.com/ja/developers/social-media-api/weibo/keyword-search/) | `POST /weibo/search/task`, `GET /weibo/search/task/{task_id}` |
| [Weibo（微博）コメント API](https://www.largitdata.com/ja/developers/social-media-api/weibo/comments/) | `POST /weibo/pushs/task`, `GET /weibo/pushs/task/{task_id}` |
| [Weibo（微博）リポスト API とリポスト連鎖の遡及](https://www.largitdata.com/ja/developers/social-media-api/weibo/reposts/) | `POST /weibo/reposts/task`, `GET /weibo/reposts/task/{task_id}`, `POST /weibo/repost/parent/task`, `GET /weibo/repost/parent/task/{task_id}` |
| [Weibo（微博）ユーザータイムライン API](https://www.largitdata.com/ja/developers/social-media-api/weibo/user-timeline/) | `POST /weibo/users/task`, `GET /weibo/users/task/{task_id}` |
| [Weibo（微博）英語翻訳 API](https://www.largitdata.com/ja/developers/social-media-api/weibo/english-translation/) | `POST /weibo/translate/search`, `POST /weibo/translate/pushs`, `POST /weibo/translate/reposts` |
| [小紅書（小红书）ノート検索 API](https://www.largitdata.com/ja/developers/social-media-api/xiaohongshu/keyword-search/) | `POST /xhs/search/task`, `GET /xhs/search/task/{task_id}` |
| [小紅書（小红书）コメント API](https://www.largitdata.com/ja/developers/social-media-api/xiaohongshu/comments/) | `POST /xhs/pushs/task`, `GET /xhs/pushs/task/{task_id}` |
| [小紅書（小红书）ユーザータイムライン API](https://www.largitdata.com/ja/developers/social-media-api/xiaohongshu/user-timeline/) | `POST /xhs/users/task`, `GET /xhs/users/task/{task_id}` |
| [抖音（Douyin）キーワード検索 API](https://www.largitdata.com/ja/developers/social-media-api/douyin/keyword-search/) | `POST /douyin/search/task`, `GET /douyin/search/task/{task_id}` |
| [抖音（Douyin）コメント API](https://www.largitdata.com/ja/developers/social-media-api/douyin/comments/) | `POST /douyin/pushs/task`, `GET /douyin/pushs/task/{task_id}` |
| [抖音（Douyin）ユーザータイムライン API](https://www.largitdata.com/ja/developers/social-media-api/douyin/user-timeline/) | `POST /douyin/users/task`, `GET /douyin/users/task/{task_id}` |
| [Threads キーワード検索 API](https://www.largitdata.com/ja/developers/social-media-api/threads/keyword-search/) | `POST /threads/search/task`, `GET /threads/search/task/{task_id}` |
| [Threads 返信 API](https://www.largitdata.com/ja/developers/social-media-api/threads/replies/) | `POST /threads/pushs/task`, `GET /threads/pushs/task/{task_id}` |
| [Threads ユーザータイムライン API](https://www.largitdata.com/ja/developers/social-media-api/threads/user-timeline/) | `POST /threads/users/task`, `GET /threads/users/task/{task_id}` |
| [Threads reactions API](https://www.largitdata.com/ja/developers/social-media-api/threads/reactions/) | `POST /threads/reactions/task`, `GET /threads/reactions/task/{task_id}` |
| [ビリビリ（bilibili）動画キーワード検索 API](https://www.largitdata.com/ja/developers/social-media-api/bilibili/keyword-search/) | `POST /bilibili/search/task`, `GET /bilibili/search/task/{task_id}` |
| [ビリビリ（bilibili）コメント API](https://www.largitdata.com/ja/developers/social-media-api/bilibili/comments/) | `POST /bilibili/pushs/task`, `GET /bilibili/pushs/task/{task_id}` |
| [知乎（Zhihu）キーワード検索 API](https://www.largitdata.com/ja/developers/social-media-api/zhihu/keyword-search/) | `POST /zhihu/search/task`, `GET /zhihu/search/task/{task_id}` |
| [知乎（Zhihu）回答・コメント API](https://www.largitdata.com/ja/developers/social-media-api/zhihu/answers-and-comments/) | `POST /zhihu/pushs/task`, `GET /zhihu/pushs/task/{task_id}` |
| [百度貼吧（Baidu Tieba）スレッド検索 API](https://www.largitdata.com/ja/developers/social-media-api/tieba/keyword-search/) | `POST /tieba/search/task`, `GET /tieba/search/task/{task_id}` |
| [百度貼吧（Baidu Tieba）返信 API](https://www.largitdata.com/ja/developers/social-media-api/tieba/replies/) | `POST /tieba/pushs/task`, `GET /tieba/pushs/task/{task_id}` |

プラットフォーム別リファレンス：[Weibo](https://www.largitdata.com/ja/developers/social-media-api/weibo/) ·
[小紅書](https://www.largitdata.com/ja/developers/social-media-api/xiaohongshu/) ·
[抖音](https://www.largitdata.com/ja/developers/social-media-api/douyin/) ·
[Threads](https://www.largitdata.com/ja/developers/social-media-api/threads/) ·
[ビリビリ](https://www.largitdata.com/ja/developers/social-media-api/bilibili/) ·
[知乎](https://www.largitdata.com/ja/developers/social-media-api/zhihu/) ·
[百度貼吧](https://www.largitdata.com/ja/developers/social-media-api/tieba/)。完全なドキュメント：https://api.infominer.io/docs

## ファイル

- [`openapi.json`](openapi.json)：Weibo・小紅書・抖音・Threads エンドポイントの OpenAPI 3.1 定義（2026-10-25 仕様スナップショット）と、ビリビリ・知乎・百度貼吧のエンドポイント（2026-11-21 時点の仕様）
- [`examples/`](examples/)：Python のサンプル（`pip install -r examples/requirements.txt` の後、
  `export LARGITDATA_API_KEY=...` を設定して実行）
- [`apify/`](apify/)：同じ API を Apify Actor として公開（[apify.com/largitdata/social-media-api](https://apify.com/largitdata/social-media-api)）。ご自身の API キーで実行し、結果を Apify の dataset に保存します。

## 知っておきたい制限

- キーワード検索の結果は 1 ページ最大 100 件、コメントは最大 1000 件まで取得できます。
- Weibo と小紅書のコメントタスクは 2 層目の返信（`crawl_second_layer`）も取得できます。抖音は対象外です。
- 抖音のコメントタスクは既定で 1 動画あたり 50 件を収集します（`max_items`、`get_all` で変更）。
- Weibo のリポストチェーンは深さ 10 まで追跡できます（既定は 3）。
- Threads の検索・返信・タイムラインのタスクは、ポーリングで収集済みの行を `data` に、件数を `total_count` に返し、
  タスクが `RUNNING` の間も読み取れます。reactions タスクは完了時に投稿の閲覧数・いいね数・シェア数と、ページ分割された
  reactions 一覧（`per_page` は最大 1000）を返します。`mask_author` で投稿者の識別情報を除外できます。ウェブクローラーで
  収集するサービスであり、Meta 公式の Threads API ではありません。
- Weibo の英語翻訳は購読キーワードについて直近 30 日分をさかのぼって取得します。任意の投稿をその場で翻訳する機能ではありません。
- ビリビリ、知乎、百度貼吧のタスクは `DONE` のときだけ `task`、`total_count`、`data` を返し、それ以外はタスクオブジェクトのみを返します。
  ビリビリの検索は 1 回約 1,000 本まで、コメントタスクは動画の人気上位 3 件の第 1 階層コメントとそれぞれの返信 20 件までです。
  知乎の検索は回答とコラム記事が対象で、網羅的ではありません。貼吧の検索は 1 回約 620 スレッドまで（`depth_capped` で期間が途中で
  切れたかがわかります）、フロア内の返信は 1 フロア最大 600 件です。
- 取得できる期間、件数、更新頻度はプロジェクトごとに確認します。

## 概要

[LargitData](https://www.largitdata.com/ja/)（大數軟體有限公司）は台北の企業で、InfoMiner、RAGi とデータ API を提供しています。
お問い合わせは[トライアル申込フォーム](https://www.largitdata.com/ja/social-media-api/#api-inquiry)からどうぞ。

このリポジトリのサンプルコードは MIT License で公開しています。API 自体の利用は LargitData との契約に従います。
