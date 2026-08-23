# opencc on macOS — Binary Compatibility Issue

## Symptom

After `pip install opencc-python-reimplemented` (v0.1.7), importing fails:

```
>>> from opencc import OpenCC
ImportError: cannot import name 'opencc_clib' from 'opencc.clib'
```

Or when opencc from a different source is installed:

```
>>> import opencc
ModuleNotFoundError: No module named 'opencc_clib'
```

## Root Cause

The `opencc` package on PyPI depends on a C extension (`opencc_clib`) that is compiled for specific platform/architecture combinations. On macOS (especially Apple Silicon M-series), the pre-built binary wheel may be incompatible with the architecture or Python version.

## Diagnostics

```bash
# Check what's installed
pip show opencc-python-reimplemented
# → Version 0.1.7

# Check if the C extension is present
ls /opt/anaconda3/lib/python3.12/site-packages/opencc/clib/
# May show .py files but no .so or .dylib
```

## Workarounds

### Option A: Use zhconv instead

```python
# Pure Python, no binary deps
pip install zhconv

from zhconv import convert
text_tw = convert(text, 'zh-tw')
```

### Option B: Manual character mapping (fallback)

Use the character mapping table in `references/character-mapping.md` to build a Python dict and apply it character by character. This is reliable on any platform but requires maintaining the mapping.

### Option C: Use the s2tw.json directly (advanced)

If you have opencc-js installed via npm:
```bash
npm install -g opencc
opencc -i input.txt -o output.txt -c s2tw
```

Or via Docker:
```bash
docker run --rm -v $(pwd):/data opencc/opencc \
  opencc -i /data/input.txt -o /data/output.txt -c s2tw
```
