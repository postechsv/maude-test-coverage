#!/usr/bin/env python3
"""
Utility: add missing labels to Maude equations and rules, then collect
all labels into {"Rule": {...}, "Eq": {...}}.

Exposed functions
-----------------
add_temp_labels(text: str) -> str
    Return the source with temporary labels added.

label_file(in_path: str) -> tuple[str, dict]
    Read a .maude file, insert temporary labels where needed,
    write the result to CWD/temp/<filename>, and return
    (output-file-path, {"Rule": set(...), "Eq": set(...)}).
"""
import re
import itertools
from pathlib import Path

# patterns ---------------------------------------------------------------
LINE_RE  = re.compile(r'^(\s*)(ceq|eq|rl|crl)\b(.*)$')
LABEL_RE = re.compile(r'\[[^\]]+\]\s*:')                     # in-line label
LABEL_FIND_RE = re.compile(r'\s*(ceq|eq|rl|crl)\s*\[\s*([^\]]+?)\s*\]\s*:')

def _label_generator(prefix: str):
    for idx in itertools.count(1):
        yield f"{prefix}{idx}"

# -----------------------------------------------------------------------
def add_temp_labels(source: str) -> str:
    eq_gen = _label_generator("tempEQ")
    rl_gen = _label_generator("tempRL")
    out = []

    for line in source.splitlines():
        m = LINE_RE.match(line)
        if not m:
            out.append(line)
            continue

        indent, kind, rest = m.groups()
        if LABEL_RE.search(rest):
            out.append(line)
            continue

        label = next(eq_gen if kind in ("eq", "ceq") else rl_gen)
        out.append(f"{indent}{kind} [{label}] : {rest.lstrip()}")

    return "\n".join(out) + "\n"

def _collect_labels(text: str) -> dict:
    rules, eqs = [], []
    for line in text.splitlines():
        m = LABEL_FIND_RE.match(line)
        if not m:
            continue
        kind, label = m.groups()
        (eqs if kind in ("ceq", "eq") else rules).append([label, False])
    return {"Rule": rules, "Eq": eqs}

def label_file(in_path: str):
    src = Path(in_path).read_text(encoding="utf-8")
    processed = add_temp_labels(src)

    out_dir = Path.cwd() / "temp"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / Path(in_path).name
    out_file.write_text(processed, encoding="utf-8")

    return str(out_file), _collect_labels(processed)