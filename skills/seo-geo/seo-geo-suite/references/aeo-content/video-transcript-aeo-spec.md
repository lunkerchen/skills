---
name: video-transcript-aeo
description: 影音/Podcast逐字稿轉 AEO 高引用問答與 FAQ Schema。
version: 1.0.0
author: community
license: MIT
read_when:
  - User has video transcripts, YouTube scripts, or Podcast transcripts (Whisper/SRT) to convert to AEO/GEO content
  - Converting spoken content into high-citability QA pairs, FAQPage Schema, or Speakable markup
  - Optimizing YouTube description chapters and web transcripts for AI search engines (AIO, ChatGPT, Perplexity)
  - Transforming podcast audio notes into structured web articles with 40-60 character top conclusions
metadata:
  hermes:
    tags: [seo, geo, aeo, podcast, youtube, transcript, schema, speakable]
---

# Video & Podcast Transcript to AEO Asset（影音逐字稿轉 AEO 資產）

## When to Use

當你擁有 YouTube 影片逐字稿、Podcast（如《重新構圖Reframe》）訪談錄音轉錄文字（Whisper/SRT），需要將其沉澱為能被 Google AIO、Perplexity、ChatGPT 高頻引用的結構化問答與網頁內容時載入此 Skill。

> **數據背景**：Ahrefs 75K 品牌研究指出，**YouTube 逐字稿與 AI 搜尋可見度的相關性高達 ~0.737（全網最強）**。將語音內容文字化並賦予結構，是建立「第三方共識」與「領域權威」的最佳槓桿。

---

## 4 步轉換管線

```
[原始 Whisper 逐字稿 / SRT]
           │
           ▼
[步驟 1：核心意圖切塊] ── 提煉 3-5 組獨立問答（How-to / Vs / 定義 / 實戰建議）
           │
           ▼
[步驟 2：AEO 語言重構] ── 40-60 字結論置頂 + 150-250 字自洽段落 + 消除口語代名詞
           │
           ▼
[步驟 3：結構化 Schema 注入] ── 生成 FAQPage + Speakable + VideoObject/PodcastEpisode JSON-LD
           │
           ▼
[步驟 4：雙向分發格式] ── 產出 (A) YouTube 說明欄章節 + (B) 官網/方格子發布 Markdown
```

---

## 步驟 1：意圖切塊與問答抽取

將口語漫談依據高引用結構分類為 3–5 個區塊：
- **概念定義型**：「什麼是 [X]？為什麼重要？」
- **教學步驟型（How-to）**：「如何從 0 開始 [執行 Y]？」
- **對比評測型（Vs）**：「[方案 A] 與 [方案 B] 的核心差別與適用場景？」
- **實戰避坑型**：「[主題 Z] 常見的三個致命錯誤與解法？」

---

## 步驟 2：AEO 語意改寫規範

1. **結論置頂（Answer-First）**：
   - 每個問題下方第一句話（40–60 字 / 英文 1–2 句）直接給出清晰定義或核心結論。
2. **段落自洽（Self-Contained Passage）**：
   - 段落長度維持 150–250 繁中字。
   - 將口語中的「我們剛剛講的那個」、「它的話」替換為精準實體名（如「街拍攝影的焦段選擇」）。
3. **時間戳錨定**：
   - 標註音訊對應時間（如 `[04:15 - 06:30]`），增加真實信號。

---

## 步驟 3：結構化標記模板（FAQPage + Speakable）

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "AudioObject",
      "name": "單集標題",
      "description": "單集核心摘要",
      "contentUrl": "https://example.com/audio/episode-01.mp3",
      "uploadDate": "2026-08-21"
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "街拍攝影新手如何克服對陌生人拍攝的恐懼？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "克服街拍恐懼的核心在於「預先構圖與等待主體走入」而非主動逼近。透過定焦 35mm 鏡頭、將相機掛於胸前盲拍，並在公共空間尋找光影交界處守株待兔，能有效降低被攝者的防備心理。"
          }
        }
      ]
    },
    {
      "@type": "WebPage",
      "speakable": {
        "@type": "SpeakableSpecification",
        "cssSelector": [".aeo-lead-answer", ".aeo-core-takeaway"]
      }
    }
  ]
}
</script>
```

---

## 步驟 4：交付產物格式

每次轉換必須同時輸出三種內容：
1. **Markdown 網頁版**：包含 H2 問答、前言 40-60 字加粗導言、表格對比、時間戳記。
2. **JSON-LD 程式碼**：可直接貼入網頁 `<head>` 或 Astro 元件。
3. **YouTube / Podcast 說明欄文本**：帶有秒數章節（Timestamps）與 3 點高資訊增益 Key Takeaways。
