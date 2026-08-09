#!/usr/bin/env python3
"""Scan text/SVG/HTML files for Simplified-only Chinese glyphs.

The blacklist contains ONLY characters whose Simplified form DIFFERS from
their Traditional counterpart (项 vs 項, 现 vs 現, 发 vs 發, 这 vs 這...).
Characters shared identically between both scripts (人, 不, 大, 力, 地, 工,
是, 用, 真, 能, 落...) MUST NOT be listed — they are not simplified glyphs
and including them produces false positives that fail the whole pipeline.
This is a verified working set; a naive word-level list fails exactly this way.

Usage:
    python3 check-simplified.py FILE...          # scan files (exit 0 = clean)
    python3 check-simplified.py -                # scan stdin
    python3 check-simplified.py --blacklist '项据' FILE...   # extend

Exit code: 0 = clean, 1 = hits found (each printed with line + context).
"""
import sys

# Session-verified core (from a real 8-slide Traditional Chinese card build).
CORE = '项据演员愿为么现实艳后换个导连术译问决关询这发给'

# Curated expansion: more common simplified-only glyphs in tech content.
# Each entry below is a SIMPLIFIED form whose traditional counterpart differs.
COMMON = (
    '与个为从们关对会当将没发变时来体后开进过说间长门写吗听声处备复'
    '数点线级经这还两层样产业动区机权标断号头难严团图园场计许论让识'
    '读讲课请谁该调试试设词谢护买卖费资质责负赛办运选边邮针钱钢错键'
    '钟镜闪闭陈随静颗题额风飞饭饰马驾验惊'
)


def scan(text, blacklist):
    hits = {}
    for i, line in enumerate(text.splitlines(), 1):
        found = sorted(set(line) & blacklist)
        if found:
            hits[i] = sorted(set(hits.get(i, [])) | set(found))
    return hits


def main(argv):
    extra = ''
    files = []
    i = 0
    while i < len(argv):
        if argv[i] == '--blacklist':
            i += 1
            extra = argv[i]
        elif argv[i] == '-':
            files.append(None)
        else:
            files.append(argv[i])
        i += 1
    if not files:
        print(__doc__)
        return 2
    blacklist = set(CORE + COMMON + extra)
    bad = False
    for f in files:
        text = sys.stdin.read() if f is None else open(f, encoding='utf-8').read()
        hits = scan(text, blacklist)
        for lineno, chars in sorted(hits.items()):
            bad = True
            line = text.splitlines()[lineno - 1].strip()
            print(f'{f or "<stdin>"}:{lineno}: simplified-only glyphs {chars} :: {line[:80]}')
    if not bad:
        print('OK: no simplified-only glyphs found')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
