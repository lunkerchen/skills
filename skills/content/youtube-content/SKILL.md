---
name: youtube-content
description: "YouTube transcripts to summaries, threads, blogs. Covers transcript extraction, content summarization, thread generation, and blog post conversion. Use when converting YouTube videos to written content, summarizing video transcripts, or extracting key points from video content."
---

# YouTube Content Tool

## When to use

Use when the user shares a YouTube URL or video link, asks to summarize a video, requests a transcript, or wants to extract and reformat content from any YouTube video. Transforms transcripts into structured content (chapters, summaries, threads, blog posts).

Extract transcripts from YouTube videos and convert them into useful formats.

## Setup

```bash
pip install youtube-transcript-api
```

## Helper Script

`SKILL_DIR` is the directory containing this SKILL.md file. The script accepts any standard YouTube URL format, short links (youtu.be), shorts, embeds, live links, or a raw 11-character video ID.

```bash
# JSON output with metadata
python3 SKILL_DIR/scripts/fetch_transcript.py "https://youtube.com/watch?v=VIDEO_ID"

# Plain text (good for piping into further processing)
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --text-only

# With timestamps
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --timestamps

# Specific language with fallback chain
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --language tr,en
```

## Output Formats

After fetching the transcript, format it based on what the user asks for:

- **Chapters**: Group by topic shifts, output timestamped chapter list
- **Summary**: Concise 5-10 sentence overview of the entire video
- **Chapter summaries**: Chapters with a short paragraph summary for each
- **Thread**: Twitter/X or Threads format — numbered posts, each punchy and accessible. **For this user**: avoid product names and technical jargon when the target is general audience. Lead with the human outcome ("從草圖到上線") not the tool name ("Claude Code + Cloud Run"). Use short lines, one idea per paragraph, plain language.
- **Blog post**: Full article with title, sections, and key takeaways
- **Quotes**: Notable quotes with timestamps
- **Subtitles (SRT)**: Translated subtitles for bilingual YouTube upload. See `references/transcript-to-subtitles.md` for the full pipeline — segment merging, translation via delegate_task, SRT generation, and caption attachment.

- **Narrative timeline**: Scene-by-scene breakdown with emotional beats, turning points, and dramatic arcs — not just topic shifts but narrative function (setup, tension, climax, reflection). Each entry includes start time, a scene label, and a one-line summary of its narrative role. Best for analyzing vlogs, competition recaps, sports rounds, and story-driven content.

### Example — Chapters Output

```
00:00 Introduction — host opens with the problem statement
03:45 Background — prior work and why existing solutions fall short
12:20 Core method — walkthrough of the proposed approach
24:10 Results — benchmark comparisons and key takeaways
31:55 Q&A — audience questions on scalability and next steps
```

## Workflow

1. **Fetch** the transcript using the helper script with `--text-only --timestamps`.
2. **Validate**: confirm the output is non-empty and in the expected language. If empty, retry without `--language` to get any available transcript. If still empty, try the yt-dlp subtitle fallback (see below). If that also yields nothing, use the Whisper ASR final fallback — download the audio track and transcribe locally. Do NOT tell the user "transcripts disabled" without first exhausting both fallback paths.
3. **Chunk if needed**: if the transcript exceeds ~50K characters, split into overlapping chunks (~40K with 2K overlap) and summarize each chunk before merging.
4. **Transform** into the requested output format. If the user did not specify a format, default to a summary.
5. **Verify**: re-read the transformed output to check for coherence, correct timestamps, and completeness before presenting.

### Post-Transcript Pipeline

After fetching and verifying, the user may ask for downstream processing. Common pipeline steps:

