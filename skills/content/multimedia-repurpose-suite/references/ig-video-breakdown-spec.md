---
name: ig-video-breakdown
description: 把 IG 影片（reel/post）轉逐字稿並拆解影片腳本。當使用者說「IG 影片轉逐字稿」「拆解這支 IG 影片」「分析這支 reel 的腳本/結構」時使用。流程：下載 → Whisper 轉寫 → 結構化拆解（hook/段落/鏡頭/節奏/CTA）→ 可複製的腳本公式。
---

# IG 影片轉逐字稿 + 腳本拆解

## 觸發條件

- 「把這支 IG 影片轉逐字稿」+ URL
- 「拆解這支 reel」「分析他影片的腳本結構」
- 使用者給 IG reels/posts 連結或本地影片檔，要求逐字稿、腳本、結構分析

## 流程總覽

1. **取得影片**（URL 或本地檔）
2. **抽音訊 → 轉寫** → 逐字稿（SRT + 純文字）
3. **拆解腳本**（結構化輸出）
4. **產出報告**（`ig_breakdown_<短碼>.md`）

**一鍵跑 1+2**（跨平台，Windows/macOS/Linux、Hermes/Claude Code 通用）：

```bash
python scripts/ig_transcribe.py "<IG_URL|影片檔>" --lang zh
# 403 時加 --cookies-browser safari（或 chrome / edge）
```

Windows 安裝與 Claude Code 安裝方式 → 見 `references/platforms.md`。

## Step 1: 取得影片

### 輸入是本地檔
直接跳 Step 2。

### 輸入是 IG URL
優先 yt-dlp（公開 reel 大多可直接抓）：

```bash
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best" --restrict-filenames \
  -o "ig_tmp/%(id)s.%(ext)s" "<IG_URL>"
```

- 403 / login wall → 加 cookies：`--cookies-from-browser safari`（或 `chrome`）
- 仍失敗 → Apify fallback（需 `APIFY_TOKEN`，見 `apify-scrapers` skill）：
  - `python <apify-scrapers>/scripts/scrape_instagram.py reels <username> --max-reels 20`
  - 從輸出 JSON 的 `video_url` 抓目標 reel（用短碼比對），再下載該 URL
- 單支 reel URL 拿不到 → 換抓該 username 的 reels 清單再挑

### 輸入是 IG username（分析整個帳號的影片）
Apify reels mode → 逐支處理（使用者通常只要一支，先問清楚）。

## Step 2: 轉寫

先確認音訊真的有人聲（IG 很多純 BGM reel）：

```bash
ffprobe -v error -show_entries stream=codec_name -select_streams a -of csv=p=0 "<影片檔>"
ffmpeg -i "<影片檔>" -t 10 -vn -acodec pcm_s16le -ar 16000 -ac 1 /tmp/ig_check.wav -y
```

- 音軌不存在或 10 秒樣本聽起來只有音樂 → 回報「此 reel 無口白，無法轉逐字稿」，不要硬轉（Whisper 對純 BGM 會胡謅）
- 有人聲 → 正式轉寫：

```bash
ffmpeg -y -i "<影片檔>" -vn -acodec pcm_s16le -ar 16000 -ac 1 ig_tmp/audio.wav

# 本機已裝 openai-whisper（CLI: whisper）。短影片用 turbo；CPU 用 base 並指定語言
whisper ig_tmp/audio.wav --model turbo --language zh \
  --output_format srt txt --output_dir ig_tmp/ --verbose False
```

- 中英混雜 → 先 `--language zh` 跑，英文段落後處理時補
- 純英文 → `--language en`
- faster-whisper 1.2.1 也可用（`WhisperModel("turbo", device="cpu", compute_type="int8")`，比 openai-whisper CPU 快）
- 中文 homophone 錯字多（tiny/base）→ 用 whisper skill 的 Stage 2 LLM 修正，或直接升 turbo/large

## Step 3: 腳本拆解（核心輸出）

拿到逐字稿後，拆成以下結構（依影片類型選用，不要硬套；資料缺就標「未取得」，不要臆測）：

### 3.1 基本盤
帳號/作者、發布日期（如有）、影片類型（口播/剪輯/教學/帶貨/劇情/紀錄）、長度、語言、表現數據（讚/留言/觀看 — 僅在有抓取或使用者提供時寫）

### 3.2 時間線拆解（beat table）

| 時間 | 時長 | 口白 | 畫面/鏡頭 | 螢幕文字 | 作用 |
|---|---|---|---|---|---|

逐段拆，標出 hook 的位置。畫面/鏡頭若只有逐字稿可看，標「無法從逐字稿判定」或請使用者看影片補。

### 3.3 結構分析
- **Hook（前 3 秒）**：類型（提問/衝突/結果先行/畫面衝擊/對比）、為什麼抓人
- **節奏**：平均鏡頭長度、剪輯密度、轉場風格
- **資訊密度**：每秒承載多少訊息、有無空窗
- **情緒弧線**：起 → 伏 → 轉 → 收
- **CTA**：有沒有、在第幾秒、形式（追蹤/留言/分享/連結/收藏）
- **可複製公式**：壓成一句「hook 類型 + 結構順序 + CTA」模板，例如 `衝突提問 hook → 3 個反轉段落 → 乾貨總結 → 留言互動 CTA`

### 3.4 產出格式
寫成 `ig_breakdown_<短碼>.md`：

```markdown
# IG 影片拆解 — <短碼或標題>
## 逐字稿（純文字）
## 逐字稿（SRT）
## 腳本拆解
### 基本盤
### beat table
### 結構分析
### 可複製公式
```

## Pitfalls

- **IG 防爬**：yt-dlp 裸抓偶爾 403 → 先 cookies → 再 Apify（花錢，`~$0.003-0.008/reel`）
- **純 BGM reel**：Whisper 會把音樂聽成「Zither Harp」之類亂碼 — 先 ffprobe/試聽，無口白直接回報
- **背景音樂蓋過人聲**：轉寫品質差是預期內，試 `--language` 或接受較差結果，不要假裝精準
- **字幕與口白不一致**：IG 常螢幕字卡 ≠ 口白，拆解以口白為主、字卡註記為輔
- **短影片（<15s）**：常常沒有完整結構 — 說「無 CTA」「無完整情緒弧線」，不要硬湊五段式
- **不要臆測數據**：讚/留言/觀看沒抓到就標「未取得」
- **轉寫腳本**：優先使用 `whisper` CLI 或 `faster-whisper`；若某個本機 wrapper 或舊流程失效，回到這兩條支援路徑，不要假裝轉寫成功

## 依賴

- `yt-dlp`、`ffmpeg`（macOS 已裝；Windows/其他平台安裝法見 `references/platforms.md`）
- `openai-whisper`（CLI: `whisper`）或 `faster-whisper`
- `APIFY_TOKEN`（fallback 下載用，非必須）
