# Weibo, Xiaohongshu, Douyin, Threads, Bilibili, Zhihu & Tieba Data

Collect public posts, comments, and account timelines from seven Chinese-language social media platforms with one scraper API Actor. Results save to an Apify dataset that you can export to CSV, Excel, or JSON, or pass into your own pipeline.

This Actor connects to the [LargitData Social Media Data API](https://www.largitdata.com/en/social-media-api/). **You need a LargitData API key** to use it. Keys are issued after a [trial request](https://www.largitdata.com/en/social-media-api/#api-inquiry). The Actor itself is free. LargitData bills collection at USD 0.005 per record (each returned post or comment counts as one record).

## Supported platforms and data types

| Platform | Keyword search | Post comments | Account timeline |
|---|---|---|---|
| Weibo | Posts | Comments (optional second-level replies) | Yes |
| Xiaohongshu (RedNote) | Notes | Comments (optional second-level replies) | Yes |
| Douyin | Videos | Comments | Yes |
| Threads | Posts | Replies | Yes |
| Bilibili | Videos | Top comments with replies | No |
| Zhihu | Answers and articles | Answers, comments, and replies | No |
| Baidu Tieba | Posts | Floors and replies | No |

Douyin is the mainland China app, not TikTok. TikTok is not supported.

## How to use this Actor

1. Enter your LargitData API key. Without a key, the Actor returns one sample record (marked `"sample": true`) to preview the output format.
2. Choose a platform and collection mode:
   - **Keyword search**: enter a keyword in the platform's language (Simplified Chinese for most platforms), with an optional date range.
   - **Post comments**: enter the post URL.
   - **Account timeline**: enter the account's author ID. On Weibo, Xiaohongshu (RedNote), and Douyin, the date range defaults to the last 30 days.
3. Run the Actor. It creates a collection task, waits for it to finish, and saves every record to the Apify dataset.

Collection runs on LargitData's servers and can take several minutes. If the Actor reaches its timeout while a task is still running, it stops and writes the task ID to the `OUTPUT` record. The task keeps running so you can retrieve it later.

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

Each record includes the fields returned by the API, plus `platform` and `mode`. Here is a sample Xiaohongshu (RedNote) note:

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

See the full field lists for every platform and mode in the [API reference](https://api.infominer.io/docs) and [developer documentation](https://www.largitdata.com/developers/social-media-api/).

## FAQ

**Can I get Weibo data in English?**
Not through this Actor. The LargitData API offers English keyword subscriptions for Weibo with machine translation; see the [Weibo English data page](https://www.largitdata.com/developers/social-media-api/weibo/english-translation/) for details.

**How far back does historical data go?**
Historical range, volume, and refresh frequency are set per project when you request a trial.

**Can LargitData manage data collection for me?**
Yes. LargitData can monitor keywords and accounts, clean and translate the data, backfill historical data, and deliver it to your systems.

## Source code and Python client

Find the OpenAPI spec, Python client, and Actor source code on GitHub: [github.com/ywchiu/social-media-api](https://github.com/ywchiu/social-media-api).

Built by [LargitData](https://www.largitdata.com/en/) (大數軟體), Taipei.
