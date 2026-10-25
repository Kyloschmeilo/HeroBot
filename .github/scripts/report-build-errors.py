"""Turns the interesting part of a failed Gradle log into workflow annotations.

The annotations show up on the run page and in the checks API, so a failed build can be
diagnosed without downloading the full log.
"""
import re
import sys

MAX_ANNOTATIONS = 9
CHUNK = 3500  # GitHub cuts annotation messages at 4096 characters


def escape(text: str) -> str:
    return text.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


lines = open(sys.argv[1], encoding="utf-8", errors="replace").read().splitlines()

picked = []
i = 0
while i < len(lines):
    line = lines[i]
    if re.search(r"\.java:\d+: error:", line):
        # javac prints the source line and a caret below each error
        picked.extend(lines[i:i + 3])
        i += 3
        continue
    if line.startswith("* What went wrong:"):
        block = [line]
        i += 1
        while i < len(lines) and not lines[i].startswith("* Try:"):
            block.append(lines[i])
            i += 1
        picked.extend(block)
        continue
    i += 1

if not picked:
    picked = lines[-150:]

text = "\n".join(picked)
for n in range(MAX_ANNOTATIONS):
    part = text[n * CHUNK:(n + 1) * CHUNK]
    if not part:
        break
    print(f"::error title=Build log part {n + 1}::{escape(part)}")
