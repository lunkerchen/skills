# 跨平台使用：Windows 與 Claude Code

本技能在 Hermes（macOS）與 Claude Code（macOS / Windows / Linux）下皆可使用。
核心管線不依賴任何平台專屬功能：yt-dlp + ffmpeg + Whisper 三大 CLI 在所有平台都有。

## 快速一鍵

不管哪個平台，裝好依賴後就是同一條指令：

```bash
python ig_transcribe.py "<IG_URL>" --lang zh
```

- 403 / 登入牆 → 加 `--cookies-browser chrome`（或 edge / safari / firefox）
- 逐字稿完成後，讓 agent 依 SKILL.md 的 Step 3 拆解腳本（LLM 分析，跨平台相同）

## Claude Code 安裝技能

Claude Code 的技能放 `.claude/skills/`（專案級）或 `~/.claude/skills/`（個人級，全專案可用）。

```bash
# 個人級（推薦，所有專案可用）
mkdir -p ~/.claude/skills/ig-video-breakdown
cp -r skills/ig-video-breakdown/* ~/.claude/skills/ig-video-breakdown/
```

或直接從此 repo 複製（Windows PowerShell）：

```powershell
New-Item -ItemType Directory -Force $HOME\.claude\skills\ig-video-breakdown | Out-Null
Copy-Item -Recurse skills\ig-video-breakdown\* $HOME\.claude\skills\ig-video-breakdown\
```

專案級則是放 `./.claude/skills/ig-video-breakdown/`，只對該專案生效。
安裝後 Claude Code 看到「IG 影片轉逐字稿」等觸發詞即自動載入。

## Windows 安裝依賴

PowerShell（系統管理員）或普通權限皆可：

```powershell
# yt-dlp + ffmpeg
winget install yt-dlp.yt-dlp
winget install Gyan.FFmpeg

# Whisper（Python 3.8–3.11；裝完即有 whisper CLI）
python -m pip install -U openai-whisper

# 或更快（CPU int8、不需 CLI）： 
python -m pip install -U faster-whisper
```

- 沒有 winget 時：yt-dlp 抓 https://github.com/yt-dlp/yt-dlp/releases 的 .exe 放進 PATH；
  ffmpeg 抓 https://www.gyan.dev/ffmpeg/builds/ 的 essentials zip 解壓後加 PATH。
- cookies：Windows 上的 Chrome/Edge 直接 `--cookies-from-browser chrome`（或 `edge`）。

## macOS（Hermes 用）安裝依賴

```bash
brew install yt-dlp ffmpeg
python3 -m pip install -U openai-whisper   # 或 faster-whisper
```

## 手動指令對照（不跑 script 時）

| 步驟 | macOS / Linux (bash) | Windows (PowerShell) |
|---|---|---|
| 下載 | `yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best" -o "ig_tmp/%(id)s.%(ext)s" "<URL>"` | 同左（yt-dlp 指令跨 shell 相同） |
| 抽音訊 | `ffmpeg -y -i "<影片>" -vn -acodec pcm_s16le -ar 16000 -ac 1 ig_tmp/audio.wav` | 同左 |
| 轉寫 | `whisper ig_tmp/audio.wav --model turbo --language zh --output_format txt srt --output_dir ig_tmp/` | 同左（PowerShell 下引號內路徑用 `$HOME\ig_tmp\...` 或絕對路徑） |

yt-dlp / ffmpeg / whisper 都是跨平台 CLI，指令本體一致；只有「輸出目錄寫法」與「cookies browser 名稱」可能因平台不同。

## 效能注意（Windows / 無 Apple Silicon 時）

- `turbo` 在純 CPU 上很慢；短 reel（<60s）可接受，長影片建議 `--model base` + `--language zh`
- 有 NVIDIA GPU → faster-whisper 更快：
  ```python
  from faster_whisper import WhisperModel
  model = WhisperModel("turbo", device="cuda", compute_type="float16")
  ```
- 純 BGM 的 reel 仍會胡謅 — 先用 ffprobe / 試聽確認有人聲再轉（見 SKILL.md Step 2）

## Hermes vs Claude Code 差異

| | Hermes | Claude Code |
|---|---|---|
| 技能路徑 | `$HERMES_HOME/skills/` | `~/.claude/skills/`（或專案 `.claude/skills/`） |
| 觸發 | 系統自動掃 description | 同左（Claude Code 也讀 frontmatter description） |
| 執行 | agent 自己下指令 | agent 經 bash tool 下同樣指令 |
| script | `python scripts/ig_transcribe.py ...` | 同左（Claude Code 可直接跑） |

兩邊共用同一份 SKILL.md + script，無需改寫。
