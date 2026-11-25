# 社群數據 API：微博、小紅書、抖音、Threads、嗶哩嗶哩、知乎、百度貼吧

本儲存庫提供 [大數軟體 LargitData 社群數據 API](https://www.largitdata.com/社群媒體API/)（社群媒體爬蟲 API）的程式範例與 OpenAPI 規格。
透過本 API 可取得 **微博**、**小紅書（RedNote）**、**抖音**、**Threads**、**嗶哩嗶哩**、**知乎**、**百度貼吧** 的公開貼文、留言、轉發與帳號時間軸，並以 JSON 格式回傳。
微博另支援英文關鍵字訂閱，並提供英文機器翻譯。PTT、Dcard、X、Reddit、Facebook、Instagram 則依帳號設定的頻道與關鍵字組提供，歡迎洽詢。

[English](README.md) · [日本語](README.ja.md)

- 本服務為商用 API，申請試用後即可取得 API 金鑰：**[申請試用](https://www.largitdata.com/社群媒體API/#api-inquiry)**。
- 若不自行串接 API，亦可由大數軟體代為監測、清理、翻譯並回補歷史資料，直接交付至您的系統。

## 支援的平台與資料項目

| 平台 | 關鍵字搜尋 | 留言／回覆 | 帳號時間軸 | 其他 |
|---|---|---|---|---|
| 微博 | 貼文 | 留言（可含第二層回覆） | 支援 | 轉發與轉發鏈追蹤（最多 10 層）；英文關鍵字訂閱與英文機器翻譯 |
| 小紅書（RedNote） | 筆記 | 留言（可含第二層回覆） | 支援 | |
| 抖音 | 影片 | 留言（預設每支影片 50 則，可調整） | 支援 | |
| Threads | 貼文 | 回覆 | 支援 | 貼文瀏覽、按讚、分享數與互動列表 |
| 嗶哩嗶哩 | 影片（每次查詢約 1,000 支） | 最熱門 3 則留言，各含前 20 則回覆 | | |
| 知乎 | 回答與專欄文章 | 問題的回答；回答與文章的留言及回覆 | | |
| 百度貼吧 | 貼文（每次查詢約 620 篇） | 樓層與樓中樓回覆 | | |

另支援快手影片搜尋與留言，以及微信公眾號文章；相關端點文件將隨試用申請提供，未收錄於本儲存庫。

## API 運作方式與呼叫流程

Base URL 為 `https://api.infominer.io/api/v2`，API 金鑰透過 `auth-header` 標頭傳入。查詢採非同步任務機制：

1. 呼叫 `POST` 建立任務（如關鍵字搜尋、指定貼文留言、帳號時間軸），取得任務 `id`。
2. 以 `GET` 查詢該任務狀態，直到狀態不再是 `INIT` 或 `RUNNING`。
3. 當狀態為 `DONE` 時，同一回應即會回傳資料（`data`、`total_count`），並可透過 `page` 與 `pageSize` 控制分頁。

```bash
curl -X POST https://api.infominer.io/api/v2/xhs/search/task \
  -H "auth-header: $LARGITDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "护肤日常", "start_date": "2026-06-01", "end_date": "2026-06-30", "max_pages": 3}'

curl "https://api.infominer.io/api/v2/xhs/search/task/$TASK_ID?page=1&pageSize=100" \
  -H "auth-header: $LARGITDATA_API_KEY"
```

任務完成後，小紅書筆記搜尋的 JSON 回應範例如下：

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

本 API 也可以在 Apify 上執行：[apify.com/largitdata/social-media-api](https://apify.com/largitdata/social-media-api)。填入您的 API 金鑰即可使用，結果將存為 Apify dataset，支援匯出 CSV、Excel 或 JSON 格式。

### Python Client 套件

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

## 各平台 API 端點文件

各端點文件均包含請求參數、回應欄位、curl 與 Python 範例及回傳範例。

- **微博**：[關鍵字搜尋](https://www.largitdata.com/開發者中心/社群媒體API/weibo/keyword-search/) · [留言](https://www.largitdata.com/開發者中心/社群媒體API/weibo/comments/) · [轉發與轉發鏈](https://www.largitdata.com/開發者中心/社群媒體API/weibo/reposts/) · [帳號時間軸](https://www.largitdata.com/開發者中心/社群媒體API/weibo/user-timeline/) · [英文翻譯資料](https://www.largitdata.com/開發者中心/社群媒體API/weibo/english-translation/)
- **小紅書（RedNote）**：[筆記搜尋](https://www.largitdata.com/開發者中心/社群媒體API/xiaohongshu/keyword-search/) · [留言與回覆](https://www.largitdata.com/開發者中心/社群媒體API/xiaohongshu/comments/) · [帳號時間軸](https://www.largitdata.com/開發者中心/社群媒體API/xiaohongshu/user-timeline/)
- **抖音**：[影片搜尋](https://www.largitdata.com/開發者中心/社群媒體API/douyin/keyword-search/) · [留言](https://www.largitdata.com/開發者中心/社群媒體API/douyin/comments/) · [帳號時間軸](https://www.largitdata.com/開發者中心/社群媒體API/douyin/user-timeline/)
- **Threads**：[關鍵字搜尋](https://www.largitdata.com/開發者中心/社群媒體API/threads/keyword-search/) · [回覆](https://www.largitdata.com/開發者中心/社群媒體API/threads/replies/) · [帳號時間軸](https://www.largitdata.com/開發者中心/社群媒體API/threads/user-timeline/) · [貼文互動](https://www.largitdata.com/開發者中心/社群媒體API/threads/reactions/)
- **嗶哩嗶哩**：[影片搜尋](https://www.largitdata.com/開發者中心/社群媒體API/bilibili/keyword-search/) · [留言](https://www.largitdata.com/開發者中心/社群媒體API/bilibili/comments/)
- **知乎**：[關鍵字搜尋](https://www.largitdata.com/開發者中心/社群媒體API/zhihu/keyword-search/) · [回答與留言](https://www.largitdata.com/開發者中心/社群媒體API/zhihu/answers-and-comments/)
- **百度貼吧**：[貼文搜尋](https://www.largitdata.com/開發者中心/社群媒體API/tieba/keyword-search/) · [樓層與回覆](https://www.largitdata.com/開發者中心/社群媒體API/tieba/replies/)

完整 OpenAPI 線上文件：https://api.infominer.io/docs

## 常見問題（FAQ）

**可以用 API 以 JSON 格式取得小紅書（RedNote）筆記留言嗎？**
可以。傳入筆記網址並呼叫 `POST /xhs/pushs/task` 即可取得留言（可選擇包含第二層回覆）；若要以關鍵字搜尋筆記，請呼叫 `POST /xhs/search/task`。

**不懂中文也能透過 API 取得微博英文翻譯嗎？**
可以。訂閱英文關鍵字後，系統會轉成中文搜尋詞，回補近 30 天符合的貼文並附英文機器翻譯；不在訂閱範圍內的貼文則不提供即時翻譯。

**抖音（Douyin）和 TikTok 一樣嗎？**
不一樣。抖音是中國大陸使用的 App，與 TikTok 內容各自獨立。本 API 涵蓋抖音，不包含 TikTok。

**歷史資料可以回溯多久？更新頻率為何？**
歷史資料回溯範圍、資料量與更新頻率，將於申請試用時依專案需求確認。

**可以不自行串接 API，改由大數軟體直接交付資料嗎？**
可以。大數軟體可代為監測關鍵字與帳號、清理並翻譯資料、回補歷史資料，再直接交付至您的系統。

## 關於大數軟體（LargitData）

[大數軟體有限公司](https://www.largitdata.com/)（LargitData）位於台北，開發 InfoMiner、RAGi 與數據 API。如有疑問，請透過[試用申請表](https://www.largitdata.com/社群媒體API/#api-inquiry)與我們聯絡。

本儲存庫的範例程式採 MIT 授權釋出。API 本身的使用依您與大數軟體的合約。
