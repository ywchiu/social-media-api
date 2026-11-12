"""Weibo repost API and repost-chain tracing.

Reference: https://www.largitdata.com/developers/social-media-api/weibo/reposts/
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
    f"{BASE_URL}/weibo/reposts/task",
    headers=HEADERS,
    json={
        "post_url": "https://m.weibo.cn/detail/0000000000000001",
    },
    timeout=30,
).json()

# 2. Poll until the task leaves INIT / RUNNING
while True:
    result = requests.get(
        f"{BASE_URL}/weibo/reposts/task/{task['id']}",
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
    print(row["parent_id"], row["author"], row["content"][:60])
