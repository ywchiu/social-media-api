# Douyin Scraper: Videos, Comments & Account Posts

Collect public Douyin videos by keyword, the comments of a video and account posts as JSON. Results land in an Apify dataset you can export to CSV, Excel or JSON, or pass on to your own pipeline.

This Actor is a thin client for the [LargitData Social Media Data API](https://www.largitdata.com/developers/social-media-api/douyin/). **You need a LargitData API key** to use it; keys are issued after a [trial request](https://www.largitdata.com/en/social-media-api/#api-inquiry). The Actor itself is free; collection is billed by LargitData at USD 0.005 per record (each post or comment returned counts as one record).

## What you can collect

| Mode | What you get |
|---|---|
| Keyword search | Videos matching a keyword, optionally within a date range. |
| Comments of a video | Comments of one video (Post URL). |
| Account posts | One account's videos (Author ID). The date range defaults to the last 30 days. |

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
  "keyword": "露营装备",
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
  "platform": "douyin",
  "mode": "keyword_search",
  "url": "https://www.douyin.com/video/0000000000000000001",
  "post_id": "0000000000000000001",
  "content": "第一次带全家去露营，这几样装备真的省事 #露营装备",
  "author": "sample_user_1",
  "tm": 1781056800,
  "date": "2026-06-10",
  "metadata_tags": [
    "露营装备"
  ],
  "like_count": 240,
  "comment_count": 31,
  "share_count": 18,
  "video_length": 42
}
```

The full field list for every mode is on the [Douyin API page](https://www.largitdata.com/developers/social-media-api/douyin/) and in the [API reference](https://api.infominer.io/docs).

## FAQ

**Does it cover TikTok?**
No. Douyin is the mainland-China app. TikTok is a separate service and is not covered.

**Does it download the video files?**
No. The records carry the video's metadata and text. Resolving download URLs for collected videos is a separate LargitData API endpoint; see the [Douyin page](https://www.largitdata.com/developers/social-media-api/douyin/).

**How far back does the data go?**
History range, volume and refresh frequency are agreed per project when you request a trial.

**Can LargitData run the collection for me?**
Yes. LargitData can monitor keywords and accounts, clean and translate the data, backfill history and deliver it to your systems.

## Other platforms

The [multi-platform Actor](https://apify.com/largitdata/social-media-api) covers Weibo, Xiaohongshu (RedNote), Douyin, Threads, Bilibili, Zhihu and Baidu Tieba with the same API key.

## Source code

OpenAPI description, Python client and this Actor's source: [github.com/ywchiu/social-media-api](https://github.com/ywchiu/social-media-api)

Built by [LargitData](https://www.largitdata.com/en/) (大數軟體), Taipei.
