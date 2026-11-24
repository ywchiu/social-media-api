# Weibo Scraper: Posts, Comments & Account Timelines

Collect public Weibo posts by keyword, the comments of a post and account timelines as JSON. Results land in an Apify dataset you can export to CSV, Excel or JSON, or pass on to your own pipeline.

This Actor is a thin client for the [LargitData Social Media Data API](https://www.largitdata.com/developers/social-media-api/weibo/). **You need a LargitData API key** to use it; keys are issued after a [trial request](https://www.largitdata.com/en/social-media-api/#api-inquiry). The Actor itself is free; collection is billed by LargitData at USD 0.005 per record (each post or comment returned counts as one record).

## What you can collect

| Mode | What you get |
|---|---|
| Keyword search | Posts matching a keyword, optionally within a date range. |
| Comments of a post | Comments of one post (Post URL), optionally with second-level replies. |
| Account timeline | One account's posts (Author ID). The date range defaults to the last 30 days. |

## How to use it

1. Paste your LargitData API key. Without a key, the Actor returns one sample record (marked `"sample": true`) so you can see the output format.
2. Pick what to collect and fill in the keyword, post URL or author ID.
3. Run. The Actor creates a collection task, waits for it to finish, and saves every record to the dataset.

Collection runs on LargitData's side and can take several minutes. If a task is still running when the timeout is reached, the Actor stops and writes the task ID to the `OUTPUT` record; the task keeps running and you can fetch it later.

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

Each record keeps the fields the API returns, plus `platform` and `mode`. A keyword-search record looks like this (sample values, not a real post):

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

The full field list for every mode is on the [Weibo API page](https://www.largitdata.com/developers/social-media-api/weibo/) and in the [API reference](https://api.infominer.io/docs).

## FAQ

**Can I read Weibo in English?**
The LargitData API offers English keyword subscriptions for Weibo with machine translation. That feature is not part of this Actor; see the [Weibo English data page](https://www.largitdata.com/developers/social-media-api/weibo/english-translation/).

**Can I trace reposts?**
Repost lists and repost-chain tracing are available in the LargitData API, not in this Actor; see the [Weibo reposts page](https://www.largitdata.com/developers/social-media-api/weibo/reposts/).

**How far back does the data go?**
History range, volume and refresh frequency are agreed per project when you request a trial.

**Can LargitData run the collection for me?**
Yes. LargitData can monitor keywords and accounts, clean and translate the data, backfill history and deliver it to your systems.

## Other platforms

The [multi-platform Actor](https://apify.com/largitdata/social-media-api) covers Weibo, Xiaohongshu (RedNote), Douyin, Threads, Bilibili, Zhihu and Baidu Tieba with the same API key.

## Source code

OpenAPI description, Python client and this Actor's source: [github.com/ywchiu/social-media-api](https://github.com/ywchiu/social-media-api)

Built by [LargitData](https://www.largitdata.com/en/) (大數軟體), Taipei.
