# ソーシャルメディアデータ API：Weibo・小紅書（RED）・抖音・Threads

[LargitData ソーシャルメディア API](https://www.largitdata.com/ja/social-media-api/) のコード例と OpenAPI 定義です。
**Weibo（微博）**、**小紅書（RED / RedNote）**、**抖音（Douyin）**、**Threads** の公開投稿、コメント、リポスト、
アカウントのタイムラインを JSON で取得できます。Weibo はキーワード購読による**英語の機械翻訳**にも対応しています。
PTT、Dcard、X、Reddit、Facebook、Instagram はアカウント単位の設定で提供しますので、お問い合わせください。

[English](README.md)

- データは各プラットフォームで公開されているコンテンツをウェブクローラーで収集したものです。当社はこれらのプラットフォームと
  提携しておらず、各プラットフォーム自身が提供する API ではありません。ご利用目的に適するかどうかは、用途と法域に応じて
  買い手側の法務部門でご判断ください。収集元と収集方法の説明はご提供できます。
- 商用 API です。API キーはトライアル申込後に発行します：**[トライアルを申し込む](https://www.largitdata.com/ja/social-media-api/#api-inquiry)**

## 仕組み

Base URL は `https://api.infominer.io/api/v2`、API キーは `auth-header` リクエストヘッダーで送信します。
収集は非同期です：`POST` でタスクを作成して `id` を受け取り、`GET` でステータスが `INIT` / `RUNNING` でなくなるまで
ポーリングし、`DONE` になると同じレスポンスに `data` と `total_count` が含まれます。

## 機能別のエンドポイント

| 機能 | エンドポイント |
|---|---|
| [Weibo（微博）キーワード検索 API](https://www.largitdata.com/ja/developers/social-media-api/weibo/keyword-search/) | `POST /weibo/search/task`, `GET /weibo/search/task/{task_id}` |
| [Weibo（微博）コメント API](https://www.largitdata.com/ja/developers/social-media-api/weibo/comments/) | `POST /weibo/pushs/task`, `GET /weibo/pushs/task/{task_id}` |
| [Weibo（微博）リポスト API とリポスト連鎖の遡及](https://www.largitdata.com/ja/developers/social-media-api/weibo/reposts/) | `POST /weibo/reposts/task`, `GET /weibo/reposts/task/{task_id}`, `POST /weibo/repost/parent/task`, `GET /weibo/repost/parent/task/{task_id}` |
| [Weibo（微博）ユーザータイムライン API](https://www.largitdata.com/ja/developers/social-media-api/weibo/user-timeline/) | `POST /weibo/users/task`, `GET /weibo/users/task/{task_id}` |
| [Weibo（微博）英語翻訳 API](https://www.largitdata.com/ja/developers/social-media-api/weibo/english-translation/) | `POST /weibo/translate/search`, `POST /weibo/translate/pushs`, `POST /weibo/translate/reposts` |
| [小紅書（RED）ノート検索 API](https://www.largitdata.com/ja/developers/social-media-api/xiaohongshu/keyword-search/) | `POST /xhs/search/task`, `GET /xhs/search/task/{task_id}` |
| [小紅書（RED）コメント API](https://www.largitdata.com/ja/developers/social-media-api/xiaohongshu/comments/) | `POST /xhs/pushs/task`, `GET /xhs/pushs/task/{task_id}` |
| [小紅書（RED）ユーザータイムライン API](https://www.largitdata.com/ja/developers/social-media-api/xiaohongshu/user-timeline/) | `POST /xhs/users/task`, `GET /xhs/users/task/{task_id}` |
| [抖音（Douyin）キーワード検索 API](https://www.largitdata.com/ja/developers/social-media-api/douyin/keyword-search/) | `POST /douyin/search/task`, `GET /douyin/search/task/{task_id}` |
| [抖音（Douyin）コメント API](https://www.largitdata.com/ja/developers/social-media-api/douyin/comments/) | `POST /douyin/pushs/task`, `GET /douyin/pushs/task/{task_id}` |
| [抖音（Douyin）ユーザータイムライン API](https://www.largitdata.com/ja/developers/social-media-api/douyin/user-timeline/) | `POST /douyin/users/task`, `GET /douyin/users/task/{task_id}` |

完全なドキュメント：https://api.infominer.io/docs

## ファイル

- [`openapi.json`](openapi.json)：Weibo・小紅書・抖音・Threads エンドポイントの OpenAPI 3.1 定義（2026-10-25 仕様スナップショット）
- [`examples/`](examples/)：Python のサンプル（`export LARGITDATA_API_KEY=...` を設定して実行）
