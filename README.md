# Social Media Data API: Weibo, Xiaohongshu (RedNote), Douyin, Threads, Bilibili, Zhihu, Baidu Tieba

Code examples and an OpenAPI description for the [LargitData Social Media API](https://www.largitdata.com/en/social-media-api/),
which returns public posts, comments, reposts and account timelines as JSON from **Weibo (微博)**,
**Xiaohongshu (RedNote, 小红书)**, **Douyin (抖音)**, **Threads**, **Bilibili (哔哩哔哩)**, **Zhihu (知乎)**
and **Baidu Tieba (百度贴吧)**. Weibo data is also available with
**English machine translation** through a keyword subscription. PTT, Dcard, X, Reddit, Facebook and
Instagram are available through account-configured channels; ask us.

[日本語](README.ja.md)

- Data is collected by web crawlers from content publicly published on each platform. LargitData is not
  affiliated with any of these platforms, and this is not any platform's own API. Whether it suits your
  use depends on the purpose and jurisdiction and is for your legal team to assess; we can describe sources
  and collection methods.
- This is a commercial API. Keys are issued after a trial request:
  **[request a trial](https://www.largitdata.com/en/social-media-api/#api-inquiry)**.
- Besides the API, LargitData can monitor, clean, translate and backfill the data and deliver it into your
  systems as a service.

## How it works

Base URL `https://api.infominer.io/api/v2`; send your key in the `auth-header` request header.
Collection is asynchronous:

1. `POST` creates a task (keyword search, the comments of one post, an account timeline, ...) and returns its `id`.
2. `GET` the task by `id` until its status leaves `INIT` / `RUNNING`.
3. At `DONE`, the same response carries the records (`data`, `total_count`), paged with `page` and `pageSize`.

```bash
curl -X POST https://api.infominer.io/api/v2/weibo/search/task \
  -H "auth-header: $LARGITDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "手冲咖啡", "start_date": "2026-06-01", "end_date": "2026-06-30", "max_pages": 3}'

curl "https://api.infominer.io/api/v2/weibo/search/task/$TASK_ID?page=1&pageSize=100" \
  -H "auth-header: $LARGITDATA_API_KEY"
```

## Endpoints by capability

Each link goes to a page with parameters, response fields, curl and Python examples and a sample response.

| Capability | Endpoints |
|---|---|
| [Weibo keyword search API](https://www.largitdata.com/developers/social-media-api/weibo/keyword-search/) | `POST /weibo/search/task`, `GET /weibo/search/task/{task_id}` |
| [Weibo comments API](https://www.largitdata.com/developers/social-media-api/weibo/comments/) | `POST /weibo/pushs/task`, `GET /weibo/pushs/task/{task_id}` |
| [Weibo repost API and repost-chain tracing](https://www.largitdata.com/developers/social-media-api/weibo/reposts/) | `POST /weibo/reposts/task`, `GET /weibo/reposts/task/{task_id}`, `POST /weibo/repost/parent/task`, `GET /weibo/repost/parent/task/{task_id}` |
| [Weibo user timeline API](https://www.largitdata.com/developers/social-media-api/weibo/user-timeline/) | `POST /weibo/users/task`, `GET /weibo/users/task/{task_id}` |
| [Weibo English translation API](https://www.largitdata.com/developers/social-media-api/weibo/english-translation/) | `POST /weibo/translate/search`, `POST /weibo/translate/pushs`, `POST /weibo/translate/reposts` |
| [Xiaohongshu (RedNote) note search API](https://www.largitdata.com/developers/social-media-api/xiaohongshu/keyword-search/) | `POST /xhs/search/task`, `GET /xhs/search/task/{task_id}` |
| [Xiaohongshu (RedNote) comments API](https://www.largitdata.com/developers/social-media-api/xiaohongshu/comments/) | `POST /xhs/pushs/task`, `GET /xhs/pushs/task/{task_id}` |
| [Xiaohongshu (RedNote) user timeline API](https://www.largitdata.com/developers/social-media-api/xiaohongshu/user-timeline/) | `POST /xhs/users/task`, `GET /xhs/users/task/{task_id}` |
| [Douyin keyword search API](https://www.largitdata.com/developers/social-media-api/douyin/keyword-search/) | `POST /douyin/search/task`, `GET /douyin/search/task/{task_id}` |
| [Douyin comments API](https://www.largitdata.com/developers/social-media-api/douyin/comments/) | `POST /douyin/pushs/task`, `GET /douyin/pushs/task/{task_id}` |
| [Douyin user timeline API](https://www.largitdata.com/developers/social-media-api/douyin/user-timeline/) | `POST /douyin/users/task`, `GET /douyin/users/task/{task_id}` |
| [Threads keyword search API](https://www.largitdata.com/developers/social-media-api/threads/keyword-search/) | `POST /threads/search/task`, `GET /threads/search/task/{task_id}` |
| [Threads replies API](https://www.largitdata.com/developers/social-media-api/threads/replies/) | `POST /threads/pushs/task`, `GET /threads/pushs/task/{task_id}` |
| [Threads user timeline API](https://www.largitdata.com/developers/social-media-api/threads/user-timeline/) | `POST /threads/users/task`, `GET /threads/users/task/{task_id}` |
| [Threads reactions API](https://www.largitdata.com/developers/social-media-api/threads/reactions/) | `POST /threads/reactions/task`, `GET /threads/reactions/task/{task_id}` |
| [Bilibili video keyword search API](https://www.largitdata.com/developers/social-media-api/bilibili/keyword-search/) | `POST /bilibili/search/task`, `GET /bilibili/search/task/{task_id}` |
| [Bilibili comments API](https://www.largitdata.com/developers/social-media-api/bilibili/comments/) | `POST /bilibili/pushs/task`, `GET /bilibili/pushs/task/{task_id}` |
| [Zhihu keyword search API](https://www.largitdata.com/developers/social-media-api/zhihu/keyword-search/) | `POST /zhihu/search/task`, `GET /zhihu/search/task/{task_id}` |
| [Zhihu answers and comments API](https://www.largitdata.com/developers/social-media-api/zhihu/answers-and-comments/) | `POST /zhihu/pushs/task`, `GET /zhihu/pushs/task/{task_id}` |
| [Baidu Tieba thread search API](https://www.largitdata.com/developers/social-media-api/tieba/keyword-search/) | `POST /tieba/search/task`, `GET /tieba/search/task/{task_id}` |
| [Baidu Tieba replies API](https://www.largitdata.com/developers/social-media-api/tieba/replies/) | `POST /tieba/pushs/task`, `GET /tieba/pushs/task/{task_id}` |

Platform references: [Weibo](https://www.largitdata.com/developers/social-media-api/weibo/) ·
[Xiaohongshu](https://www.largitdata.com/developers/social-media-api/xiaohongshu/) ·
[Douyin](https://www.largitdata.com/developers/social-media-api/douyin/) ·
[Threads](https://www.largitdata.com/developers/social-media-api/threads/) ·
[Bilibili](https://www.largitdata.com/developers/social-media-api/bilibili/) ·
[Zhihu](https://www.largitdata.com/developers/social-media-api/zhihu/) ·
[Baidu Tieba](https://www.largitdata.com/developers/social-media-api/tieba/). Full documentation: https://api.infominer.io/docs

## Files

- [`openapi.json`](openapi.json): OpenAPI 3.1 description of the Weibo, Xiaohongshu, Douyin and Threads
  endpoints (2026-10-25 specification snapshot) and the Bilibili, Zhihu and Baidu Tieba endpoints (2026-11-21).
- [`examples/`](examples/): runnable Python scripts (`pip install -r examples/requirements.txt`,
  then `export LARGITDATA_API_KEY=...`).
- [`postman_collection.json`](postman_collection.json): a Postman collection (v2.1) with every endpoint;
  import it and set the `api_key` collection variable.
- [`python/`](python/): `largitdata-social`, a small Python client (create a task, wait for it, read rows).

## Limits worth knowing

- Keyword search results are read up to 100 per page; comments up to 1000 per page.
- Weibo and Xiaohongshu comment tasks can include second-layer replies (`crawl_second_layer`); Douyin cannot.
- Douyin comment tasks collect 50 comments per video by default (`max_items`, `get_all` to change).
- Weibo repost chains are traced up to depth 10 (default 3).
- Threads search, reply and timeline polls return the rows collected so far in `data` with `total_count`,
  readable while the task is still `RUNNING`, paged with `page` and `per_page` (max 1000; the bundled 2026-10-25 OpenAPI
  file still describes these polls as status-only). Reactions tasks return the post's view, like and share counts
  and a paginated reactions list (`per_page` up to 1000) when they complete; `mask_author` removes author
  identity fields. This is a crawler-based service, not Meta's official Threads API.
- Weibo English translation backfills the last 30 days for subscribed keywords; arbitrary posts are not
  translated on demand.
- Bilibili, Zhihu and Baidu Tieba tasks carry `task`, `total_count` and `data` only once `DONE`; other statuses
  return the task object alone. One Bilibili search reaches about 1,000 videos, and a comment task collects at
  most a video's 3 most popular top-level comments and 20 replies under each. Zhihu search covers answers and
  column articles and is not exhaustive. One Tieba search reaches about 620 threads (`depth_capped` tells you
  when the date range was cut short); in-floor replies are capped at 600 per floor.
- How far back data goes, volume and refresh frequency are confirmed per project.

## About

[LargitData](https://www.largitdata.com/en/) (大數軟體有限公司) is a Taipei-based company that builds InfoMiner, RAGi and data
APIs. Questions: use the [trial request form](https://www.largitdata.com/en/social-media-api/#api-inquiry).

Example code in this repository is released under the MIT License. Use of the API itself is governed by
your agreement with LargitData.
