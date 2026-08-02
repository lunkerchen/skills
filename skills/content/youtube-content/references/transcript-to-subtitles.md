# Transcript → Subtitles Pipeline

Convert any YouTube transcript into translated SRT subtitles, ready for YouTube upload.

## Pipeline Overview

```
1. Fetch transcript (JSON with segments)
2. Parse segments → merge short ones into subtitle chunks
3. Translate each chunk (delegate_task for batching)
4. Generate SRT file
5. Upload video + attach SRT captions
```

## Step 1: Fetch Transcript

```bash
# JSON output now includes "segments" array with {text, start, duration} per segment
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" > /tmp/transcript.json
```

Each segment: `{"text": "...", "start": 0.0, "duration": 2.5}`

## Step 2: Merge into Subtitle Chunks

Raw segments from youtube-transcript-api are often 2-3 seconds each — too many for readable subtitles. Merge them into chunks of **4-10 seconds** and **max 2-3 lines** per subtitle.

Heuristic (Python):

```python
merged = []
chunk = None

for seg in segments:
    s = {"start": seg["start"], "end": seg["start"] + seg["duration"], "text": seg["text"]}
    
    if chunk is None:
        chunk = {"start": s["start"], "end": s["end"], "texts": [s["text"]]}
    else:
        duration = s["end"] - chunk["start"]
        texts = chunk["texts"] + [s["text"]]
        full_text = " ".join(texts)
        
        if duration <= 10 and len(full_text) < 120 and len(texts) <= 4:
            chunk["end"] = s["end"]
            chunk["texts"] = texts
        else:
            # Finalize current chunk
            merged.append({
                "start": chunk["start"],
                "end": chunk["end"],
                "text": " ".join(chunk["texts"])
            })
            chunk = {"start": s["start"], "end": s["end"], "texts": [s["text"]]}

if chunk:
    merged.append({"start": chunk["start"], "end": chunk["end"], "text": " ".join(chunk["texts"])})
```

**Target:** ~80-150 chunks for a 15-20 min video. Adjust `duration <= 10` ceiling as needed (shorter for fast talking, longer for slow).

## Step 3: Translation

Use `delegate_task` to batch-translate all chunks. Pass the merged JSON array to a sub-agent with clear tone/locale instructions.

**Important translation notes for this user:**
- Target: Traditional Chinese (zh-Hant), not Simplified
- Preserve profanity level in Chinese (他媽的/幹 for fuck, 娘們 for broads, etc.)
- Keep proper names (driver names, team names) in original English
- Preserve censor markers like `[__]`
- Keep `>>` markers for quoted/secondary speakers
- Recurring spam memes (e.g. "Women in the workplace") → consistent short Chinese (e.g. "女人就該上班")

## Step 4: Generate SRT

```python
def to_srt_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

srt_lines = []
for i, chunk in enumerate(segments, 1):
    srt_lines.append(str(i))
    srt_lines.append(f"{to_srt_time(chunk['start'])} --> {to_srt_time(chunk['end'])}")
    srt_lines.append(chunk["zh"])
    srt_lines.append("")

with open("subtitles.srt", "w") as f:
    f.write("\n".join(srt_lines))
```

## Step 5: Upload with Captions

See `youtube-caption-upload` skill for SRT attachment. Key points:
- Upload video first (unlisted for review per user preference)
- Attach SRT via `youtube.captions().insert()` with `sync=True`
- Language code: `zh-Hant` for Traditional Chinese
- Use `MediaFileUpload` from official library — raw multipart always fails with 400

## Pitfalls

- **fetch_transcript.py pre-v1.1** (before skill patch): JSON output did NOT include raw `segments` array. You had to parse `timestamped_text` line by line (each line starts with `MM:SS` prefix). Update the skill if you see this.
- **Segment density**: A 17-min video can have 400+ raw segments. Always merge before translating — 144 chunks (vs 421 segments) is manageable for delegate_task translation.
- **SRT timing**: Use `start` and `start + duration` from raw segments. For merged chunks, the end is the last segment's `start + duration`.
- **Delegated translation**: Pass the full merged array (~150 items, ~38KB JSON) as context. The sub-agent needs the tone/domain instructions explicitly.

## Entry Point: Existing SRT → Bilingual SRT

Use this path when you already have an English SRT file (from Whisper, downloaded subs, etc.) and want to produce a bilingual SRT with English + Traditional Chinese in the same file.

### Pipeline

```
Existing SRT → Parse segments → Batch translate → Rebuild bilingual SRT
```

### 1. Parse the SRT

SRT format is blocks of `index` / `timecode` / `text` separated by blank lines:

```python
import re

with open("input.srt") as f:
    content = f.read()

blocks = content.strip().split('\n\n')
segments = []
for block in blocks:
    lines = block.strip().split('\n')
    if len(lines) >= 3:
        idx = lines[0].strip()
        timecode = lines[1].strip()
        text = ' '.join(lines[2:])
        segments.append((idx, timecode, text))
```

### 2. Batch Translate

Collect all English text (one per segment line), then translate in batches. For 400+ segments, batch into groups of ~50:

```python
# Write batches for translation
batch_size = 50
batches = [segments[i:i+batch_size] for i in range(0, len(segments), batch_size)]

for b_idx, batch in enumerate(batches):
    with open(f'/tmp/sub_batch_{b_idx}.txt', 'w') as f:
        for i, (idx, tc, text) in enumerate(batch):
            f.write(f'{b_idx*batch_size + i}|{text}\n')
```

Translate each batch (ask model or use delegate_task). Expect each batch to produce translations preserving the line numbering.

### 3. Rebuild Bilingual SRT

Each segment gets **two text lines**: original English + Chinese translation immediately below:

```python
output = []
for idx, timecode, text in segments:
    seg_num = int(idx) - 1  # 0-based
    cn = translation_dict[seg_num]
    output.append(str(idx))
    output.append(timecode)
    output.append(text)     # English
    output.append(cn)       # Chinese below
    output.append("")       # blank line separator

with open("output_bilingual.srt", "w") as f:
    f.write("\n".join(output))
```

### When to use this path vs the merge-then-translate path

| Situation | Use |
|-----------|-----|
| Transcript from youtube-transcript-api (JSON segments) | Standard pipeline: merge → translate → generate SRT |
| Already have an SRT (Whisper, downloaded, provided by user) | Bilingual path: parse SRT → translate → rebuild bilingual |
| Need only target-language subtitles | Standard pipeline (generate monolingual SRT) |
| Need English + Chinese side-by-side subtitles | Bilingual path |

### Notes

- Whisper output SRT segments are already at reasonable duration (usually 3-8s each) — no merging needed.
- For long videos (>300 segments), batch the translation to avoid context overflow.
- File naming convention: `input_bilingual.srt` to distinguish from the original monolingual file.
