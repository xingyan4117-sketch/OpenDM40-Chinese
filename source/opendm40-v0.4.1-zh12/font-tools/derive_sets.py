#!/usr/bin/env python3
"""Derive keep_cjk.txt and need_glyphs.txt from the patched sources.

Only text inside string literals is counted. Scanning whole files pulled in
characters that appear only in comments (the vendor's traditional forms show
up in the doc comments), and those glyphs cost ~60 bytes each of a region B
that has almost nothing free.

    python derive_sets.py STOCK_CJK_SET_FILE PATCHED_SRC...

writes keep_cjk.txt (characters the vendor font already has) and
need_glyphs.txt (characters that must be drawn, in first-appearance order).
"""

import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
stock_path = sys.argv[1]
srcs = sys.argv[2:]

stock = set(io.open(stock_path, encoding="utf-8").read().strip())

# Drop // comments (the sources have no "//" inside a literal that matters),
# then take what sits between double quotes.
NO_COMMENT = re.compile(r"//[^\n]*")
LITERAL = re.compile(r'"([^"\n]*)"')
# The sources write some CJK as Rust \u{7ec4} escapes (the main-menu
# "组合视图：" prefix, the gallery pager, the limits titles); without
# decoding, their glyphs never reach need_glyphs.txt and render blank.
ESCAPE = re.compile(r"\\u\{([0-9A-Fa-f]{1,6})\}")

def _decode(s):
    return ESCAPE.sub(lambda m: chr(int(m.group(1), 16)), s)

def _wanted(ch):
    """CJK ideographs plus the full-width punctuation the literals use."""
    o = ord(ch)
    return (0x4E00 <= o <= 0x9FFF        # hanzi
            or 0x3000 <= o <= 0x303F    # 。、，etc.
            or 0x2010 <= o <= 0x205E    # … — etc.
            or 0xFF00 <= o <= 0xFFEF    # ？：，etc. (full-width forms)
            or 0x0370 <= o <= 0x03FF    # 希腊字母：μ（μA）等
            or o in (0x2103, 0x2109))   # ℃ ℉


seen = []
for p in srcs:
    text = io.open(p, encoding="utf-8").read()
    for m in LITERAL.finditer(NO_COMMENT.sub("", text)):
        for ch in _decode(m.group(1)):
            if _wanted(ch) and ch not in seen:
                seen.append(ch)

keep = [c for c in seen if c in stock]
draw = [c for c in seen if c not in stock]

io.open(os.path.join(HERE, "keep_cjk.txt"), "w", encoding="utf-8", newline="\n").write("".join(keep))
io.open(os.path.join(HERE, "need_glyphs.txt"), "w", encoding="utf-8", newline="\n").write("".join(draw))

sys.stderr.write("sources: %d\n" % len(srcs))
sys.stderr.write("CJK in literals: %d (%d from the vendor font, %d to draw)\n"
                 % (len(seen), len(keep), len(draw)))
sys.stderr.write("keep: %s\n" % "".join(keep))
sys.stderr.write("draw: %s\n" % "".join(draw))
