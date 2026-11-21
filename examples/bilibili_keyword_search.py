"""Bilibili video keyword search API.

Reference: https://www.largitdata.com/developers/social-media-api/bilibili/keyword-search/
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
    f"{BASE_URL}/bilibili/search/task",
    headers=HEADERS,
    json={
        "keyword": "露营装备",
        "start_date": "2026-06-01",
        "end_date": "2026-06-07",
        "max_pages": 3,
    },
    timeout=30,
)
resp.raise_for_status()
task = resp.json()

# 2. Poll until the task leaves INIT / RUNNING
for _ in range(120):
    resp = requests.get(
        f"{BASE_URL}/bilibili/search/task/{task['id']}",
        headers=HEADERS,
        params={
            "page": 1,
            "pageSize": 100,
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
    print(row.get("url"), (row.get("title") or "")[:60])
