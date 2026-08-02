# Sox-Based Piano Intro/Outro Synthesis (v2 Arpeggio)

Quick sox commands to generate the v2 piano intro/outro without Python. Useful when pydub/ffmpeg isn't available or you want instant regeneration during iteration.

## Prerequisites

```bash
brew install sox
```

## Intro (6s) — Cmaj7 → G/B → Am7 → Fmaj7 arpeggio + reverb

```bash
# Generate each chord as arpeggio (notes spread across chord duration)
# Cmaj7: C4(261.63) E4(329.63) G4(392.00) B4(493.88)
sox -n -r 44100 -c 1 /tmp/c1.wav \
  synth 1.5 pl 261.63  pad 0   vol 0.5 \
  synth 1.5 pl 329.63  pad 0.4 vol 0.5 \
  synth 1.5 pl 392.00  pad 0.8 vol 0.5 \
  synth 1.5 pl 493.88  pad 1.1 vol 0.5 \
  fade t 0.01 0.01 2 \
  gain -3

# G/B: B2(123.47) D3(146.83) G3(196.00) D4(293.66)
sox -n -r 44100 -c 1 /tmp/c2.wav \
  synth 1.5 pl 123.47 pad 0   vol 0.5 \
  synth 1.5 pl 146.83 pad 0.4 vol 0.5 \
  synth 1.5 pl 196.00 pad 0.8 vol 0.5 \
  synth 1.5 pl 293.66 pad 1.1 vol 0.5 \
  fade t 0.01 0.01 2 \
  gain -3

# Am7: A2(110.00) C3(130.81) E3(164.81) G3(196.00)
sox -n -r 44100 -c 1 /tmp/c3.wav \
  synth 1.5 pl 110.00 pad 0   vol 0.5 \
  synth 1.5 pl 130.81 pad 0.4 vol 0.5 \
  synth 1.5 pl 164.81 pad 0.8 vol 0.5 \
  synth 1.5 pl 196.00 pad 1.1 vol 0.5 \
  fade t 0.01 0.01 2 \
  gain -3

# Fmaj7: F3(174.61) A3(220.00) C4(261.63) E4(329.63)
sox -n -r 44100 -c 1 /tmp/c4.wav \
  synth 1.5 pl 174.61 pad 0   vol 0.5 \
  synth 1.5 pl 220.00 pad 0.4 vol 0.5 \
  synth 1.5 pl 261.63 pad 0.8 vol 0.5 \
  synth 1.5 pl 329.63 pad 1.1 vol 0.5 \
  fade t 0.01 0.01 2 \
  gain -3

# Concatenate chords
sox /tmp/c1.wav /tmp/c2.wav /tmp/c3.wav /tmp/c4.wav /tmp/intro_raw.wav

# Reverb (4-tap delay)
sox /tmp/intro_raw.wav /tmp/intro_v2.wav \
  delay 0 0.1 0.2 0.3 \
  reverb 50 50 100 100 0 0 \
  gain -3
```

## Outro (4s) — Fmaj7 → Cmaj7 arpeggio + fade + reverb

```bash
# Fmaj7
sox -n -r 44100 -c 1 /tmp/o1.wav \
  synth 2.0 pl 174.61 pad 0   vol 0.5 \
  synth 2.0 pl 220.00 pad 0.4 vol 0.5 \
  synth 2.0 pl 261.63 pad 0.8 vol 0.5 \
  synth 2.0 pl 329.63 pad 1.1 vol 0.5 \
  fade t 0.01 0.01 2 \
  gain -3

# Cmaj7 (ending chord, sustain longer)
sox -n -r 44100 -c 1 /tmp/o2.wav \
  synth 2.0 pl 261.63 pad 0   vol 0.5 \
  synth 2.0 pl 329.63 pad 0.4 vol 0.5 \
  synth 2.0 pl 392.00 pad 0.8 vol 0.5 \
  synth 2.0 pl 523.25 pad 1.1 vol 0.5 \
  fade t 0.01 0.01 2 \
  gain -3

# Concatenate + fade out
sox /tmp/o1.wav /tmp/o2.wav /tmp/outro_raw.wav
sox /tmp/outro_raw.wav /tmp/outro_v2.wav \
  delay 0 0.12 0.24 0.36 \
  reverb 60 60 100 100 0 0 \
  fade h 0 3 1 \
  gain -3
```

## Alternative: Single-command sox intro (quick & dirty)

```bash
# Continuous arpeggio using tremolo + harmonics (less control, faster)
sox -n -r 44100 -c 1 /tmp/quick_intro.wav \
  synth 6.0 pl 261.63 pl 329.63 pl 392.00 pl 523.25 \
  tremolo 2 40 \
  reverb 30 \
  gain -5
```

## Key Parameters Explained

| Parameter | Value | Effect |
|-----------|-------|--------|
| `pl` (pluck) | — | Quick-decay waveform simulating plucked string |
| `fade t` | 0.01 0.01 N | Exponential fade with short attack (0.01s) for softer onset |
| `gain` | -3 to -6 | Headroom before reverb to prevent clipping |
| `delay` | 0 0.1 0.2 0.3 | Multi-tap delay for spatial depth (4 taps = richer reverb) |
| `reverb` | 50 50 100 100 0 0 | Room size 50, HF damping 50, stereo 100, wet-only 0 |
| `fade h` | 0 3 1 | Hold at full volume 3s then fade out over 1s |
| synth duration | 1.5s per chord | Each chord gets a full 1.5s before the next starts |

## Combine with TTS narration

Once you have `/tmp/intro_v2.wav` and `/tmp/outro_v2.wav`:

```bash
# With pydub
python3 -c "
from pydub import AudioSegment
from pydub.effects import normalize
intro = AudioSegment.from_wav('/tmp/intro_v2.wav')
outro = AudioSegment.from_wav('/tmp/outro_v2.wav')
tts = AudioSegment.from_wav('/path/to/narration.wav')
final = normalize(intro + tts + outro, headroom=0.5)
final.export('/tmp/final.wav', format='wav')
"

# Or with sox if no pydub
sox /tmp/intro_v2.wav /path/to/narration.wav /tmp/outro_v2.wav /tmp/final.wav
```

## Genesis

These sox commands were developed during session 2026-07-25 as "v2 piano" after 使用者rejected the initial block-chord version for being too electronic/piano-roll sounding. The key insight was spreading each chord into an arpeggio across the chord's duration window, and adding multi-tap reverb to simulate room ambience. The resulting sound is warmer and closer to a real pianist playing at moderate distance.
