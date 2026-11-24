# Xiaohongshu (RedNote) Scraper: Notes, Comments, Accounts

Collect public Xiaohongshu (RedNote) notes by keyword, the comments of a note and account timelines as JSON. Results land in an Apify dataset you can export to CSV, Excel or JSON, or pass on to your own pipeline.

This Actor is a thin client for the [LargitData Social Media Data API](https://www.largitdata.com/developers/social-media-api/xiaohongshu/). **You need a LargitData API key** to use it; keys are issued after a [trial request](https://www.largitdata.com/en/social-media-api/#api-inquiry). The Actor itself is free; collection is billed by LargitData at USD 0.005 per record (each post or comment returned counts as one record).

> LargitData collects this data with web crawlers from publicly published content. LargitData is not affiliated with Xiaohongshu, and this is not the platform's official API. Whether it suits your use depends on your purpose and jurisdiction; please have your own counsel assess it.

## What you can collect

| Mode | What you get |
|---|---|
| Keyword search | Notes matching a keyword, optionally within a date range. |
| Comments of a note | Comments of one note (Post URL), optionally with second-level replies. |
| Account timeline | One account's notes (Author ID). The date range defaults to the last 30 days. |

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
  "keyword": "护肤日常",
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
  "platform": "xiaohongshu",
  "mode": "keyword_search",
  "source": "xhs_note",
  "url": "https://www.xiaohongshu.com/explore/000000000000000000000001",
  "content": "换季之后我把早晚的护肤步骤简化成四步，记录一下这个月的肤况 #护肤日常",
  "author": "sample_user_1",
  "author_id": "0000000000000001",
  "tm": 1781056800,
  "metadata_tags": [
    "护肤日常",
    "换季保养"
  ],
  "like_count": 120,
  "comment_count": 14,
  "share_count": 6
}
```

The full field list for every mode is on the [Xiaohongshu (RedNote) API page](https://www.largitdata.com/developers/social-media-api/xiaohongshu/) and in the [API reference](https://api.infominer.io/docs).

## FAQ

**Is this the official Xiaohongshu (RedNote) API?**
No. LargitData collects publicly published Xiaohongshu content with web crawlers and serves it through its own API. LargitData is not affiliated with Xiaohongshu.

**Are Xiaohongshu, RedNote and XHS the same platform?**
Yes. Xiaohongshu (小红书) is the platform's Chinese name, RedNote is the name used in app stores outside mainland China, and XHS is the common abbreviation.

**How far back does the data go?**
History range, volume and refresh frequency are agreed per project when you request a trial.

**Can LargitData run the collection for me?**
Yes. LargitData can monitor keywords and accounts, clean and translate the data, backfill history and deliver it to your systems.

## Other platforms

The [multi-platform Actor](https://apify.com/largitdata/social-media-api) covers Weibo, Xiaohongshu (RedNote), Douyin, Threads, Bilibili, Zhihu and Baidu Tieba with the same API key.

## Source code

OpenAPI description, Python client and this Actor's source: [github.com/ywchiu/social-media-api](https://github.com/ywchiu/social-media-api)

Built by [LargitData](https://www.largitdata.com/en/) (大數軟體), Taipei.