1. **Translate** → If the user asks for translation in a specific language, first try `--translate <code>` on the fetch script. If that returns HTTP 429 (YouTube rate limit), the fallback is to read the cached `transcript.md` from the output directory and translate it directly using the agent's own capabilities — do NOT rely on retrying the YouTube API. For Traditional Chinese use `zh-Hant`.
2. **Export to notes** → If the user asks to save to notes (e.g. "輸出到筆記"), write to their Obsidian vault. For this user, the target is `$OBSIDIAN_VAULT/05-HERMES-OUTPUTS/`. Maintain the YAML frontmatter with source URL, channel, date, and tag the note appropriately.
3. **Summarize** → After translation, if asked for key points, produce a concise bullet-point summary in the same language as the transcript. Lead with actionable advice; group related concepts; skip filler.

### Pro Workflow: yt-dlp Multi-Format Extraction (Fallback)

When `youtube-transcript-api` fails but the video has visible auto-generated subtitles, use `yt-dlp` directly. YouTube now requires JS challenge solving for subtitle downloads — always include `--remote-components ejs:github`:

```bash
yt-dlp --remote-components ejs:github --write-subs --write-auto-subs \\
  --sub-langs "zh,zh-TW,zh-HK,zh-CN,zh-Hans,zh-Hant,en,ja,ko" \\
  --skip-download --sub-format "vtt/srt" \\
  --sleep-interval 2 \\
  --output "%(id)s.%(ext)s" "<URL>"
```

**Prerequisites:** `pip install yt-dlp-ejs` and `brew install deno`.

**Language code pitfall:** Chinese auto-captions use exact codes like `zh-TW`, `zh-Hans`. The generic `zh` silently finds nothing. Always check with `--list-subs` first:
```bash
yt-dlp --list-subs URL | grep -E "^[a-z]"   # discover exact codes
```

Then search for `.vtt`, `.srt`, or `.json` files and parse accordingly:
- **VTT**: Strip `WEBVTT` header, timestamps (`-->`), and HTML tags; deduplicate consecutive lines.
- **SRT**: Strip numeric indices and timestamps (`-->`), deduplicate.
- **JSON**: Parse YouTube's `events[].segs[].utf8` structure.

If the priority language list finds no matches, retry with `--sub-langs all`.

### Pro Workflow: Metadata Probe (Gate Before Whisper)

Before committing to the expensive Whisper ASR step, probe video metadata first to confirm language, duration, and topic:

```bash
yt-dlp --print "%(title)s\n%(channel)s\n%(duration_string)s\n%(description)s" "<URL>"
```

This tells you:
- The primary **language** (set `--language` correctly on Whisper)
- The **duration** (estimate Whisper runtime: ~1-2x real-time on GPU, ~5-10x on CPU for `small` model)
- The **topic/domain** (use as `--initial_prompt` to bias Whisper vocabulary, e.g. golf terms, programming jargon)

Only proceed to Whisper ASR if the video is in a language you can analyze.

### Pro Workflow: Whisper ASR (Final Fallback)

When both the transcript API AND yt-dlp subtitle downloads return nothing (transcripts disabled + no auto-subs), download the audio track and transcribe locally with OpenAI Whisper:

```bash
# 1. Download audio (best quality, convert to wav)
yt-dlp -f bestaudio --extract-audio --audio-format wav -o "/tmp/%(id)s.%(ext)s" "<URL>"

# 2. Transcribe with Whisper
# --language: match the video's primary language (zh, en, ja, ko, etc.)
# --model: small (good accuracy/speed balance for ~10min videos); medium/large for longer or noisy audio
# --task transcribe: keep original language
# --task translate: transcribe + translate to English (only if needed)
whisper /tmp/VIDEO_ID.wav --language zh --model small --task transcribe --output_format txt --output_dir /tmp/
```

**Background execution**: Whisper processing takes significant time (5-10x real-time on CPU). For anything over ~5min, use background terminal with `notify_on_complete` to avoid blocking:

```bash
terminal(command="whisper /tmp/VIDEO_ID.wav --language zh --model small --task transcribe --output_format txt --output_dir /tmp/", background=true, notify_on_complete=true, timeout=600)
```

