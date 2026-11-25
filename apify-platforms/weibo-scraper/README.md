# Weibo Scraper: Posts, Comments & Account Timelines

Collect public Weibo posts by keyword, the comments of a post and account timelines as JSON. Export results from the Apify dataset to CSV, Excel, or JSON, or send them to your data pipeline.

This Actor connects to the [LargitData Social Media Data API](https://www.largitdata.com/developers/social-media-api/weibo/). **You need a LargitData API key** to run this Actor. Get your key through a [trial request](https://www.largitdata.com/en/social-media-api/#api-inquiry). The Actor itself is free. LargitData bills data collection at USD 0.005 per record (each returned post or comment counts as one record).

## Supported data collection modes

| Mode | What you get |
|---|---|
| Keyword search | Posts matching a keyword, optionally within a date range. |
| Comments of a post | Comments on one post (Post URL), with optional second-level replies. |
| Account timeline | Posts from one account (Author ID). Defaults to the last 30 days. |

## How to run this Actor

1. Enter your LargitData API key. Without a key, the Actor returns one sample record (marked `"sample": true`) to preview the output format.
2. Choose a collection mode and enter a keyword, post URL, or author ID.
3. Start the Actor. It creates a collection task, waits for completion, and saves all records to the Apify dataset.

Collection runs on LargitData's servers and can take several minutes. If the Actor reaches its timeout, it stops and writes the task ID to the `OUTPUT` record. The task keeps running, and you can fetch the results later.

## Input example

```json
{
  "apiKey": "YOUR_LARGITDATA_API_KEY",
  "mode": "keyword_search",
  "keyword": "新能源汽车",
  "startDate": "2026-06-01",
  "endDate": "2026-06-30",
  "maxPages": 3,
  "maxItems": 1000
}
```

## Output example

Each record includes all API response fields plus `platform` and `mode`. Example keyword-search record (sample values, not a real post):

```json
{
  "platform": "weibo",
  "mode": "keyword_search",
  "url": "https://weibo.com/0000000001/Sample0001",
  "content": "周末去试驾了两款新能源汽车，续航和充电速度差别比想象的大 #新能源汽车",
  "author": "sample_user_1",
  "author_id": "0000000001",
  "tm": 1781056800,
  "datetime": "2026-06-10 10:00:00",
  "metadata_tags": [
    "新能源汽车"
  ],
  "like_count": 86,
  "comment_count": 12,
  "share_count": 5
}
```

See the complete output field list for every mode on the [Weibo API page](https://www.largitdata.com/developers/social-media-api/weibo/) and in the [API reference](https://api.infominer.io/docs).

## FAQ

**Can I get Weibo data in English with translation?**
Not in this Actor. The LargitData API offers English keyword subscriptions for Weibo with machine translation; see the [Weibo English data page](https://www.largitdata.com/developers/social-media-api/weibo/english-translation/).

**Can I trace Weibo reposts and repost chains?**
Not in this Actor. Repost lists and repost-chain tracing are available in the LargitData API; see the [Weibo reposts page](https://www.largitdata.com/developers/social-media-api/weibo/reposts/).

**How far back does historical data go?**
Historical range, volume, and refresh frequency are set per project when you request a trial.

**Can LargitData manage data collection for me?**
Yes. LargitData can monitor keywords and accounts, clean and translate data, backfill historical data, and deliver it to your systems.

## Other supported social media platforms

Need more platforms? The [multi-platform Actor](https://apify.com/largitdata/social-media-api) supports Weibo, Xiaohongshu (RedNote), Douyin, Threads, Bilibili, Zhihu, and Baidu Tieba using the same API key.

## Source code and Python client

OpenAPI specification, Python client, and Actor source code: [github.com/ywchiu/social-media-api](https://github.com/ywchiu/social-media-api)

Built by [LargitData](https://www.largitdata.com/en/) (大數軟體), Taipei.
