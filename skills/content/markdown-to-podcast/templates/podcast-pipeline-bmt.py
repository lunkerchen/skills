#!/usr/bin/env python3
"""
Markdown → Podcast Pipeline (BlueMagpie-TTS variant).
Reads markdown, generates arpeggio piano intro/outro, narrates via
BlueMagpie-TTS (built-in speaker or voice clone), and concatenates to WAV.

Usage:
    python3 podcast-pipeline-bmt.py <input.md> [output.wav]              # hung_yi_lee
    python3 podcast-pipeline-bmt.py <input.md> [output.wav] --clone      # voice clone via DJI ref

Environment:
    BMT_CLONE_REF    Path to reference WAV for voice cloning
                     (default: $VOICE_CLONE_AUDIO_DIR/DJI_27_...)
"""

import sys, os, re, tempfile, struct, wave, math, shutil
from pydub import AudioSegment
from pydub.effects import normalize

# ── Config ──
SAMPLE_RATE = 44100
INTRO_SEC = 6
OUTRO_SEC = 4
TTS_SLOW_PCT = 0.85          # ffmpeg atempo factor (0.85 = 15% slower)

CHORDS = {
    'Cmaj7': [261.63, 329.63, 392.00, 523.25],
    'G_B':   [246.94, 392.00, 493.88, 587.33],
    'Am7':   [220.00, 392.00, 440.00, 523.25],
    'Fmaj7': [349.23, 440.00, 523.25, 659.25],
}

DEFAULT_CLONE_REF = "$VOICE_CLONE_AUDIO_DIR/DJI_27_20260401_180028.WAV"


def piano_tone_note(freq, duration_sec, velocity=0.8):
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
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        for s in samples:
            wf.writeframes(struct.pack('<h', max(min(s, 32767), -32768)))


def generate_intro(path):
    seq = ['Cmaj7', 'G_B', 'Am7', 'Fmaj7']
    raw = []
    for chord in seq:
        raw.extend(arpeggio(chord, INTRO_SEC / len(seq)))
    rev = apply_reverb(raw)
    write_wav(rev, path)


def generate_outro(path):
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


def generate_tts_bmt(text, output_wav, mode='centroid', ref_path=None):
    """
    Generate TTS via BlueMagpie-TTS. Two modes:
      - 'centroid': use built-in hung_yi_lee speaker centroid
      - 'clone': use reference_wav_path for voice cloning

    PITFALL: 'clone' mode + text with many line-break pauses can produce
    unclear output. Prefer 'centroid' for pause-rich text. If 'clone'
    is needed, keep text continuous and insert silence post-hoc via pydub.
    """
    import torch
    import soundfile as sf
    from huggingface_hub import snapshot_download
    from transformers import PreTrainedTokenizerFast
    from bluemagpie import BlueMagpieModel

    model_dir = snapshot_download('OpenFormosa/BlueMagpie-TTS')
    tokenizer = PreTrainedTokenizerFast(
        tokenizer_file=os.path.join(model_dir, 'tokenizer.json')
    )
    model = BlueMagpieModel.from_local(
        model_dir, tokenizer=tokenizer, training=False, device='mps'
    )

    if mode == 'centroid':
        centroids = torch.load(
            os.path.join(model_dir, 'checkpoints', 'hung_yi_lee_speaker_centroids.pt'),
            map_location='cpu', weights_only=True
        )
        speaker_centroid = centroids['centroids'][
            centroids['speaker_ids'].index('hung_yi_lee')
        ]
        audio = model.generate(
            target_text=text,
            speaker_centroid=speaker_centroid,
            cfg_value=2.8,
            inference_timesteps=9,
            max_len=3000,
            retry_badcase=True,
        )
    else:
        ref = ref_path or DEFAULT_CLONE_REF
        audio = model.generate(
            target_text=text,
            reference_wav_path=ref,
            cfg_value=2.8,
            inference_timesteps=9,
            max_len=3000,
            retry_badcase=True,
        )

    sf.write(output_wav, audio.squeeze().cpu().numpy(), model.sample_rate)
    print(f'  TTS duration: {audio.squeeze().shape[0] / model.sample_rate:.1f}s')
    print(f'  Mode: {mode}')


def slow_down(input_wav, output_wav, factor=TTS_SLOW_PCT):
    """Apply ffmpeg atempo to slow narration for more natural cadence."""
    import subprocess
    cmd = ['ffmpeg', '-y', '-i', input_wav,
           '-filter:a', f'atempo={factor}', output_wav]
    subprocess.run(cmd, capture_output=True, check=True)
    print(f'  Slowed to {factor*100:.0f}% speed')


def main():
    use_clone = '--clone' in sys.argv
    if use_clone:
        sys.argv.remove('--clone')

    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <input.md> [output.wav] [--clone]', file=sys.stderr)
        sys.exit(1)

    md_path = sys.argv[1]
    md_name = os.path.splitext(os.path.basename(md_path))[0]
    output_path = sys.argv[2] if len(sys.argv) > 2 else f'{md_name}.wav'

    tempdir = tempfile.mkdtemp(prefix='podcast_bmt_')
    intro_wav = os.path.join(tempdir, 'intro.wav')
    outro_wav = os.path.join(tempdir, 'outro.wav')
    tts_raw = os.path.join(tempdir, 'narration_raw.wav')
    tts_final = os.path.join(tempdir, 'narration.wav')

    print(f'Reading: {md_path}')
    text = extract_text(md_path)
    print(f'Text: {len(text)} chars')

    print(f'Generating intro ({INTRO_SEC}s arpeggio piano)...')
    generate_intro(intro_wav)

    print(f'Generating TTS via BlueMagpie ({ "clone" if use_clone else "hung_yi_lee" })...')
    generate_tts_bmt(text, tts_raw, mode='clone' if use_clone else 'centroid')

    print(f'Slowing narration to {TTS_SLOW_PCT*100:.0f}%...')
    slow_down(tts_raw, tts_final)

    print(f'Generating outro ({OUTRO_SEC}s)...')
    generate_outro(outro_wav)

    print('Loading + concatenating...')
    intro = AudioSegment.from_wav(intro_wav)
    narration = AudioSegment.from_wav(tts_final)
    outro = AudioSegment.from_wav(outro_wav)
    final = normalize(intro + narration + outro, headroom=0.5)
    final.export(output_path, format='wav')

    print(f'Done — {len(final)/1000:.1f}s')
    print(f'Output: {os.path.abspath(output_path)}')

    shutil.rmtree(tempdir, ignore_errors=True)


if __name__ == '__main__':
    main()
