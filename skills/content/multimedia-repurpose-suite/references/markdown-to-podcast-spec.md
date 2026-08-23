---
name: markdown-to-podcast
title: markdown-to-podcast
description: 'Convert markdown to podcast WAV via Edge TTS (neural) + pydub piano intro/outro.'
---

# Markdown → Podcast Pipeline

將 Markdown 文章轉成 WAV podcast 音檔。支援三層 TTS（依清晰度與自然度平衡排序）：**BlueMagpie-TTS hung_yi_lee**（台灣口音最佳平衡）→ **Edge TTS**（微軟神經網路語音，快速）→ **BlueMagpie-TTS 聲音複製**（自己的聲音，注意斷句清晰度陷阱）→ macOS `say`（備用）。鋼琴 intro/outro 使用 arpeggio v2 風格（sox 或 pydub 合成）。

## Pipeline

```bash
# 單篇文章
python3 podcast-pipeline.py vocus-drafts/2026-07-23-ai-junbei-shengwen.md

# 批次全部
for f in vocus-drafts/*.md; do python3 podcast-pipeline.py "$f"; done

# 指定語音/語速
PODCAST_TTS_VOICE=zh-TW-HsiaoChenNeural PODCAST_TTS_RATE=-20% python3 podcast-pipeline.py input.md
```

```
article.md
  │
  ├── Step 1: Intro ─────────────────────
  │   Python + pydub 合成鋼琴約 6s
  │   Arpeggio 分解和弦 + reverb（v2 style）
  │   和弦進行: Cmaj7 → G/B → Am7 → Fmaj7
  │
  ├── Step 2: TTS 朗讀 ──────────────────
  │   edge-tts → mp3 → pydub 載入
  │   語音: zh-TW-YunJheNeural（Default 男聲）
  │   env: PODCAST_TTS_VOICE, PODCAST_TTS_RATE
  │
  ├── Step 3: Outro ─────────────────────
  │   鋼琴 ~4s + Fmaj7 → Cmaj7 + fade-out + reverb
  │
  ├── Step 4: 合併 ─────────────────────
  │   intro + narration + outro → pydub concat
  │   .normalize(headroom=0.5) → .export(.wav)
  │
  └── article.wav (目標 1-2 min per article)
```

## Tools

### BlueMagpie-TTS（最高自然度 — 台灣口音 + 聲音複製）

BlueMagpie-TTS 是台灣腔優先的開源 TTS 模型，支援語者向量（speaker centroid）合成與參考音檔聲音複製（voice cloning）。**自然度高於 Edge TTS** — 適合對 AI 讀稿感敏感的場景。

- **位置**: `~/Developer/BlueMagpie-TTS/`
- **環境**: `.venv`（提供獨立 venv，使用前需 `source .venv/bin/activate`）
- **可用語者**: `hung_yi_lee`（李宏毅，預設台灣腔語者向量）
- **Python API 參數**:
  - `cfg_value=2.8` — 分類器自由導引強度
  - `inference_timesteps=9` — 生成步數（越高細節越多，越慢）
  - `max_len=3000` — 最大 token 長度
  - `retry_badcase=True` — 自動重試低品質輸出
- **輸出**: 48kHz mono WAV

#### 快速測試腳本

```bash
cd ~/Developer/BlueMagpie-TTS
source .venv/bin/activate
PYTHONPATH="" ./tts.sh "要朗讀的文字" [voice_id]
```

#### 聲音複製（Voice Cloning） — Engineer 的聲音

Engineer 的參考音檔位於 `/Users/your-user/Movies/專案/Realme 16 Pro/Audio/`（DJI 系列 WAV，5-14 秒）。使用 `reference_wav_path` 參數取代 `speaker_centroid`：

```python
from bluemagpie import BlueMagpieModel
audio = model.generate(
    target_text="要朗讀的文字",
    reference_wav_path="/Users/your-user/Movies/專案/Realme 16 Pro/Audio/DJI_27_20260401_180028.WAV",
    cfg_value=2.8,
    inference_timesteps=9,
    max_len=3000,
    retry_badcase=True,
)
```

聲音複製優先選用最近的錄音（DJI_26、DJI_27，2026/03-04），品質足夠清晰，不需預處理。

#### BlueMagpie vs Edge TTS 選擇

