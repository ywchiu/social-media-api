"""Weibo English translation API.

Reference: https://www.largitdata.com/developers/social-media-api/weibo/english-translation/
Set LARGITDATA_API_KEY first; keys are issued after a trial request:
https://www.largitdata.com/en/social-media-api/#api-inquiry
"""
import os
import requests

BASE_URL = "https://api.infominer.io/api/v2"
HEADERS = {"auth-header": os.environ["LARGITDATA_API_KEY"]}

# Translated posts for your subscribed keywords (no task needed)
posts = requests.post(
    f"{BASE_URL}/weibo/translate/search",
    headers=HEADERS,
    json={
        "keywords": "coffee OR latte",
        "startDate": "2026-06-01 00:00:00",
        "endDate": "2026-06-30 23:59:59",
        "dateType": "post_time",
        "sorted": "tm",
        "page": 1,
        "pageSize": 50,
    },
    timeout=30,
).json()
print(posts["total_count"], "translated posts")

# Translated comments of one post
comments = requests.post(
    f"{BASE_URL}/weibo/translate/pushs",
    headers=HEADERS,
    json={
        "post_id": "0000000000000001",
        "page": 1,
        "pageSize": 50,
    },
    timeout=30,
).json()
for row in comments.get("data", []):
    print(row["author"], row["content"][:60])
