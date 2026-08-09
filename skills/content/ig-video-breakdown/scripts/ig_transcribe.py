#!/usr/bin/env python3
"""IG reel / 本地影片 → 逐字稿 (txt + srt)。跨平台（macOS / Windows / Linux）。

在 Hermes 與 Claude Code 下皆可直接執行。只依賴既有 CLI：yt-dlp、ffmpeg、whisper
（或 faster-whisper 套件），不需安裝額外東西。

用法:
    python ig_transcribe.py <IG_URL|影片檔路徑> [--outdir DIR] [--model turbo] [--lang zh] [--cookies-browser chrome]

範例:
    python ig_transcribe.py "https://www.instagram.com/reel/XXXX/" --lang zh
    python ig_transcribe.py "https://www.instagram.com/reel/XXXX/" --cookies-browser safari
    python ig_transcribe.py ./video.mp4 --model base --lang en --outdir ./out

輸出 (在 outdir 下):
    audio.wav          抽好的 16kHz 單聲道音訊
    audio.txt/srt/json/tsv/vtt  Whisper CLI 產出的逐字稿與時間軸（依輸入檔 stem 命名）
    transcript.txt/srt  faster-whisper fallback 產出的逐字稿與時間軸
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], step: str) -> None:
    print(f"[ig_transcribe] {step}: {' '.join(cmd)}", flush=True)
    proc = subprocess.run(cmd)
    if proc.returncode != 0:
        raise SystemExit(f"[ig_transcribe] {step} 失敗 (exit {proc.returncode})")


def find_cli(name: str) -> str | None:
    return shutil.which(name)


def download_video(url: str, outdir: Path, cookies_browser: str | None) -> Path:
    if not find_cli("yt-dlp"):
        raise SystemExit("找不到 yt-dlp。請安裝: macOS `brew install yt-dlp` / Windows `winget install yt-dlp`")
    cmd = ["yt-dlp", "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
           "--restrict-filenames", "-o", str(outdir / "%(id)s.%(ext)s")]
    if cookies_browser:
        cmd += ["--cookies-from-browser", cookies_browser]
    cmd.append(url)
    run(cmd, "下載影片")
    vids = list(outdir.glob("*.mp4"))
    if not vids:
        vids = list(outdir.glob("*.mkv")) + list(outdir.glob("*.webm"))
    if not vids:
        raise SystemExit("下載完成但找不到影片檔（可能 IG 防爬，試 --cookies-browser 或改用 Apify fallback）")
    return vids[0]


def extract_audio(video: Path, outdir: Path) -> Path:
    if not find_cli("ffmpeg"):
        raise SystemExit("找不到 ffmpeg。請安裝: macOS `brew install ffmpeg` / Windows `winget install ffmpeg`")
    wav = outdir / "audio.wav"
    run(["ffmpeg", "-y", "-i", str(video), "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", str(wav)],
        "抽出音訊")
    return wav


def transcribe(audio: Path, outdir: Path, model: str, lang: str) -> tuple[Path, Path]:
    cli = find_cli("whisper")
    if cli:
        cmd = [cli, str(audio), "--model", model, "--output_format", "all",
               "--output_dir", str(outdir), "--verbose", "False"]
        if lang:
            cmd += ["--language", lang]
        run(cmd, "Whisper 轉寫")
        return audio.with_suffix(".txt"), audio.with_suffix(".srt")
    # fallback: faster-whisper 套件（無 CLI 時）
    try:
        from faster_whisper import WhisperModel
        import os
        wmodel = WhisperModel(model, device="cpu", compute_type="int8")
        segments, _ = wmodel.transcribe(str(audio), language=lang or None, beam_size=5)
        txt_lines, srt_lines = [], []
        for i, seg in enumerate(segments, 1):
            start, end, text = seg.start, seg.end, seg.text.strip()
            txt_lines.append(text)
            srt_lines.append(f"{i}\n{fmt_ts(start)} --> {fmt_ts(end)}\n{text}\n")
        (outdir / "transcript.txt").write_text("\n".join(txt_lines), encoding="utf-8")
        (outdir / "transcript.srt").write_text("\n".join(srt_lines), encoding="utf-8")
        print(f"[ig_transcribe] faster-whisper 完成: {outdir}")
        return outdir / "transcript.txt", outdir / "transcript.srt"
    except ImportError:
        raise SystemExit("找不到 whisper CLI 或 faster-whisper。請安裝: pip install -U openai-whisper")


def fmt_ts(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h, rem = divmod(ms, 3600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main() -> None:
    ap = argparse.ArgumentParser(description="IG/本地影片 → 逐字稿 (跨平台)")
    ap.add_argument("input", help="IG URL 或本地影片檔路徑")
    ap.add_argument("--outdir", default="ig_tmp", help="輸出目錄（預設 ig_tmp）")
    ap.add_argument("--model", default="turbo", help="Whisper 模型（CPU 建議 base）")
    ap.add_argument("--lang", default="", help="語言代碼，如 zh / en（留空自動偵測）")
    ap.add_argument("--cookies-browser", default="", help="yt-dlp cookies 來源，如 safari / chrome / edge")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    inp = args.input
    if inp.startswith("http"):
        video = download_video(inp, outdir, args.cookies_browser or None)
    else:
        video = Path(inp)
        if not video.exists():
            raise SystemExit(f"找不到本地檔: {video}")

    audio = extract_audio(video, outdir)
    txt_path, srt_path = transcribe(audio, outdir, args.model, args.lang)
    print(f"\n完成。逐字稿: {txt_path}  /  SRT: {srt_path}")


if __name__ == "__main__":
    main()
