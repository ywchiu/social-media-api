"""Apify Actor: collect public social media data through the LargitData Social Media Data API.

The API is asynchronous: POST creates a collection task, GET polls it until the
status leaves INIT / RUNNING, and the finished task carries the rows. This
Actor runs that loop and saves the rows to the default dataset. It is not any
platform's official API; users bring their own key.
"""
import asyncio
import os
from datetime import date, timedelta

import httpx
from apify import Actor

BASE_URL = os.environ.get("LARGITDATA_BASE_URL", "https://api.infominer.io/api/v2").rstrip("/")
# Single-platform Actors (apify-platforms/) set this in their Dockerfile and
# have no platform field in their input.
FIXED_PLATFORM = os.environ.get("LARGITDATA_PLATFORM", "").strip()

PLATFORM_PATH = {
    "weibo": "weibo",
    "xiaohongshu": "xhs",
    "douyin": "douyin",
    "threads": "threads",
    "bilibili": "bilibili",
    "zhihu": "zhihu",
    "tieba": "tieba",
}
TIMELINE_PLATFORMS = {"weibo", "xiaohongshu", "douyin", "threads"}
# Platforms whose comment task takes a page depth instead of fetching everything.
PAGED_COMMENTS = {"bilibili", "zhihu", "tieba"}
PAGE_SIZE = 100

# Returned when no API key is given, so the Actor can be tried (and Apify's
# daily health check passes) without anyone's key. Clearly marked as a sample.
SAMPLE_NOTE = {
    "sample": True,
    "note": "Sample record. Add your LargitData API key to collect real data: "
            "https://www.largitdata.com/en/social-media-api/#api-inquiry",
}
# One made-up keyword-search record per platform; the values are not real posts.
SAMPLE_RECORDS = {
    "xiaohongshu": {
        "source": "xhs_note",
        "url": "https://www.xiaohongshu.com/explore/000000000000000000000001",
        "content": "换季之后我把早晚的护肤步骤简化成四步，记录一下这个月的肤况 #护肤日常",
        "author": "sample_user_1",
        "author_id": "0000000000000001",
        "tm": 1781056800,
        "metadata_tags": ["护肤日常", "换季保养"],
        "like_count": 120,
        "comment_count": 14,
        "share_count": 6,
    },
    "weibo": {
        "url": "https://weibo.com/0000000001/Sample0001",
        "content": "周末去试驾了两款新能源汽车，续航和充电速度差别比想象的大 #新能源汽车",
        "author": "sample_user_1",
        "author_id": "0000000001",
        "tm": 1781056800,
        "datetime": "2026-06-10 10:00:00",
        "metadata_tags": ["新能源汽车"],
        "like_count": 86,
        "comment_count": 12,
        "share_count": 5,
    },
    "douyin": {
        "url": "https://www.douyin.com/video/0000000000000000001",
        "post_id": "0000000000000000001",
        "content": "第一次带全家去露营，这几样装备真的省事 #露营装备",
        "author": "sample_user_1",
        "tm": 1781056800,
        "date": "2026-06-10",
        "metadata_tags": ["露营装备"],
        "like_count": 240,
        "comment_count": 31,
        "share_count": 18,
        "video_length": 42,
    },
    "threads": {
        "url": "https://www.threads.com/@sample_user_1/post/Sample00001",
        "post_id": "Sample00001",
        "content": "今天試了巷口新開的手搖店，珍珠奶茶半糖剛剛好",
        "author": "sample_user_1",
        "author_id": "0000000001",
        "tm": 1781056800,
        "like_count": 35,
        "comment_count": 4,
        "share_count": 1,
        "is_reply": False,
        "is_quote": False,
        "keyword": "珍珠奶茶",
    },
}


class InputError(ValueError):
    pass


