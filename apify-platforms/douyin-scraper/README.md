# Douyin Scraper: Videos, Comments & Account Posts

Collect public Douyin videos by keyword, the comments of a video and account posts as JSON. Export results from the Apify dataset to CSV, Excel, or JSON, or send them to your data pipeline.

This Actor connects to the [LargitData Social Media Data API](https://www.largitdata.com/developers/social-media-api/douyin/). **You need a LargitData API key** to run this Actor. Get your key through a [trial request](https://www.largitdata.com/en/social-media-api/#api-inquiry). The Actor itself is free. LargitData bills data collection at USD 0.005 per record (each returned post or comment counts as one record).

## Supported data collection modes

| Mode | What you get |
|---|---|
| Keyword search | Videos matching a keyword, with an optional date range. |
| Comments of a video | Comments on one video (Post URL). |
| Account posts | Videos from one account (Author ID). Defaults to the last 30 days. |

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
  "keyword": "露营装备",
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

See the complete output field list for every mode on the [Douyin API page](https://www.largitdata.com/developers/social-media-api/douyin/) and in the [API reference](https://api.infominer.io/docs).

## FAQ

**Does this Douyin scraper cover TikTok?**
No. Douyin is the mainland-China app. TikTok is a separate service and is not covered.

**Does this Douyin scraper download video files?**
No. Records include video metadata and text only. Resolving download URLs for collected videos is a separate LargitData API endpoint; see the [Douyin page](https://www.largitdata.com/developers/social-media-api/douyin/).

**How far back does historical data go?**
Historical range, volume, and refresh frequency are set per project when you request a trial.

**Can LargitData manage data collection for me?**
Yes. LargitData can monitor keywords and accounts, clean and translate data, backfill historical data, and deliver it to your systems.

## Other supported social media platforms

Need more platforms? The [multi-platform Actor](https://apify.com/largitdata/social-media-api) supports Weibo, Xiaohongshu (RedNote), Douyin, Threads, Bilibili, Zhihu, and Baidu Tieba using the same API key.

## Source code and Python client

OpenAPI specification, Python client, and Actor source code: [github.com/ywchiu/social-media-api](https://github.com/ywchiu/social-media-api)

Built by [LargitData](https://www.largitdata.com/en/) (大數軟體), Taipei.
