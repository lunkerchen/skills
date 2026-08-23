# yt-dlp JS Challenge Workaround

YouTube now requires JavaScript challenge solving for subtitle downloads (`n challenge solving failed` warning). Without this fix, `--write-auto-subs` silently produces zero files.

## Root Cause

yt-dlp needs to solve JS challenges to access YouTube's subtitle API. The built-in `deno` solver requires:
- `yt-dlp-ejs` package (`pip install yt-dlp-ejs`)
- `deno` runtime (`brew install deno` on macOS)

The solver is activated via the `--remote-components` flag.

## Working Command

```bash
yt-dlp --remote-components ejs:github \
  --write-auto-subs \
  --sub-langs "zh-TW" \
  --skip-download \
  --sub-format "vtt" \
  --sleep-interval 2 \
  --output "%(playlist_index)s-%(title)s.%(ext)s" \
  "URL"
```

## Language Code Discovery

Always check exact subtitle codes before downloading:

```bash
yt-dlp --list-subs URL | grep -E "^[a-z]"
```

Chinese auto-captions use `zh-TW` (original), not `zh`, `zh-Hans`, or `zh-Hant`. The generic `zh` finds nothing.

## Failed Alternatives

These approaches do NOT work for JS-challenged subtitle downloads:
- `youtube-transcript-api` (Python library) — returns `ParseError` or `NoTranscriptFound` for `zh-TW`
- yt-dlp without `--remote-components` — runs without error but writes zero subtitle files
- yt-dlp with `--cookies-from-browser` — bypasses login but not JS challenge

This was tested on 39 videos from a Chinese technical analysis playlist (avg 7 min each, all with auto-generated Chinese captions).