| 條件 | 使用 |
|------|------|
| 快速測試、短內容 | Edge TTS（~秒級生成） |
| 台灣口音自然度優先 | BlueMagpie `hung_yi_lee`（~分鐘級生成） |
| 聲音複製（自己的聲音） | BlueMagpie `reference_wav_path`（~分鐘級生成） |
| 文字有大量斷句停頓 | BlueMagpie `hung_yi_lee`（clone 版斷句易模糊 — 見下方 Pitfall）→ 或 Edge TTS |

#### Pitfalls

- BlueMagpie-TTS 生成約 **1 秒音訊需要 1 秒 GPU 推理**（MPS / Apple Silicon） — 長內容需等待 1-3 分鐘
- `.venv` 使用 `PYTHONPATH=""` 執行以避免路徑衝突
- Speaker centroid 只有 `hung_yi_lee`（若 `.pt` 檔案有更多語者，`speaker_ids` 會列出）
- Model 初次載入會從 HuggingFace 下載 ~5GB，之後以 `snapshot_download` 快取
- 出現 `FutureWarning: weight_norm deprecated` 可忽略 — 仍正常運作
- `inference_timesteps=9` 是平衡點；調高至 12-15 可改善細節但時間線性增加

### Edge TTS（快速生成用）

- **Edge TTS** — 微軟神經網路語音，比 macOS `say` 自然很多
  - 安裝: `pip install edge-tts`
  - 列出語音: `edge-tts --list-voices | grep zh-TW`
  - 繁中台灣語音（3 種）:
    - `zh-TW-HsiaoChenNeural` — 女聲，友善正向（推薦女性選項）
    - `zh-TW-HsiaoYuNeural` — 女聲，甜美
    - `zh-TW-YunJheNeural` — 男聲，友善正向（Engineer 預設試聽中）
  - 支援 rate 調整: `edge-tts --voice zh-TW-YunJheNeural --rate=-20% --text "..."`

### macOS `say`（備用 — 僅 Edge TTS 不可用時）

- `say -v Meijia -o temp.aiff "朗讀內容"`（繁中台灣腔）
- 不支援直出 WAV → 輸出 AIFF 後用 pydub 轉
- pydub 載入 AIFF 需指定 `format='aiff'`
- 可用語音: `say -v '?' | grep zh_TW`

### pydub

- 載入/合併/匯出: `AudioSegment.from_wav()`, `from_mp3()`, `from_file(..., format='aiff')`
- 串接: `intro + narration + outro`
- 標準化: `.normalize(headroom=0.5)`
- 匯出 WAV: `.export(path, format='wav')`
- 匯出 MP3: `.export(path, format='mp3', bitrate='192k')`
- 底層依賴 ffmpeg

## 鋼琴合成 v2（Arpeggio + Reverb 風格）

Session 2026-07-25 開發的改良版鋼琴，比 v1（block chords）溫暖自然。

### v1 vs v2 差異

| 特徵 | v1（舊） | v2（新 — 使用中） |
|------|----------|-----------------|
| 和弦按法 | Block chord（一次性全部壓） | Arpeggio（分解琶音） |
| 和聲進行 | C → G → Am → F | Cmaj7 → G/B → Am7 → Fmaj7 |
| 空間感 | 無 | Reverb（多重延遲混合） |
| Intro 長度 | ~5s | ~6s |
| Outro 長度 | ~3s | ~4s |
| 高頻泛音 | 偏多（電子感） | 降低（更暖） |

### 核心概念

1. **Arpeggio 琶音** — 每個和弦的音符依序彈出，非同時壓下。聽起來像真人在彈。
2. **Chord voicing 開放和聲** — 用 Cmaj7/G/B/Am7/Fmaj7 取代簡單三和弦，音域跨兩個八度，更豐富。
3. **Reverb 殘響** — 四層遞減延遲（`decay=0.25`, `delay=0.1s`）模擬房間空間感。
4. **ADSR 封包優化** — Attack 0.005s、Decay 0.15s、Sustain 0.35，更接近真鋼琴的觸鍵響應。

## 朗讀自然化技巧

### 自然停頓技巧（Text Pausing）

在輸入文字中加入結構化停頓，讓 TTS 產出更像真人朗讀：

```
原句：
三家公司指向同一個方向，AI正在從被動回應的工具轉向主動執行的智能體。

停頓版：
三家公司指向同一個方向。
AI正在從被動回應的工具，
轉向主動執行的智能體。
```

**規則**：
- 長句 → 切碎成短句（每句 10-20 字，含逗號可略長）
- 段落之間 → 留空行
- 每組邏輯概念 → 獨立一段
- 數字 + 百分比 → 保持同句

