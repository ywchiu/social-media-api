# Weibo, Xiaohongshu, Douyin, Threads, Bilibili, Zhihu & Tieba Data

Collect public posts, comments and account timelines from seven Chinese-language platforms as JSON, and get them in an Apify dataset you can export to CSV, Excel or JSON, or pass on to your own pipeline.

This Actor is a thin client for the [LargitData Social Media Data API](https://www.largitdata.com/en/social-media-api/). **You need a LargitData API key** to use it; keys are issued after a [trial request](https://www.largitdata.com/en/social-media-api/#api-inquiry). The Actor itself is free; collection is billed under your LargitData plan.

> LargitData collects this data with web crawlers from publicly published content. LargitData is not affiliated with any of these platforms, and this is not any platform's official API. Whether it suits your use depends on your purpose and jurisdiction; please have your own counsel assess it.

## What you can collect

| Platform | Keyword search | Comments of a post | Account timeline |
|---|---|---|---|
| Weibo | Posts | Comments, optionally with second-level replies | Yes |
| Xiaohongshu (RedNote) | Notes | Comments, optionally with second-level replies | Yes |
| Douyin | Videos | Comments | Yes |
| Threads | Posts | Replies | Yes |
| Bilibili | Videos | Top comments with replies | |
| Zhihu | Answers and articles | Answers, comments and replies | |
| Baidu Tieba | Posts | Floors and replies | |

Douyin is the mainland-China app; it is not TikTok, and TikTok is not covered.

## How to use it

1. Paste your LargitData API key. Without a key, the Actor returns one sample record (marked `"sample": true`) so you can see the output format.
2. Pick a platform and what to collect:
   - **Keyword search**: enter a keyword in the platform's language (Simplified Chinese for most platforms) and, optionally, a date range.
   - **Comments of a post**: enter the post URL.
   - **Account timeline**: enter the account's author ID. On Weibo, Xiaohongshu and Douyin the date range defaults to the last 30 days.
3. Run. The Actor creates a collection task, waits for it to finish, and saves every record to the dataset.

Collection runs on LargitData's side and can take several minutes. If a task is still running when the timeout is reached, the Actor stops and writes the task ID to the `OUTPUT` record; the task keeps running and you can fetch it later.

## Input example

```json
{
  "apiKey": "YOUR_LARGITDATA_API_KEY",
  "platform": "xiaohongshu",
  "mode": "keyword_search",
  "keyword": "护肤日常",
  "startDate": "2026-06-01",
  "endDate": "2026-06-30",
  "maxPages": 3,
  "maxItems": 1000
}
```

## Output example

Each record keeps the fields the API returns, plus `platform` and `mode`. A Xiaohongshu note looks like this (sample values):

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
  "metadata_tags": ["护肤日常", "换季保养"],
  "like_count": 120,
  "comment_count": 14,
  "share_count": 6
}
```

Field lists for every platform and mode are in the [API reference](https://api.infominer.io/docs) and the [developer pages](https://www.largitdata.com/developers/social-media-api/).

## FAQ

**Is this the official Weibo / Xiaohongshu / Douyin / Threads API?**
No. LargitData collects publicly published content with web crawlers and serves it through its own API.

**Can I read Weibo in English?**
The LargitData API offers English keyword subscriptions for Weibo with machine translation. That feature is not part of this Actor; see the [Weibo English data page](https://www.largitdata.com/developers/social-media-api/weibo/english-translation/).

**How far back does the data go?**
History range, volume and refresh frequency are agreed per project when you request a trial.

**Can LargitData run the collection for me?**
Yes. LargitData can monitor keywords and accounts, clean and translate the data, backfill history and deliver it to your systems.

## Source code

OpenAPI description, Python client and this Actor's source: [github.com/ywchiu/social-media-api](https://github.com/ywchiu/social-media-api)

Built by [LargitData](https://www.largitdata.com/en/) (大數軟體), Taipei.
