"""Generate the single-platform Apify Actors under apify-platforms/.

Each folder is a complete Actor (its own .actor/, Dockerfile, README and a
copy of apify/src) so Apify can build it from this repository with the folder
as the build context. Run after changing apify/src or this file:

    python3 apify/make_platform_actors.py
"""
import copy
import json
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "apify-platforms"
SITE = "https://www.largitdata.com"
TRIAL = f"{SITE}/en/social-media-api/#api-inquiry"
UMBRELLA = "https://apify.com/largitdata/social-media-api"

PLATFORMS = {
    "weibo": {
        "name": "weibo-scraper",
        "title": "Weibo Scraper: Posts, Comments & Account Timelines",
        "label": "Weibo",
        "description": "Collect public Weibo posts by keyword, the comments of a post and account timelines "
                       "as JSON, using your LargitData Social Media Data API key.",
        "page": f"{SITE}/developers/social-media-api/weibo/",
        "keyword": "新能源汽车",
        "keyword_language": "Simplified Chinese",
        "post_noun": "posts",
        "modes": [
            ("keyword_search", "Keyword search", "Posts matching a keyword, optionally within a date range."),
            ("comments", "Comments of a post", "Comments of one post (Post URL), optionally with second-level replies."),
            ("user_timeline", "Account timeline", "One account's posts (Author ID). The date range defaults to the last 30 days."),
        ],
        "replies": True,
        "faq": [
            ("Can I read Weibo in English?",
             "The LargitData API offers English keyword subscriptions for Weibo with machine translation. That "
             f"feature is not part of this Actor; see the [Weibo English data page]({SITE}/developers/social-media-api/weibo/english-translation/)."),
            ("Can I trace reposts?",
             "Repost lists and repost-chain tracing are available in the LargitData API, not in this Actor; see "
             f"the [Weibo reposts page]({SITE}/developers/social-media-api/weibo/reposts/)."),
        ],
    },
    "xiaohongshu": {
        "name": "xiaohongshu-rednote-scraper",
        "title": "Xiaohongshu (RedNote) Scraper: Notes, Comments, Accounts",
        "label": "Xiaohongshu (RedNote)",
        "description": "Collect public Xiaohongshu (RedNote) notes by keyword, the comments of a note and account "
                       "timelines as JSON, using your LargitData Social Media Data API key.",
        "page": f"{SITE}/developers/social-media-api/xiaohongshu/",
        "keyword": "护肤日常",
        "keyword_language": "Simplified Chinese",
        "post_noun": "notes",
        "modes": [
            ("keyword_search", "Keyword search", "Notes matching a keyword, optionally within a date range."),
            ("comments", "Comments of a note", "Comments of one note (Post URL), optionally with second-level replies."),
            ("user_timeline", "Account timeline", "One account's notes (Author ID). The date range defaults to the last 30 days."),
        ],
        "replies": True,
        "faq": [
            ("Are Xiaohongshu, RedNote and XHS the same platform?",
             "Yes. Xiaohongshu (小红书) is the platform's Chinese name, RedNote is the name used in app stores "
             "outside mainland China, and XHS is the common abbreviation."),
        ],
    },
    "douyin": {
        "name": "douyin-scraper",
        "title": "Douyin Scraper: Videos, Comments & Account Posts",
        "label": "Douyin",
        "description": "Collect public Douyin videos by keyword, the comments of a video and account posts as JSON, "
                       "using your LargitData Social Media Data API key. Douyin is the mainland-China app, not TikTok.",
        "page": f"{SITE}/developers/social-media-api/douyin/",
        "keyword": "露营装备",
        "keyword_language": "Simplified Chinese",
        "post_noun": "videos",
        "modes": [
            ("keyword_search", "Keyword search", "Videos matching a keyword, optionally within a date range."),
            ("comments", "Comments of a video", "Comments of one video (Post URL)."),
            ("user_timeline", "Account posts", "One account's videos (Author ID). The date range defaults to the last 30 days."),
        ],
        "replies": False,
        "faq": [
            ("Does it cover TikTok?",
             "No. Douyin is the mainland-China app. TikTok is a separate service and is not covered."),
            ("Does it download the video files?",
             "No. The records carry the video's metadata and text. Resolving download URLs for collected videos "
             f"is a separate LargitData API endpoint; see the [Douyin page]({SITE}/developers/social-media-api/douyin/)."),
        ],
    },
    "threads": {
        "name": "threads-scraper",
        "title": "Threads Scraper: Keyword Search, Replies & Timelines",
        "label": "Threads",
        "description": "Collect public Threads posts by keyword, the replies to a post and public account timelines "
                       "as JSON, using your LargitData Social Media Data API key.",
        "page": f"{SITE}/developers/social-media-api/threads/",
        "keyword": "珍珠奶茶",
        "keyword_language": "the language of the posts you want",
        "post_noun": "posts",
        "modes": [
            ("keyword_search", "Keyword search", "Posts matching a keyword, optionally within a date range."),
            ("comments", "Replies to a post", "Replies to one post (Post URL)."),
            ("user_timeline", "Account timeline", "One public account's posts (Author ID), optionally within a date range."),
        ],
        "replies": False,
        "faq": [
            ("Can I get the accounts that reacted to a post?",
             "Reactions are available as a separate task in the LargitData API, not in this Actor; see the "
             f"[Threads page]({SITE}/developers/social-media-api/threads/)."),
        ],
    },
}