**注意**：此技巧對 BlueMagpie `hung_yi_lee` 效果顯著，但**對聲音複製（voice clone）可能導致模糊**。若使用聲音複製，建議保持文字連續，事後用 pydub 插入 silence 來控制間距。

### 語速調整

Edge TTS 即時調整：
```bash
edge-tts --voice zh-TW-YunJheNeural --rate=-15% --text "..."
```

BlueMagpie-TTS 後處理調整（因 model 不支援即時 rate）：
```bash
ffmpeg -i narration.wav -filter:a "atempo=0.85" slow.wav
```

Engineer 偏好：**85% 速度**（`atempo=0.85`）— 更從容、不趕。

## 使用者偏好（Engineer）

- **TTS（從優到劣，考量清晰度）**: **BlueMagpie-TTS hung_yi_lee（台灣口音）**（最佳平衡）≈ **Edge TTS**（快速）> **BlueMagpie-TTS 聲音複製（自己的聲音）**（自然但注意清晰度陷阱）> macOS `say`（罐頭感）
- **語音**：YunJheNeural（男聲，Edge TTS 選項）；hung_yi_lee（BlueMagpie 選項）；自己的聲音（voice clone 參考 `/Users/your-user/Movies/專案/Realme 16 Pro/Audio/`，但注意斷句陷阱）
- **語速**：慢 15%（`atempo=0.85`，ffmpeg 後處理）。Edge TTS 可用 `--rate=-15%` 近似。
- **音樂**：鋼琴 arpeggio v2 風格，intro 6s、outro 4s
- **形式**：單人朗讀（非雙人對話）
- **輸出**：每篇文章獨立 WAV（不合成一集）
- **輸入來源**：`vocus-drafts/` 下的 `.md` 檔（非原先的 briefings/）
  - 路徑：`/Users/your-user/Library/Mobile Documents/iCloud~md~obsidian/Documents/Engineer/04-HERMES-OUTPUTS/vocus-drafts/`
- **朗讀範圍**：全文（標題 + 引言 + 各節 + Q&A），跳過 YAML frontmatter
- **品質標準**：不要有 AI 讀稿感。Edge TTS 神經網路語音是底線，不夠自然就要換方案。

## Pitfalls

- Edge TTS 內建 `asyncio.run()` → 在 template 腳本中包在 `generate_tts()` 內呼叫
- `edge-tts` 輸出 MP3 → 用 `AudioSegment.from_mp3()` 載入
- pydub 載入 AIFF 需明確指定 `format='aiff'`
- 若 `edge-tts` 未安裝: `pip install edge-tts`
- 長文章（>3000 中文字）TTS 時間較長，注意腳本同步等待
- 鋼琴合成防止 clipping: 每組 arpeggio 的 peak 要 normalize 到 16-bit 範圍
- 確認 Edge TTS 版本支援繁中台灣語音（`edge-tts --list-voices | grep zh-TW`）
- **聲音複製（voice clone）清晰度陷阱**：BlueMagpie-TTS 的 `reference_wav_path` 模式在句子間有大段停頓（空白行、換行）時，產出容易模糊不清。原因是 diffusion model 對 silence 區塊的處理與內建語者向量不同。解決方案：（1）保持文字連續少停頓，事後用 pydub 插入 silence；（2）改用 `hung_yi_lee`（內建語者）搭配停頓文字，效果更清晰。
- **ffmpeg atempo 品質**：`atempo=0.85`（約慢 15%）是 Engineer 偏好的語速。注意 atempo 範圍只能 0.5-2.0，且偏離 1.0 太多會產生 artifact。如果需要大幅降速，分兩次串接：`atempo=0.85,atempo=0.85` 而非 `atempo=0.72`。

## 參考

- `templates/podcast-pipeline.py` — 完整可跑 pipeline 腳本（v2，含 Edge TTS + arpeggio piano）
- `templates/podcast-pipeline-bmt.py` — BlueMagpie-TTS 版本（支援 hung_yi_lee 內建語者 + `--clone` 聲音複製，含自動語速放慢）
- `references/sox-piano-synthesis.md` — sox 指令快速生成 v2 鋼琴 intro/outro（Python pydub 以外的替代方案）
- 環境變數:
  - `PODCAST_TTS_VOICE` — 語音名稱（default: zh-TW-YunJheNeural）
  - `PODCAST_TTS_RATE` — 語速（default: +0%）
