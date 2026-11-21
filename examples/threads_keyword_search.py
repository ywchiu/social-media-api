"""Threads keyword search API.

Reference: https://www.largitdata.com/developers/social-media-api/threads/keyword-search/
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
    f"{BASE_URL}/threads/search/task",
    headers=HEADERS,
    json={
        "keyword": "登山步道",
        "start_date": "2026-06-01",
        "end_date": "2026-06-30",
        "max_scroll": 5,
        "mask_author": False,
    },
    timeout=30,
)
resp.raise_for_status()
task = resp.json()

# 2. Poll until the task leaves INIT / RUNNING
for _ in range(120):
    resp = requests.get(
        f"{BASE_URL}/threads/search/task/{task['id']}",
        headers=HEADERS,
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

if status == "FAILED":
    raise SystemExit("task failed")
if status != "DONE":
    print("task ended with status", status, "- results may be incomplete")

# 3. Read the records
for row in result.get("data", []):
    print(row.get("url"), (row.get("content") or "")[:60])
