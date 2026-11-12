"""Xiaohongshu (RedNote) note search API.

Reference: https://www.largitdata.com/developers/social-media-api/xiaohongshu/keyword-search/
Set LARGITDATA_API_KEY first; keys are issued after a trial request:
https://www.largitdata.com/en/social-media-api/#api-inquiry
"""
import os
import time
import requests

BASE_URL = "https://api.infominer.io/api/v2"
HEADERS = {"auth-header": os.environ["LARGITDATA_API_KEY"]}

# 1. Create the task
task = requests.post(
    f"{BASE_URL}/xhs/search/task",
    headers=HEADERS,
    json={
        "keyword": "护肤日常",
        "start_date": "2026-06-01",
        "end_date": "2026-06-30",
        "max_pages": 3,
    },
    timeout=30,
).json()

# 2. Poll until the task leaves INIT / RUNNING
while True:
    result = requests.get(
        f"{BASE_URL}/xhs/search/task/{task['id']}",
        headers=HEADERS,
        params={
            "page": 1,
            "pageSize": 100,
        },
        timeout=30,
    ).json()
    status = result.get("status") or result.get("task", {}).get("status")
    if status not in ("INIT", "RUNNING"):
        break
    time.sleep(15)

if status == "FAILED":
    raise SystemExit("task failed")

# 3. Read the records (use page / pageSize to fetch further pages)
for row in result.get("data", []):
    print(row["url"], row["content"][:60])
