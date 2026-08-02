#!/usr/bin/env python3
"""
Markdown → Podcast Pipeline — Full working template (v2).
Reads a markdown file, generates arpeggio piano intro/outro,
narrates via Edge TTS (neural zh-TW voices), and concatenates into a final WAV.

Usage:
    python3 podcast-pipeline.py <input.md> [output.wav]

Environment:
    PODCAST_TTS_VOICE   Edge TTS voice (default: zh-TW-YunJheNeural)
    PODCAST_TTS_RATE    Speech rate  (default: +0%)
"""

import sys, subprocess, tempfile, struct, math, wave, os, re
from pydub import AudioSegment

# ── Config ──
SAMPLE_RATE = 44100
SAMPLE_WIDTH = 2
CHANNELS = 1
INTRO_SEC = 6
OUTRO_SEC = 4
TTS_VOICE = os.environ.get('PODCAST_TTS_VOICE', 'zh-TW-YunJheNeural')
TTS_RATE = os.environ.get('PODCAST_TTS_RATE', '+0%')

# Chord voicings (v2: spread arpeggio - warmer than block triads)
CHORDS = {
    'Cmaj7':  [261.63, 329.63, 392.00, 523.25],
    'G_B':    [246.94, 392.00, 493.88, 587.33],
    'Am7':    [220.00, 392.00, 440.00, 523.25],
    'Fmaj7':  [349.23, 440.00, 523.25, 659.25],
}


def piano_tone_note(freq, duration_sec, velocity=0.8):
    """Warmer piano tone: fundamental + 2nd/3rd/4th harmonics + sub-octave + ADSR."""
    n = int(SAMPLE_RATE * duration_sec)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        val = (math.sin(2 * math.pi * freq * t) * 1.0 +
               math.sin(2 * math.pi * freq * 2 * t) * 0.25 +
               math.sin(2 * math.pi * freq * 3 * t) * 0.08 +
               math.sin(2 * math.pi * freq * 4 * t) * 0.03 +
               math.sin(2 * math.pi * freq * 0.5 * t) * 0.10)
        a, d, s = 0.005, 0.15, 0.35
        sus_end = duration_sec - 0.5
        if t < a:
            env = (t / a) * 1.2
        elif t < a + d:
            env = 1.2 - (1.2 - s) * ((t - a) / d)
        elif t < sus_end:
            env = s
        else:
            env = s * (1.0 - (t - sus_end) / 0.5)
        brightness = 0.5 + velocity * 0.5
        samples.append(int(val * env * velocity * 0.6 * brightness * 32767))
    return samples


def arpeggio(chord_name, duration_sec):
    """Broken chord: notes played sequentially for a natural piano feel."""
    freqs = CHORDS[chord_name]
    n_notes = len(freqs)
    note_dur = duration_sec / n_notes
    total = int(SAMPLE_RATE * duration_sec)
    out = [0] * total
    for idx, freq in enumerate(freqs):
        offset = int(SAMPLE_RATE * note_dur * idx)
        note_len = min(int(SAMPLE_RATE * (note_dur + 0.05)), total - offset)
        if note_len <= 0:
            continue
        note = piano_tone_note(freq, note_len / SAMPLE_RATE, velocity=0.6 + idx * 0.1)
        for i in range(min(len(note), note_len)):
            out[offset + i] += int(note[i] * 0.6)
    peak = max(abs(s) for s in out) or 1
    scale = 32767 / peak
    return [int(s * min(scale, 0.85)) for s in out]


def apply_reverb(samples, decay=0.25, delay_sec=0.1):
    """Simple reverb via delayed + attenuated copies."""
    delay = int(SAMPLE_RATE * delay_sec)
    length = len(samples) + delay * 4
    result = samples + [0] * (length - len(samples))
    for tap in range(1, 5):
        gain = decay ** tap
        off = delay * tap
        for i in range(len(samples)):
            idx = i + off
            if idx < length:
                result[idx] = int(result[idx] + samples[i] * gain)
    peak = max(abs(s) for s in result) or 1
    scale = 32767 / peak
    return [int(s * min(scale, 0.95)) for s in result]


