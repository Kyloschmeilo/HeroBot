"""Summarises a smoke-test server log: which checks passed, which failed, and any errors.

    python3 tools/smoke-test/report.py <name> <latest.log> [--github]
"""
import re
import sys

platform, path = sys.argv[1], sys.argv[2]
github = "--github" in sys.argv
try:
    lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
except FileNotFoundError:
    lines = []

ok = [m.group(1) for line in lines if (m := re.search(r"SMOKE OK (\S+)", line))]
fail = [m.group(1) for line in lines if (m := re.search(r"SMOKE FAIL (\S+)", line))]
info = [line.split("SMOKE INFO ", 1)[1] for line in lines if "SMOKE INFO " in line]
started = any("SMOKE START" in line for line in lines)
done = any("SMOKE DONE" in line for line in lines)

problems = []
i = 0
while i < len(lines):
    line = lines[i]
    if re.search(r"/(ERROR|FATAL)\]|Exception|Error:|\bat [a-z]+\.[\w.$]+\(", line) and "SMOKE" not in line:
        block = [line]
        j = i + 1
        while j < len(lines) and len(block) < 25 and (lines[j].startswith(("\t", "    at ", "Caused by")) or re.match(r"^\s+at ", lines[j])):
            block.append(lines[j])
            j += 1
        problems.append("\n".join(block))
        i = j
        continue
    i += 1

summary = [f"{platform}: started={started} done={done} ok={len(ok)} fail={len(fail)}",
           "OK: " + ", ".join(ok),
           "FAIL: " + (", ".join(fail) or "-")] + ["INFO " + i for i in info]
print("\n".join(summary))
print(f"{len(problems)} error block(s)")
for p in problems:
    print(p)
    print("-" * 40)


def annotate(level, title, text):
    for n, i in enumerate(range(0, min(len(text), 3500 * 6), 3500)):
        esc = text[i:i + 3500].replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        print(f"::{level} title={title} ({n + 1})::{esc}")


if github:
    good = started and done and not fail
    annotate("notice" if good else "error", f"Smoke test {platform}", "\n".join(summary))
    if problems:
        annotate("warning", f"Smoke test {platform} log errors", "\n\n".join(problems))
    if not lines:
        annotate("error", f"Smoke test {platform}", "no server log found")
    elif not done:
        annotate("error", f"Smoke test {platform} log tail", "\n".join(lines[-60:]))