def build_task(inp):
    """Return (path, body, paged) for the collection task the input asks for."""
    platform = FIXED_PLATFORM or inp.get("platform") or "weibo"
    mode = inp.get("mode") or "keyword_search"
    if platform not in PLATFORM_PATH:
        raise InputError(f"Unknown platform: {platform}")
    p = PLATFORM_PATH[platform]
    max_pages = int(inp.get("maxPages") or 3)
    start, end = inp.get("startDate") or None, inp.get("endDate") or None
    # The date picker may hand back an ISO timestamp; the API wants YYYY-MM-DD.
    start = start[:10] if start else None
    end = end[:10] if end else None
    threads = platform == "threads"

    if mode == "keyword_search":
        keyword = (inp.get("keyword") or "").strip()
        if not keyword:
            raise InputError("Keyword search needs a keyword.")
        body = {"keyword": keyword}
        body["max_scroll" if threads else "max_pages"] = max_pages
        if start:
            body["start_date"] = start
        if end:
            body["end_date"] = end
        return f"/{p}/search/task", body, not threads

    if mode == "comments":
        post_url = (inp.get("postUrl") or "").strip()
        if not post_url:
            raise InputError("Comments mode needs a post URL.")
        body = {"post_url": post_url}
        if threads:
            body["max_scroll"] = max_pages
        else:
            body["crawl_second_layer"] = bool(inp.get("includeReplies"))
            if platform in PAGED_COMMENTS:
                body["max_pages"] = max_pages
        return f"/{p}/pushs/task", body, not threads

    if mode == "user_timeline":
        if platform not in TIMELINE_PLATFORMS:
            raise InputError("Account timeline is available for Weibo, Xiaohongshu, Douyin and Threads.")
        author_id = (inp.get("authorId") or "").strip()
        if not author_id:
            raise InputError("Account timeline needs an author ID.")
        body = {"author_id": author_id}
        if threads:
            body["max_scroll"] = max_pages
            if start:
                body["start_date"] = start
            if end:
                body["end_date"] = end
        else:
            # Required on these platforms; default to the last 30 days.
            end = end or date.today().isoformat()
            start = start or (date.fromisoformat(end) - timedelta(days=30)).isoformat()
            body["startDate"], body["endDate"] = start, end
        return f"/{p}/users/task", body, False

    raise InputError(f"Unknown mode: {mode}")


def task_status(result):
    return result.get("status") or (result.get("task") or {}).get("status")


def task_id(created):
    return created.get("id") or (created.get("task") or {}).get("id")


async def call(client, method, path, **kwargs):
    resp = await client.request(method, BASE_URL + path, **kwargs)
    if resp.status_code in (401, 403):
        raise InputError("The API key was rejected. Check the key, or request one at "
                         "https://www.largitdata.com/en/social-media-api/#api-inquiry")
    resp.raise_for_status()
    return resp.json()


async def main():
    async with Actor:
        inp = await Actor.get_input() or {}
        api_key = (inp.get("apiKey") or "").strip()
        platform = FIXED_PLATFORM or inp.get("platform") or "weibo"
        if not api_key:
            sample_platform = platform if platform in SAMPLE_RECORDS else "xiaohongshu"
            await Actor.push_data([{"platform": sample_platform, "mode": "keyword_search",
                                    **SAMPLE_NOTE, **SAMPLE_RECORDS[sample_platform]}])
            await Actor.exit(status_message="No API key given, so only a sample record was returned. "
                                            "Request a key at https://www.largitdata.com/en/social-media-api/#api-inquiry")
            return
        try:
            path, body, paged = build_task(inp)
        except InputError as e:
            await Actor.fail(status_message=str(e))
            return

        max_items = int(inp.get("maxItems") or 0)
        interval = int(inp.get("pollIntervalSecs") or 15)
        deadline = asyncio.get_running_loop().time() + 60 * int(inp.get("timeoutMins") or 30)
        extra = {"platform": platform, "mode": inp.get("mode") or "keyword_search"}

        async with httpx.AsyncClient(headers={"auth-header": api_key}, timeout=60) as client:
            try:
                created = await call(client, "POST", path, json=body)
            except InputError as e:
                await Actor.fail(status_message=str(e))
                return
            tid = task_id(created)
            if not tid:
                await Actor.fail(status_message=f"Unexpected response when creating the task: {str(created)[:300]}")
                return
            Actor.log.info(f"Created task {tid} at {path}")
            await Actor.set_status_message(f"Task {tid} running")

            query = {"page": 1, "pageSize": PAGE_SIZE} if paged else None
            while True:
                result = await call(client, "GET", f"{path}/{tid}", params=query)
                status = task_status(result)
                if status not in ("INIT", "RUNNING"):
                    break
                if asyncio.get_running_loop().time() > deadline:
                    await Actor.set_value("OUTPUT", {"task_id": tid, "path": path, "status": status})
                    await Actor.exit(status_message=f"Task {tid} still {status}; it keeps running on "
                                                    "LargitData's side. Re-run later to fetch it.")
                    return
                await asyncio.sleep(interval)

            if status == "FAILED":
                await Actor.fail(status_message=f"Task {tid} failed on LargitData's side.")
                return
            if status != "DONE":
                Actor.log.warning(f"Task {tid} ended with status {status}; results may be incomplete.")

            saved, page = 0, 1
            total = result.get("total_count")
            while True:
                rows = result.get("data") or []
                if max_items:
                    rows = rows[: max_items - saved]
                if rows:
                    await Actor.push_data([{**extra, **row} for row in rows])
                    saved += len(rows)
                done = (not paged or not rows or (max_items and saved >= max_items)
                        or (total is not None and page * PAGE_SIZE >= total))
                if done:
                    break
                page += 1
                result = await call(client, "GET", f"{path}/{tid}", params={"page": page, "pageSize": PAGE_SIZE})

        await Actor.set_value("OUTPUT", {"task_id": tid, "path": path, "status": status,
                                         "total_count": total, "saved": saved})
        await Actor.set_status_message(f"Saved {saved} records (task {tid}, {status})")
