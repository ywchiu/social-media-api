# largitdata-social

Python client for the LargitData Social Media Data API (Weibo, Xiaohongshu / RedNote, Douyin, Threads,
Bilibili, Zhihu, Baidu Tieba).
Keys are issued after a trial request: https://www.largitdata.com/en/social-media-api/#api-inquiry

```python
from largitdata_social import Client

client = Client()  # reads LARGITDATA_API_KEY
task = client.create("/weibo/search/task", keyword="手冲咖啡", start_date="2026-06-01", end_date="2026-06-30", max_pages=3)
result = client.wait("/weibo/search/task", task["id"], page=1, pageSize=100)
for row in result.get("data", []):
    print(row.get("url"), (row.get("content") or "")[:60])
```

Endpoints, parameters and response fields: https://www.largitdata.com/developers/social-media-api/
