# Threads Scraper: Keyword Search, Replies & Timelines

Collect public Threads posts by keyword, the replies to a post and public account timelines as JSON. Results land in an Apify dataset you can export to CSV, Excel or JSON, or pass on to your own pipeline.

This Actor is a thin client for the [LargitData Social Media Data API](https://www.largitdata.com/developers/social-media-api/threads/). **You need a LargitData API key** to use it; keys are issued after a [trial request](https://www.largitdata.com/en/social-media-api/#api-inquiry). The Actor itself is free; collection is billed by LargitData at USD 0.005 per record (each post or comment returned counts as one record).

## What you can collect

| Mode | What you get |
|---|---|
| Keyword search | Posts matching a keyword, optionally within a date range. |
| Replies to a post | Replies to one post (Post URL). |
| Account timeline | One public account's posts (Author ID), optionally within a date range. |

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
  "keyword": "珍珠奶茶",
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
  "platform": "threads",
  "mode": "keyword_search",
  "url": "https://www.threads.com/@sample_user_1/post/Sample00001",
  "post_id": "Sample00001",
  "content": "今天試了巷口新開的手搖店，珍珠奶茶半糖剛剛好",
  "author": "sample_user_1",
  "author_id": "0000000001",
  "tm": 1781056800,
  "like_count": 35,
  "comment_count": 4,
  "share_count": 1,
  "is_reply": false,
  "is_quote": false,
  "keyword": "珍珠奶茶"
}
```

The full field list for every mode is on the [Threads API page](https://www.largitdata.com/developers/social-media-api/threads/) and in the [API reference](https://api.infominer.io/docs).

## FAQ

**Can I get the accounts that reacted to a post?**
Reactions are available as a separate task in the LargitData API, not in this Actor; see the [Threads page](https://www.largitdata.com/developers/social-media-api/threads/).

**How far back does the data go?**
History range, volume and refresh frequency are agreed per project when you request a trial.

**Can LargitData run the collection for me?**
Yes. LargitData can monitor keywords and accounts, clean and translate the data, backfill history and deliver it to your systems.

## Other platforms

The [multi-platform Actor](https://apify.com/largitdata/social-media-api) covers Weibo, Xiaohongshu (RedNote), Douyin, Threads, Bilibili, Zhihu and Baidu Tieba with the same API key.

## Source code

OpenAPI description, Python client and this Actor's source: [github.com/ywchiu/social-media-api](https://github.com/ywchiu/social-media-api)

Built by [LargitData](https://www.largitdata.com/en/) (大數軟體), Taipei.