Poll or wait for completion, then read the output file. The terminal stderr may display VTT-like timestamps during processing — ignore those and read the actual `.txt` file for clean text.

**Pitfalls:**
- Whisper on CPU uses FP32 (2x memory vs FP16). On 16GB machines, `small` can OOM on videos >15min. Prefer `tiny` or `base` for longer content.
- Chinese transcription quality degrades with `tiny` model — `small` or `medium` strongly preferred for accuracy-critical work.
- The wav file is typically 10-50MB for a ~10min video. Clean it up after: `rm /tmp/VIDEO_ID.wav`
- `--output_format txt` produces clean text in the file, but terminal output during processing shows VTT-like timestamps — read the file, not the terminal output preview.
- If the audio download fails with "n challenge solving failed" warnings from yt-dlp, the audio still often downloads fine — check the output file before retrying.
- For non-Chinese videos adjust `--language` accordingly; Whisper supports 99 languages.
- Domain-specific vocabulary (golf terms, medical jargon, product names) generally survives `small` model for common languages, but if the transcript shows frequent garbled domain terms, retry with `--model medium` and an `--initial_prompt` containing known domain terms.
- **macOS SSL cert issue**: `whisper` downloads the model via `urllib` which can fail with `SSL: CERTIFICATE_VERIFY_FAILED` on macOS Python 3.11. Prefix the command with `SSL_CERT_FILE=$(python3 -m certifi)` to fix: `SSL_CERT_FILE=$(python3 -m certifi) whisper ...`
- **Persist transcripts shared across agents**: saving to `/tmp/` is fine for single-use, but if the transcript will be consumed by multiple workers (e.g. kanban task graph with parallel analysis tasks), save to a durable path like `$DEV_PROJECTS/transcript_<VIDEO_ID>.txt` and add file comments to each kanban task so workers can find it.

### Pro Workflow: High-Fidelity Thematic Restructuring

For full article conversion (deep structuring, multi-language UI, batch processing, history management, Map-Reduce chunking for long videos), use the dedicated **`youtube-to-article`** skill instead. It encodes the complete v3.2 pipeline as a FastAPI web app with:
- 9-language subtitle priority chain (`zh`, `zh-TW`, `zh-HK`, `zh-CN`, `zh-Hans`, `zh-Hant`, `en`, `ja`, `ko`)
- Google Gemini Flash LLM synthesis with thematic block restructuring
- 4-language UI, smart URL parsing, multi-tab results
- Map-Reduce chunking for videos exceeding 80K characters
- Apple Notes & Obsidian export workflows


### Pro Workflow: Video Optimization Analysis (Multi-Agent)

When the user asks for optimization suggestions on a YouTube video (not just transcript extraction), use the multi-agent kanban pipeline documented in `references/video-optimization-analysis.md`. It decomposes the work into three parallel analysis lanes (content/SEO/production) with a synthesis task that depends on all three. This is the recommended workflow for any "analyze this video and suggest improvements" request.

---

## Error Handling

- **Transcript disabled / no subtitles**: first try the yt-dlp subtitle fallback (multi-language). If that also returns nothing, use Whisper ASR (audio download + local transcription) — see the Whisper ASR fallback section above. Only after exhausting both paths should you report that the video is not transcribable.
- **Private/unavailable video**: relay the error and ask the user to verify the URL.
- **No matching language**: retry without `--language` to fetch any available transcript, then note the actual language to the user.
- **yt-dlp fallback**: if `youtube-transcript-api` returns empty or fails, try the multi-format yt-dlp workflow in the Pro Workflow section above.
- **Translate HTTP 429**: the `--translate` flag on the outer skill's CLI (baoyu-youtube-transcript's `--translate`) can return HTTP 429 under YouTube rate limiting. Do NOT retry — instead, read the cached `transcript.md` from the output directory and translate it directly using the agent's own capabilities. The cached English transcript is always available after the first successful fetch.
- **Dependency missing**: run `pip install youtube-transcript-api` and retry.
