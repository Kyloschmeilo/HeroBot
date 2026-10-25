"""Checks the Fabric mixins against the Minecraft jars Loom set up for this build.

A mixin whose target method, invoked member, field or constant is gone does not fail
compilation, only the game start. This finds those cases up front by reading the vanilla
bytecode with javap. Run after a build so Loom's Minecraft jars exist:

    python3 tools/check-mixin-targets-ci.py [--github]

With --github every problem is also printed as a workflow error annotation.
"""
import glob
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GITHUB = "--github" in sys.argv

MIXIN_DIRS = [
    "herobot-mod/src/main/java/hero/bane/herobot/mod/common/mixin",
    "herobot-mod/src/client/java/hero/bane/herobot/mod/client/mixin",
]


def find_minecraft_jars():
    roots = [os.path.join(ROOT, ".gradle"), os.path.expanduser("~/.gradle/caches")]
    jars = []
    for r in roots:
        for pattern in ("**/minecraft-common*.jar", "**/minecraft-clientOnly*.jar", "**/minecraft-merged*.jar"):
            jars += [j for j in glob.glob(os.path.join(r, pattern), recursive=True)
                     if not j.endswith(("-sources.jar", "-javadoc.jar"))]
    return sorted(set(jars))


JARS = find_minecraft_jars()
if not JARS:
    print("No Minecraft jars found; run the build first.")
    sys.exit(2)
CP = os.pathsep.join(JARS)

_cache = {}


def parse(fqn):
    """-> {name: {desc: {"calls": [...], "code": [...]}}}, plus "__fields__" -> {name: desc}, or None"""
    if fqn in _cache:
        return _cache[fqn]
    r = subprocess.run(["javap", "-c", "-s", "-p", "-classpath", CP, fqn], capture_output=True, text=True)
    out_text = r.stdout
    if not out_text.strip() or "class not found" in (r.stdout + r.stderr).lower():
        _cache[fqn] = None
        return None
    table = {"__fields__": {}}
    name = desc = None
    calls = code = None
    pending_field = None

    def flush():
        if name is not None and desc is not None:
            entry = table.setdefault(name, {}).setdefault(desc, {"calls": [], "code": []})
            entry["calls"].extend(calls)
            entry["code"].extend(code)

    for line in out_text.split("\n"):
        m = re.match(r"^  (?!Code:|descriptor:|\s)(.*?)([A-Za-z_$<>][A-Za-z0-9_$.<>]*)\(.*\)(?:\s+throws[^;]*)?;\s*$", line)
        if m:
            flush()
            name = m.group(2).split(".")[-1]
            desc = None
            calls, code = [], []
            pending_field = None
            continue
        f = re.match(r"^  (?!Code:|descriptor:|\s)[^(]*?\s([A-Za-z_$][A-Za-z0-9_$]*);\s*$", line)
        if f:
            flush()
            name = desc = None
            pending_field = f.group(1)
            continue
        d = re.match(r"^\s*descriptor:\s*(\S+)\s*$", line)
        if d:
            if pending_field is not None:
                table["__fields__"][pending_field] = d.group(1)
                pending_field = None
            elif name is not None:
                desc = d.group(1)
            continue
        if name is not None and calls is not None:
            mm = re.search(r"// (?:Interface)?Method (\S+)", line)
            if mm:
                calls.append("M:" + mm.group(1))
            mf = re.search(r"// Field (\S+)", line)
            if mf:
                calls.append("F:" + mf.group(1))
            code.append(line)
    flush()
    _cache[fqn] = table
    return table


def simple_ctor(table, simple):
    if table is not None and simple in table:
        table["<init>"] = table[simple]
    return table


def constant_present(code_lines, kind, value):
    text = "\n".join(code_lines)
    if kind == "floatValue":
        v = float(value.rstrip("Ff"))
        if v in (0.0, 1.0, 2.0) and re.search(rf"fconst_{int(v)}\b", text):
            return True
        return re.search(rf"// float {re.escape(repr(v))}f?\b", text) is not None or \
            re.search(rf"// float {re.escape(str(v))}", text) is not None
    if kind == "doubleValue":
        v = float(value.rstrip("Dd"))
        return re.search(rf"// double {re.escape(str(v))}", text) is not None or \
            (v in (0.0, 1.0) and re.search(rf"dconst_{int(v)}\b", text) is not None)
    if kind == "intValue":
        v = int(value)
        if -1 <= v <= 5 and re.search(rf"iconst_{'m1' if v == -1 else v}\b", text):
            return True
        return re.search(rf"(bipush|sipush)\s+{v}\b", text) is not None or \
            re.search(rf"// int {v}\b", text) is not None
    return True


