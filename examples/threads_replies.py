"""Threads replies API.

Reference: https://www.largitdata.com/developers/social-media-api/threads/replies/
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
    f"{BASE_URL}/threads/pushs/task",
    headers=HEADERS,
    json={
        "post_url": "https://www.threads.com/@sample_user_1/post/00000000001",
        "mask_author": False,
    },
    timeout=30,
)
resp.raise_for_status()
task = resp.json()

# 2. Poll until the task leaves INIT / RUNNING
for _ in range(120):
    resp = requests.get(
        f"{BASE_URL}/threads/pushs/task/{task['id']}",
        headers=HEADERS,
        params={
            "page": 1,
            "per_page": 1000,
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

if status == "FAILED":
    raise SystemExit("task failed")
if status != "DONE":
    print("task ended with status", status, "- results may be incomplete")

# 3. Read the records (use page / per_page to fetch further pages)
for row in result.get("data", []):
    print(row.get("reply_level"), row.get("author"), (row.get("content") or "")[:60])