def write_wav(samples, path):
    with wave.open(path, 'w') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(SAMPLE_WIDTH)
        wf.setframerate(SAMPLE_RATE)
        for s in samples:
            wf.writeframes(struct.pack('<h', max(min(s, 32767), -32768)))


def generate_intro(path):
    """Cmaj7 → G/B → Am7 → Fmaj7 arpeggio + reverb."""
    seq = ['Cmaj7', 'G_B', 'Am7', 'Fmaj7']
    raw = []
    for chord in seq:
        raw.extend(arpeggio(chord, INTRO_SEC / len(seq)))
    rev = apply_reverb(raw, decay=0.25, delay_sec=0.1)
    write_wav(rev, path)


def generate_outro(path):
    """Fmaj7 → Cmaj7 arpeggio + reverb + full fade-out."""
    seq = ['Fmaj7', 'Cmaj7']
    raw = []
    for chord in seq:
        raw.extend(arpeggio(chord, OUTRO_SEC / len(seq)))
    total = len(raw)
    for i in range(total):
        raw[i] = int(raw[i] * (1.0 - i / total) ** 1.5)
    rev = apply_reverb(raw, decay=0.3, delay_sec=0.12)
    write_wav(rev, path)


def extract_text(md_path):
    """Strip frontmatter, link syntax, heading markers."""
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()
    if text.startswith('---'):
        end = text.find('---', 3)
        if end != -1:
            text = text[end + 3:]
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    return text.strip()


def generate_tts(text, output_path):
    """Edge TTS narration (neural zh-TW voices)."""
    try:
        import edge_tts
        import asyncio
    except ImportError:
        print("edge-tts not installed. Run: pip install edge-tts", file=sys.stderr)
        sys.exit(1)

    async def do_tts():
        communicate = edge_tts.Communicate(text, TTS_VOICE, rate=TTS_RATE)
        await communicate.save(output_path)

    asyncio.run(do_tts())  # pragma: no cover
    if not os.path.exists(output_path):
        print(f"TTS failed for {output_path}", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <input.md> [output.wav]', file=sys.stderr)
        print(f'Env: PODCAST_TTS_VOICE (default: zh-TW-YunJheNeural)', file=sys.stderr)
        print(f'     PODCAST_TTS_RATE (default: +0%)', file=sys.stderr)
        sys.exit(1)

    md_path = sys.argv[1]
    md_name = os.path.splitext(os.path.basename(md_path))[0]
    output_path = sys.argv[2] if len(sys.argv) > 2 else f'{md_name}.wav'

    tempdir = tempfile.mkdtemp(prefix='podcast_')
    intro_wav = os.path.join(tempdir, 'intro.wav')
    outro_wav = os.path.join(tempdir, 'outro.wav')
    tts_mp3 = os.path.join(tempdir, 'narration.mp3')

    print(f'Reading: {md_path}')
    text = extract_text(md_path)
    print(f'Text: {len(text)} chars')

    print(f'Generating intro ({INTRO_SEC}s arpeggio piano)...')
    generate_intro(intro_wav)

    print(f'Generating TTS ({TTS_VOICE})...')
    generate_tts(text, tts_mp3)

    print(f'Generating outro ({OUTRO_SEC}s)...')
    generate_outro(outro_wav)

    print('Loading audio segments...')
    intro = AudioSegment.from_wav(intro_wav)
    narration = AudioSegment.from_mp3(tts_mp3)
    outro = AudioSegment.from_wav(outro_wav)

    print('Concatenating + exporting...')
    final = intro + narration + outro
    final = final.normalize(headroom=0.5)
    final.export(output_path, format='wav')

    print(f'Done — {len(final)/1000:.1f}s')
    print(f'Output: {os.path.abspath(output_path)}')

    import shutil
    shutil.rmtree(tempdir, ignore_errors=True)


if __name__ == '__main__':
    main()