problems = []
checked = 0
for rel in MIXIN_DIRS:
    d = os.path.join(ROOT, rel)
    for fname in sorted(os.listdir(d)):
        if not fname.endswith(".java"):
            continue
        path = os.path.join(d, fname)
        src = open(path, encoding="utf-8").read()
        m = re.search(r"@Mixin\(\s*(?:value\s*=\s*)?([A-Za-z0-9_.]+)\.class", src)
        t = re.search(r'@Mixin\(\s*targets\s*=\s*"([^"]+)"', src)
        if m:
            simple = m.group(1)
            im = re.search(r"^import ([a-z][A-Za-z0-9_.]*\." + re.escape(simple) + r");", src, re.M)
            fqn = im.group(1) if im else None
        elif t:
            fqn = t.group(1)
            simple = re.split(r"[.$]", fqn)[-1]
        else:
            continue
        relpath = os.path.relpath(path, ROOT)
        if not fqn:
            problems.append((relpath, "unresolved @Mixin target import"))
            continue
        table = simple_ctor(parse(fqn), simple)
        if table is None:
            problems.append((relpath, f"target class {fqn} not found"))
            continue
        checked += 1
        fields = table["__fields__"]

        # Each injector annotation is checked on its own: its selectors, @At targets and constants.
        for block in re.finditer(r"@(Inject|Redirect|ModifyConstant|ModifyVariable|ModifyArg|ModifyArgs|"
                                 r"ModifyExpressionValue|ModifyReturnValue|WrapOperation|WrapWithCondition)\((.*?)\)\s*\n\s*(?:public|private|protected|static|void|[A-Za-z])",
                                 src, re.S):
            body = block.group(2)
            optional = re.search(r"require\s*=\s*0", body) is not None
            sels = []
            ms = re.search(r'method\s*=\s*\{([^}]*)\}', body)
            if ms:
                sels = re.findall(r'"([^"]+)"', ms.group(1))
            else:
                sels = re.findall(r'method\s*=\s*"([^"]+)"', body)
            chosen = []
            for sel in sels:
                n = sel.split("(")[0]
                if n not in table:
                    problems.append((relpath, f"{'(optional) ' if optional else ''}@{block.group(1)}: no method '{n}' in {fqn}"))
                    continue
                if "(" in sel:
                    want = sel[sel.index("("):]
                    if want not in table[n]:
                        problems.append((relpath, f"{'(optional) ' if optional else ''}@{block.group(1)}: {fqn}.{sel} not found, "
                                                  f"available: {sorted(table[n])}"))
                        continue
                    chosen.append((n, want))
                else:
                    chosen.extend((n, dd) for dd in table[n])
            if not chosen:
                continue
            calls = [c for n, dd in chosen for c in table[n][dd]["calls"]]
            code = [c for n, dd in chosen for c in table[n][dd]["code"]]
            for at in re.findall(r'target\s*=\s*"(L[^"]+)"', body):
                owner, rest = at[1:].split(";", 1)
                if ":" in rest and "(" not in rest.split(":")[0]:
                    member = rest.split(":")[0]
                    want_desc = rest.split(":", 1)[1]
                    kind = "F:"
                else:
                    member = rest.split("(")[0]
                    want_desc = rest[rest.index("("):]
                    kind = "M:"
                full = f"{owner}.{member}:{want_desc}"
                if not any(c == kind + full or c == f"{kind}{member}:{want_desc}" for c in calls):
                    near = sorted({c for c in calls if f".{member}:" in c or c.startswith(f"{kind}{member}:")})
                    problems.append((relpath, f"{'(optional) ' if optional else ''}@{block.group(1)} in "
                                              f"{[n + dd for n, dd in chosen]}: '{at}' is not used there"
                                              + (f"; same name: {near}" if near else "")))
            for kind, value in re.findall(r"@Constant\(\s*(floatValue|intValue|doubleValue)\s*=\s*([-0-9.eEfFdD]+)\s*\)", body):
                if not constant_present(code, kind, value):
                    problems.append((relpath, f"@{block.group(1)}: constant {kind}={value} not found in "
                                              f"{[n + dd for n, dd in chosen]}"))

        for acc in re.finditer(r'@(Accessor|Invoker)\(\s*(?:value\s*=\s*)?"([^"]+)"', src):
            kind, name = acc.groups()
            if kind == "Accessor" and name not in fields:
                problems.append((relpath, f"@Accessor: no field '{name}' in {fqn}"))
            if kind == "Invoker" and name not in table:
                problems.append((relpath, f"@Invoker: no method '{name}' in {fqn}"))

        for sh in re.finditer(r"@Shadow[^;{]*?\s([A-Za-z_$][A-Za-z0-9_$]*)\s*(\(|;|=)", src, re.S):
            name, kind = sh.groups()
            if kind == "(" and name not in table:
                problems.append((relpath, f"@Shadow method '{name}' not found in {fqn}"))
            if kind in (";", "=") and name not in fields:
                problems.append((relpath, f"@Shadow field '{name}' not found in {fqn}"))

# Optional: dump the bytecode of chosen vanilla methods, one "fully.qualified.Class method" per line.
dump_file = os.path.join(ROOT, "tools", "javap-dump.txt")
if os.path.exists(dump_file):
    for line in open(dump_file, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        cls, _, method = line.partition(" ")
        table = parse(cls)
        if table is None or method not in table:
            text = f"{cls} {method}: not found" + (f"; methods: {sorted(k for k in table if k != '__fields__')}" if table else "")
        else:
            text = "\n".join(f"{method}{dd}\n" + "\n".join(e["code"]) for dd, e in table[method].items())
            # keep annotations short: drop indentation, constant pool indices and package prefixes
            text = re.sub(r"^\s+", "", text, flags=re.M)
            text = re.sub(r"#\d+(,\s*\d+)?\s+//", "//", text)
            text = text.replace("net/minecraft/", "")
        print(f"== javap {cls} {method}\n{text}")
        if GITHUB:
            # GitHub cuts annotation messages at 4096 characters
            for n, i in enumerate(range(0, min(len(text), 3500 * 10), 3500)):
                esc = text[i:i + 3500].replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
                print(f"::notice title=javap {cls.split('.')[-1]}.{method} ({n + 1})::{esc}")

print(f"Checked {checked} mixins against {len(JARS)} jar(s): {', '.join(os.path.basename(j) for j in JARS)}")
print(f"{len(problems)} problem(s)")
for relpath, msg in problems:
    print(f"- {relpath}: {msg}")
    if GITHUB:
        level = "warning" if msg.startswith("(optional)") else "error"
        print(f"::{level} file={relpath},title=Mixin target::{msg}")
sys.exit(1 if any(not m.startswith("(optional)") for _, m in problems) else 0)
