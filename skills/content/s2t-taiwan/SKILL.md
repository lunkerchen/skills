---
name: s2t-taiwan
title: "Simplified Chinese → Traditional Chinese (Taiwan) Translation"
description: "Convert Simplified Chinese to Taiwan Traditional Chinese."
category: translation
triggers:
  - "translate to traditional Chinese"
  - "convert to Taiwan Chinese"
  - "繁體中文（台灣）"
  - "s2t"
  - "simplified to traditional"
  - "簡轉繁"
  - "tw localization"
---

# Simplified Chinese → Traditional Chinese (Taiwan) Translation

## When to Use

- User asks to convert Simplified Chinese (简体中文) to Traditional Chinese (繁體中文)
- User specifies **Taiwan** (台灣/臺灣) as the target locale — NOT Hong Kong (香港) or general Traditional
- Requirement for Taiwan-appropriate terminology (e.g. 軟體 not 軟件, 使用者 not 用戶)

## Workflow

### Step 1: Try Automated Conversion First

```python
pip install opencc-python-reimplemented

from opencc import OpenCC
# s2tw = Simplified to Traditional Taiwan (best for most cases)
converter = OpenCC('s2tw')
result = converter.convert(text)
```

If opencc is unavailable (binary incompatibility on some macOS setups), fall back to a manual character mapping (see Step 3).

### Step 2: Apply Taiwan-Specific Terminology

After character conversion, replace these Simplified Chinese terms with their Taiwan equivalents:

| Simplified | Taiwan (台灣) | Notes |
|---|---|---|
| 视频 | 影片 | video |
| 软件 | 軟體 | software |
| 服务器 | 伺服器 | server |
| 人工智能 | 人工智慧 | AI |
| 互联网 | 網路 | internet |
| 创业 | 新創 | startup |
| 项目 | 專案 | project |
| 调试 | 除錯 | debugging |
| 信息 | 資訊 | information |
| 算法 | 演算法 | algorithm |
| 屏幕 | 螢幕 | screen |
| 打印 | 列印 | print |
| 协议 | 協定 | protocol |
| 反馈 | 回饋 | feedback |
| 优化 | 最佳化 | optimize |
| 用户 | 使用者 | user |
| 质量 | 品質 | quality |
| 实时 | 即時 | real-time |
| 复盘 | 覆盤 | retrospective |
| 数据 | 數據 | keep as is (standard in Taiwan tech) |

### Step 3: Manual Character Mapping (fallback)

If no automated converter works, build a comprehensive Simplified→Traditional character map. Key conversions needed for most technical documents:

**Common character conversions:**
与→與, 个→個, 为→為, 么→麼, 从→從, 们→們, 关→關, 对→對, 会→會, 当→當, 将→將, 没→沒, 发→發, 变→變, 时→時, 来→來, 体→體, 后→後, 开→開, 进→進, 过→過, 说→說, 间→間, 长→長, 门→門, 写→寫, 吗→嗎, 听→聽, 声→聲, 处→處, 备→備, 复→復, 数→數, 点→點, 线→線, 级→級, 经→經, 这→這, 还→還, 两→兩, 层→層, 样→樣, 产→產, 业→業, 动→動, 区→區, 机→機, 权→權, 标→標, 断→斷, 来→來

⚠️ **Ambiguous simplified characters needing context:**
- `干`: 干涉→干預, 幹活→幹活, 乾燥→乾燥
- `后`: 以後→以後, 皇后→皇后
- `发`: 發現→發現, 頭髮→頭髮
- `只`: 只有→只有, 隻身→隻身

### Step 4: Taiwan Usage Quality Checks

Post-conversion, verify these Taiwan-standard forms:

**Character variants (Taiwan preference — differs from Hong Kong):**
- ✅ **裡** (not 裏) — "這裡", "圈子裡"
- ✅ **為** (not 爲) — "因為", "成為"
- ✅ **眾** (not 衆) — "聽眾", "觀眾"
- ✅ **群** (not 羣) — "社群", "群體"
- ✅ **峰** (not 峯) — "高峰", "峰值"
- ✅ **啟** (not 啓) — "啟動", "啟用"
- ✅ **干** (for "intervene") — "干預", "干涉" (NOT 幹預)
- ✅ **回流** (not 迴流) — "回流通道"
- ✅ **克制** (not 剋制) — standard form

**Number vs Digital distinction — CRITICAL:**
- 數字 = number/digit (e.g. "三個數字", "這個數字")
- 數位 = digital (e.g. "數位轉型", "數位科技")
- Do NOT blanket-replace 數字→數位; check context.

### Step 5: Preserve Formatting

- Keep markdown syntax, HTML tags, code blocks, and frontmatter untouched
- Preserve proper nouns (company names, product names, people names)
- Keep English terms and acronyms as-is unless Taiwan has an established translation

## Pitfalls

- **Blanket replacements cause errors**: "數字→數位" only in "digital" contexts
- **Variant character confusion**: Taiwan and Hong Kong use different variants (e.g. 裡 vs 裏)
- **Library import issues**: opencc may have binary compatibility on some macOS — have manual fallback ready
- **Mixed script content**: Code blocks, URLs, file paths should NOT be converted
- **"後"/"后" distinction**: "以后"(after)→"以後", "皇后"(empress)→same

## Verification

After conversion, search for remaining Simplified characters:
```python
simp_check = set('万个与从乐么习书买乱争于亏亚产亲众优会传伤价体余们关兴...')
remaining = [c for c in text if c in simp_check]
```
Also grep for commonly missed terms: 软件, 用户, 信息, 优化, 反馈, 实时

## Reference Files

See `references/character-mapping.md` for a comprehensive 300+ character mapping table and ambiguous-character decision guide.
See `references/opencc-macos-compat.md` for resolving opencc C-extension binary issues on macOS.
