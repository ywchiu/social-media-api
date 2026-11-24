# 社群數據 API：微博、小紅書、抖音、Threads、嗶哩嗶哩、知乎、百度貼吧

[大數軟體 LargitData 社群數據 API](https://www.largitdata.com/社群媒體API/) 的程式範例與 OpenAPI 描述。
API 以 JSON 回傳 **微博**、**小紅書（RedNote）**、**抖音**、**Threads**、**嗶哩嗶哩**、**知乎**、**百度貼吧** 的公開貼文、留言、轉發與帳號時間軸。
微博另可用英文關鍵字訂閱，取得英文機器翻譯。PTT、Dcard、X、Reddit、Facebook、Instagram 以帳號設定的頻道與關鍵字組提供，請洽詢。

[English](README.md) · [日本語](README.ja.md)

- 大數軟體與這些平台沒有關係，這也不是任何平台的官方 API。
- 這是商用 API，申請試用後發給金鑰：**[申請試用](https://www.largitdata.com/社群媒體API/#api-inquiry)**。
- 除了 API，也可以由大數軟體代為監測、清理、翻譯、回補歷史資料，直接交付到您的系統。

## 可以蒐集什麼

| 平台 | 關鍵字搜尋 | 留言／回覆 | 帳號時間軸 | 其他 |
|---|---|---|---|---|
| 微博 | 貼文 | 留言，可含第二層回覆 | 有 | 轉發與轉發鏈追蹤（最多 10 層）；英文關鍵字訂閱與英文機器翻譯 |
| 小紅書（RedNote） | 筆記 | 留言，可含第二層回覆 | 有 | |
| 抖音 | 影片 | 留言（預設每支影片 50 則，可調整） | 有 | |
| Threads | 貼文 | 回覆 | 有 | 貼文的瀏覽、按讚、分享數與互動列表 |
| 嗶哩嗶哩 | 影片（每次查詢約 1,000 支） | 最熱門 3 則留言，各含前 20 則回覆 | | |
| 知乎 | 回答與專欄文章 | 問題的回答；回答與文章的留言及回覆 | | |
| 百度貼吧 | 貼文（每次查詢約 620 篇） | 樓層與樓中樓回覆 | | |

快手的影片搜尋與留言、微信公眾號文章也可蒐集；端點說明隨試用提供，不在這個 repo 裡。

## 運作方式

Base URL 是 `https://api.infominer.io/api/v2`，金鑰放在 `auth-header` 標頭。蒐集採非同步任務：

1. `POST` 建立任務（關鍵字搜尋、某篇貼文的留言、帳號時間軸等），取得任務 `id`。
2. 用 `GET` 查詢該任務，直到狀態離開 `INIT`／`RUNNING`。
3. 狀態為 `DONE` 時，同一個回應會帶回資料（`data`、`total_count`），以 `page` 與 `pageSize` 分頁。

```bash
curl -X POST https://api.infominer.io/api/v2/xhs/search/task \
  -H "auth-header: $LARGITDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "护肤日常", "start_date": "2026-06-01", "end_date": "2026-06-30", "max_pages": 3}'

curl "https://api.infominer.io/api/v2/xhs/search/task/$TASK_ID?page=1&pageSize=100" \
  -H "auth-header: $LARGITDATA_API_KEY"
```

完成後的小紅書筆記搜尋回應如下（範例值）：

```json
{
  "keyword": "护肤日常",
  "status": "DONE",
  "total_count": 2,
  "task": {"id": "00000000-0000-4000-8000-000000000001", "status": "DONE"},
  "data": [
    {
      "source": "xhs_note",
      "platform": "rednote",
      "url": "https://www.xiaohongshu.com/explore/000000000000000000000001",
      "mblogid": "000000000000000000000001",
      "content": "换季之后我把早晚的护肤步骤简化成四步，记录一下这个月的肤况 #护肤日常",
      "author": "sample_user_1",
      "author_id": "0000000000000001",
      "tm": 1781056800,
      "metadata_tags": ["护肤日常", "换季保养"],
      "like_count": 120,
      "comment_count": 14,
      "share_count": 6
    }
  ]
}
```

### Apify Actor

也可以在 Apify 上執行：[apify.com/largitdata/social-media-api](https://apify.com/largitdata/social-media-api)。填入自己的 API 金鑰，結果會存成 Apify dataset，可匯出 CSV、Excel 或 JSON。

### Python client

```bash
pip install "git+https://github.com/ywchiu/social-media-api#subdirectory=python"
export LARGITDATA_API_KEY=...
```

```python
from largitdata_social import Client

client = Client()  # 讀取 LARGITDATA_API_KEY
task = client.create("/xhs/search/task", keyword="护肤日常", start_date="2026-06-01", end_date="2026-06-30", max_pages=3)
result = client.wait("/xhs/search/task", task["id"], page=1, pageSize=100)
for row in result.get("data", []):
    print(row["url"], row.get("like_count"), (row.get("content") or "")[:60])
```

## 各功能文件

每個連結都有參數、回應欄位、curl 與 Python 範例和範例回應。

- 微博：[關鍵字搜尋](https://www.largitdata.com/開發者中心/社群媒體API/weibo/keyword-search/) · [留言](https://www.largitdata.com/開發者中心/社群媒體API/weibo/comments/) · [轉發與轉發鏈](https://www.largitdata.com/開發者中心/社群媒體API/weibo/reposts/) · [帳號時間軸](https://www.largitdata.com/開發者中心/社群媒體API/weibo/user-timeline/) · [英譯資料](https://www.largitdata.com/開發者中心/社群媒體API/weibo/english-translation/)
- 小紅書：[筆記搜尋](https://www.largitdata.com/開發者中心/社群媒體API/xiaohongshu/keyword-search/) · [留言與回覆](https://www.largitdata.com/開發者中心/社群媒體API/xiaohongshu/comments/) · [帳號時間軸](https://www.largitdata.com/開發者中心/社群媒體API/xiaohongshu/user-timeline/)
- 抖音：[影片搜尋](https://www.largitdata.com/開發者中心/社群媒體API/douyin/keyword-search/) · [留言](https://www.largitdata.com/開發者中心/社群媒體API/douyin/comments/) · [帳號時間軸](https://www.largitdata.com/開發者中心/社群媒體API/douyin/user-timeline/)
- Threads：[關鍵字搜尋](https://www.largitdata.com/開發者中心/社群媒體API/threads/keyword-search/) · [回覆](https://www.largitdata.com/開發者中心/社群媒體API/threads/replies/) · [帳號時間軸](https://www.largitdata.com/開發者中心/社群媒體API/threads/user-timeline/) · [互動](https://www.largitdata.com/開發者中心/社群媒體API/threads/reactions/)
- 嗶哩嗶哩：[影片搜尋](https://www.largitdata.com/開發者中心/社群媒體API/bilibili/keyword-search/) · [留言](https://www.largitdata.com/開發者中心/社群媒體API/bilibili/comments/)
- 知乎：[關鍵字搜尋](https://www.largitdata.com/開發者中心/社群媒體API/zhihu/keyword-search/) · [回答與留言](https://www.largitdata.com/開發者中心/社群媒體API/zhihu/answers-and-comments/)
- 百度貼吧：[貼文搜尋](https://www.largitdata.com/開發者中心/社群媒體API/tieba/keyword-search/) · [樓層與回覆](https://www.largitdata.com/開發者中心/社群媒體API/tieba/replies/)

完整文件：https://api.infominer.io/docs

## 常見問題

**這是微博、小紅書、抖音或 Threads 的官方 API 嗎？**
不是。這是大數軟體自己的 API，與各平台沒有關係。

**可以用 JSON 取得小紅書筆記的留言嗎？**
可以。用筆記網址呼叫 `POST /xhs/pushs/task` 蒐集留言，可選擇包含第二層回覆；`POST /xhs/search/task` 則是用關鍵字搜尋筆記。

**看不懂中文，可以讀英文版的微博嗎？**
可以訂閱英文關鍵字：系統會轉成中文搜尋詞，回補近 30 天符合的貼文並附英文機器翻譯。不在訂閱範圍內的貼文不提供即時翻譯。

**抖音和 TikTok 一樣嗎？**
不一樣。抖音是中國大陸使用的 App，內容獨立。這個 API 涵蓋抖音，不含 TikTok。

**資料可以回溯多久、多久更新一次？**
歷史範圍、資料量與更新頻率會在申請試用時依專案確認。

**可以不自己呼叫 API，直接交付資料嗎？**
可以。大數軟體可以代為監測關鍵字與帳號、清理與翻譯資料、回補歷史，再交付到您的系統。

## 關於

[大數軟體有限公司](https://www.largitdata.com/)（LargitData）位於台北，開發 InfoMiner、RAGi 與數據 API。問題請透過[試用申請表](https://www.largitdata.com/社群媒體API/#api-inquiry)聯絡。

本 repo 的範例程式以 MIT 授權釋出。API 本身的使用依您與大數軟體的合約。
