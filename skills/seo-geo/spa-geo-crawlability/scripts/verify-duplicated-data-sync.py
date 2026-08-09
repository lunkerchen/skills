#!/usr/bin/env python3
"""Verify two duplicated data arrays (TS source vs Edge Function JS copy) are verbatim identical.

Usage:
    python3 verify-duplicated-data-sync.py <fileA> <markerA> <fileB> <markerB> [--key version]

Extracts the balanced array literal that follows each marker, then compares:
  - the list of `<key>: '...'` fields (default key: version)
  - every single-quoted string literal in the array (change bullets, titles, etc.)

Exit 0 if identical; exit 1 and print per-side-only items otherwise.

Why the `= [ ` anchor: naive `src.index('[', start)` matches a TypeScript type
annotation like `ChangelogEntry[]` BEFORE the real literal, so the extracted block
is empty (or truncated). Anchor on the first `= [` after the marker, then balance
brackets by depth counting — array members are only string/object literals, so a
simple depth counter is safe.

Example (your-project changelog):
    python3 verify-duplicated-data-sync.py \
      frontend/src/data/changelog.ts 'export const publicChangelogEntries' \
      frontend/functions/content.js 'const CHANGELOG_ENTRIES = ['
"""
import re
import sys


def extract_array(path, marker):
    src = open(path, encoding='utf-8').read()
    start = src.index(marker)
    m = re.search(r'=\s*\[', src[start:])
    if not m:
        raise SystemExit(f'no `= [` array literal found after marker {marker!r} in {path}')
    i = start + m.start() + m.group(0).index('[')
    depth = 0
    j = i
    while j < len(src):
        if src[j] == '[':
            depth += 1
        elif src[j] == ']':
            depth -= 1
            if depth == 0:
                break
        j += 1
    return src[i:j + 1]


def parse(block, key):
    keys = re.findall(rf"{re.escape(key)}:\s*'([^']+)'", block)
    strings = re.findall(r"^\s*'([^']+)',?\s*$", block, re.M)
    return keys, strings


def main():
    if len(sys.argv) < 5:
        print(__doc__)
        return 2
    path_a, marker_a, path_b, marker_b = sys.argv[1:5]
    key = sys.argv[sys.argv.index('--key') + 1] if '--key' in sys.argv else 'version'
    keys_a, strs_a = parse(extract_array(path_a, marker_a), key)
    keys_b, strs_b = parse(extract_array(path_b, marker_b), key)
    ok = True
    print(f'{path_a}: {len(keys_a)} {key}s, {len(strs_a)} strings')
    print(f'{path_b}: {len(keys_b)} {key}s, {len(strs_b)} strings')
    if keys_a != keys_b:
        ok = False
        print(f'{key} mismatch: A={keys_a} B={keys_b}')
    if strs_a != strs_b:
        ok = False
        print('strings only in A:')
        for s in strs_a:
            if s not in strs_b:
                print('  ', s)
        print('strings only in B:')
        for s in strs_b:
            if s not in strs_a:
                print('  ', s)
    print('IDENTICAL' if ok else 'MISMATCH')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