COMMON_FAQ = [
    ("How far back does the data go?",
     "History range, volume and refresh frequency are agreed per project when you request a trial."),
    ("Can LargitData run the collection for me?",
     "Yes. LargitData can monitor keywords and accounts, clean and translate the data, backfill history and "
     "deliver it to your systems."),
]


def sample_records():
    """Read SAMPLE_RECORDS out of apify/src/main.py without importing apify."""
    source = (HERE / "src" / "main.py").read_text(encoding="utf-8")
    start = source.index("SAMPLE_RECORDS = {")
    end = source.index("\n}\n", start) + 3
    scope = {}
    exec(source[start:end], scope)
    return scope["SAMPLE_RECORDS"]


def input_schema(key, cfg):
    schema = json.loads((HERE / ".actor" / "input_schema.json").read_text(encoding="utf-8"))
    props = schema["properties"]
    del props["platform"]
    schema["required"] = ["mode"]
    schema["title"] = f"{cfg['label']} data collection"
    props["mode"]["enum"] = [m[0] for m in cfg["modes"]]
    props["mode"]["enumTitles"] = [m[1] for m in cfg["modes"]]
    props["mode"]["description"] = " ".join(f"{title}: {desc}" for _, title, desc in cfg["modes"])
    props["keyword"]["prefill"] = cfg["keyword"]
    props["keyword"]["description"] = f"Search keyword for Keyword search, in {cfg['keyword_language']}."
    props["postUrl"]["description"] = f"URL of the {cfg['label']} post whose {cfg['modes'][1][1].split()[0].lower()} you want."
    props["authorId"]["description"] = f"Account ID on {cfg['label']} ({cfg['modes'][2][1]} mode)."
    if key == "threads":
        props["startDate"]["description"] = "YYYY-MM-DD. Optional."
        props["maxPages"]["title"] = "Max scroll depth"
        props["maxPages"]["description"] = "How deep the collector scrolls on Threads (max_scroll). Larger values take longer."
    else:
        props["startDate"]["description"] = "YYYY-MM-DD. Account timeline defaults to the last 30 days when left empty."
        props["maxPages"]["description"] = "How deep the collector goes on the platform (max_pages). Larger values take longer."
    if not cfg["replies"]:
        del props["includeReplies"]
    return schema


def actor_json(cfg):
    actor = json.loads((HERE / ".actor" / "actor.json").read_text(encoding="utf-8"))
    actor = copy.deepcopy(actor)
    actor["name"] = cfg["name"]
    actor["title"] = cfg["title"]
    assert len(cfg["title"]) <= 63, cfg["title"]
    actor["description"] = cfg["description"]
    return actor


