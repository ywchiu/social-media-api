# Xiaohongshu (RedNote) Scraper: Notes, Comments, Accounts

Collect public Xiaohongshu (RedNote) notes by keyword, the comments of a note and account timelines as JSON. Export results from the Apify dataset to CSV, Excel, or JSON, or send them to your data pipeline.

This Actor connects to the [LargitData Social Media Data API](https://www.largitdata.com/developers/social-media-api/xiaohongshu/). **You need a LargitData API key** to run this Actor. Get your key through a [trial request](https://www.largitdata.com/en/social-media-api/#api-inquiry). The Actor itself is free. LargitData bills data collection at USD 0.005 per record (each returned post or comment counts as one record).

## Supported data collection modes

| Mode | What you get |
|---|---|
| Keyword search | Notes matching a keyword, with an optional date range. |
| Comments of a note | Comments on one note (Post URL), with optional second-level replies. |
| Account timeline | Notes from one account (Author ID). Defaults to the last 30 days. |

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
  "keyword": "护肤日常",
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

See the complete output field list for every mode on the [Xiaohongshu (RedNote) API page](https://www.largitdata.com/developers/social-media-api/xiaohongshu/) and in the [API reference](https://api.infominer.io/docs).

## FAQ

**Are Xiaohongshu, RedNote and XHS the same platform?**
Yes. Xiaohongshu (小红书) is the platform's Chinese name, RedNote is the name used in app stores outside mainland China, and XHS is the common abbreviation.

**How far back does historical data go?**
Historical range, volume, and refresh frequency are set per project when you request a trial.

**Can LargitData manage data collection for me?**
Yes. LargitData can monitor keywords and accounts, clean and translate data, backfill historical data, and deliver it to your systems.

## Other supported social media platforms

Need more platforms? The [multi-platform Actor](https://apify.com/largitdata/social-media-api) supports Weibo, Xiaohongshu (RedNote), Douyin, Threads, Bilibili, Zhihu, and Baidu Tieba using the same API key.

## Source code and Python client

OpenAPI specification, Python client, and Actor source code: [github.com/ywchiu/social-media-api](https://github.com/ywchiu/social-media-api)

Built by [LargitData](https://www.largitdata.com/en/) (大數軟體), Taipei.
