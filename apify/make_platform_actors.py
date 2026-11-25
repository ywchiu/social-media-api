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
            ("comments", "Comments of a post", "Comments on one post (Post URL), with optional second-level replies."),
            ("user_timeline", "Account timeline", "Posts from one account (Author ID). Defaults to the last 30 days."),
        ],
        "replies": True,
        "faq": [
            ("Can I get Weibo data in English with translation?",
             "Not in this Actor. The LargitData API offers English keyword subscriptions for Weibo with machine translation; "
             f"see the [Weibo English data page]({SITE}/developers/social-media-api/weibo/english-translation/)."),
            ("Can I trace Weibo reposts and repost chains?",
             "Not in this Actor. Repost lists and repost-chain tracing are available in the LargitData API; see "
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
            ("keyword_search", "Keyword search", "Notes matching a keyword, with an optional date range."),
            ("comments", "Comments of a note", "Comments on one note (Post URL), with optional second-level replies."),
            ("user_timeline", "Account timeline", "Notes from one account (Author ID). Defaults to the last 30 days."),
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
            ("keyword_search", "Keyword search", "Videos matching a keyword, with an optional date range."),
            ("comments", "Comments of a video", "Comments on one video (Post URL)."),
            ("user_timeline", "Account posts", "Videos from one account (Author ID). Defaults to the last 30 days."),
        ],
        "replies": False,
        "faq": [
            ("Does this Douyin scraper cover TikTok?",
             "No. Douyin is the mainland-China app. TikTok is a separate service and is not covered."),
            ("Does this Douyin scraper download video files?",
             "No. Records include video metadata and text only. Resolving download URLs for collected videos "
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
            ("user_timeline", "Account timeline", "Posts from one public account (Author ID), with an optional date range."),
        ],
        "replies": False,
        "faq": [
            ("Can I collect accounts that reacted to a Threads post?",
             "Not in this Actor. Post reactions are available as a separate task in the LargitData API; see the "
             f"[Threads page]({SITE}/developers/social-media-api/threads/)."),
        ],
    },
}

COMMON_FAQ = [
    ("How far back does historical data go?",
     "Historical range, volume, and refresh frequency are set per project when you request a trial."),
    ("Can LargitData manage data collection for me?",
     "Yes. LargitData can monitor keywords and accounts, clean and translate data, backfill historical data, and "
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
    props["keyword"]["description"] = f"Query term for Keyword search mode, in {cfg['keyword_language']}."
    props["postUrl"]["description"] = f"URL of the {cfg['label']} post whose {cfg['modes'][1][1].split()[0].lower()} you want."
    props["authorId"]["description"] = f"Account ID on {cfg['label']} ({cfg['modes'][2][1]} mode)."
    if key == "threads":
        props["startDate"]["description"] = "YYYY-MM-DD. Optional."
        props["maxPages"]["title"] = "Max scroll depth"
        props["maxPages"]["description"] = "Scroll depth on Threads (max_scroll). Higher values take longer."
    else:
        props["startDate"]["description"] = "Start date (YYYY-MM-DD). Defaults to the last 30 days in Account timeline mode."
        props["maxPages"]["description"] = "Page depth to collect (max_pages). Higher values take longer."
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

{cfg['description'].split(', using your')[0].rstrip('.')}. Export results from the Apify dataset to CSV, Excel, or JSON, or send them to your data pipeline.

This Actor connects to the [LargitData Social Media Data API]({cfg['page']}). **You need a LargitData API key** to run this Actor. Get your key through a [trial request]({TRIAL}). The Actor itself is free. LargitData bills data collection at USD 0.005 per record (each returned post or comment counts as one record).

## Supported data collection modes

| Mode | What you get |
|---|---|
{modes}

## How to run this Actor

1. Enter your LargitData API key. Without a key, the Actor returns one sample record (marked `"sample": true`) to preview the output format.
2. Choose a collection mode and enter a keyword, post URL, or author ID.
3. Start the Actor. It creates a collection task, waits for completion, and saves all records to the Apify dataset.

Collection runs on LargitData's servers and can take several minutes. If the Actor reaches its timeout, it stops and writes the task ID to the `OUTPUT` record. The task keeps running, and you can fetch the results later.

## Input example

```json
{json.dumps(input_example, ensure_ascii=False, indent=2)}
```

## Output example

Each record includes all API response fields plus `platform` and `mode`. Example keyword-search record (sample values, not a real post):

```json
{json.dumps(output_example, ensure_ascii=False, indent=2)}
```

See the complete output field list for every mode on the [{cfg['label']} API page]({cfg['page']}) and in the [API reference](https://api.infominer.io/docs).

## FAQ

{faq}

## Other supported social media platforms

Need more platforms? The [multi-platform Actor]({UMBRELLA}) supports Weibo, Xiaohongshu (RedNote), Douyin, Threads, Bilibili, Zhihu, and Baidu Tieba using the same API key.

## Source code and Python client

OpenAPI specification, Python client, and Actor source code: [github.com/ywchiu/social-media-api](https://github.com/ywchiu/social-media-api)

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