def readme(key, cfg, sample):
    input_example = {"apiKey": "YOUR_LARGITDATA_API_KEY", "mode": "keyword_search", "keyword": cfg["keyword"],
                     "startDate": "2026-06-01", "endDate": "2026-06-30", "maxPages": 3, "maxItems": 1000}
    output_example = {"platform": key, "mode": "keyword_search", **sample}
    modes = "\n".join(f"| {title} | {desc} |" for _, title, desc in cfg["modes"])
    faq = "\n\n".join(f"**{q}**\n{a}" for q, a in cfg["faq"] + COMMON_FAQ)
    return f"""# {cfg['title']}

{cfg['description'].split(', using your')[0].rstrip('.')}. Results land in an Apify dataset you can export to CSV, Excel or JSON, or pass on to your own pipeline.

This Actor is a thin client for the [LargitData Social Media Data API]({cfg['page']}). **You need a LargitData API key** to use it; keys are issued after a [trial request]({TRIAL}). The Actor itself is free; collection is billed by LargitData at USD 0.005 per record (each post or comment returned counts as one record).

## What you can collect

| Mode | What you get |
|---|---|
{modes}

## How to use it

1. Paste your LargitData API key. Without a key, the Actor returns one sample record (marked `"sample": true`) so you can see the output format.
2. Pick what to collect and fill in the keyword, post URL or author ID.
3. Run. The Actor creates a collection task, waits for it to finish, and saves every record to the dataset.

Collection runs on LargitData's side and can take several minutes. If a task is still running when the timeout is reached, the Actor stops and writes the task ID to the `OUTPUT` record; the task keeps running and you can fetch it later.

## Input example

```json
{json.dumps(input_example, ensure_ascii=False, indent=2)}
```

## Output example

Each record keeps the fields the API returns, plus `platform` and `mode`. A keyword-search record looks like this (sample values, not a real post):

```json
{json.dumps(output_example, ensure_ascii=False, indent=2)}
```

The full field list for every mode is on the [{cfg['label']} API page]({cfg['page']}) and in the [API reference](https://api.infominer.io/docs).

## FAQ

{faq}

## Other platforms

The [multi-platform Actor]({UMBRELLA}) covers Weibo, Xiaohongshu (RedNote), Douyin, Threads, Bilibili, Zhihu and Baidu Tieba with the same API key.

## Source code

OpenAPI description, Python client and this Actor's source: [github.com/ywchiu/social-media-api](https://github.com/ywchiu/social-media-api)

Built by [LargitData]({SITE}/en/) (大數軟體), Taipei.
"""


def main():
    samples = sample_records()
    if OUT.exists():
        shutil.rmtree(OUT)
    for key, cfg in PLATFORMS.items():
        folder = OUT / cfg["name"]
        (folder / ".actor").mkdir(parents=True)
        shutil.copytree(HERE / "src", folder / "src", ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copy(HERE / "requirements.txt", folder / "requirements.txt")
        shutil.copy(HERE / ".actor" / "output_schema.json", folder / ".actor" / "output_schema.json")
        dockerfile = (HERE / "Dockerfile").read_text(encoding="utf-8")
        dockerfile = dockerfile.replace("CMD ", f"ENV LARGITDATA_PLATFORM={key}\nCMD ")
        assert f"LARGITDATA_PLATFORM={key}" in dockerfile
        (folder / "Dockerfile").write_text(dockerfile, encoding="utf-8")
        dump = lambda obj: json.dumps(obj, ensure_ascii=False, indent=2) + "\n"
        (folder / ".actor" / "actor.json").write_text(dump(actor_json(cfg)), encoding="utf-8")
        (folder / ".actor" / "input_schema.json").write_text(dump(input_schema(key, cfg)), encoding="utf-8")
        (folder / "README.md").write_text(readme(key, cfg, samples[key]), encoding="utf-8")
        print("wrote", folder.relative_to(OUT.parent))


if __name__ == "__main__":
    main()
