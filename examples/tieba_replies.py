"""Baidu Tieba replies API.

Reference: https://www.largitdata.com/developers/social-media-api/tieba/replies/
Set LARGITDATA_API_KEY first; keys are issued after a trial request:
https://www.largitdata.com/en/social-media-api/#api-inquiry
"""
import os
import time
import requests

BASE_URL = "https://api.infominer.io/api/v2"
HEADERS = {"auth-header": os.environ["LARGITDATA_API_KEY"]}

# 1. Create the task
resp = requests.post(
    f"{BASE_URL}/tieba/pushs/task",
    headers=HEADERS,
    json={
        "post_url": "https://tieba.baidu.com/p/10000000001",
        "crawl_second_layer": True,
        "max_pages": 2,
    },
    timeout=30,
)
resp.raise_for_status()
task = resp.json()

# 2. Poll until the task leaves INIT / RUNNING
for _ in range(120):
    resp = requests.get(
        f"{BASE_URL}/tieba/pushs/task/{task['id']}",
        headers=HEADERS,
        params={
            "page": 1,
            "pageSize": 1000,
        },
        timeout=30,
    )
    resp.raise_for_status()
    result = resp.json()
    status = result.get("status") or result.get("task", {}).get("status")
    if status not in ("INIT", "RUNNING"):
        break
    time.sleep(15)
else:
    raise SystemExit("task still running; poll it again later")

task = result.get("task", result)
if status != "DONE" or task.get("partial") or task.get("timed_out"):
    raise SystemExit(f"task ended with status {status}; no complete result")

# 3. Read the records (use page / pageSize to fetch further pages)
for row in result.get("data", []):
    print(row.get("push_type"), row.get("author"), (row.get("content") or "")[:60])
