#!/usr/bin/env python3
"""Extract the 18 GGQ rules from ggq_modal_helmholtz.f to plain-text files.

Each output file is named quadNN.txt (NN = 01..18) and contains a header
followed by lines `x_i  w_i` with full ~32-digit precision preserved from
the Fortran source (D-notation converted to E-notation).
"""
import re
import sys
from pathlib import Path

SRC = Path(__file__).parent / "ggq_modal_helmholtz.f"
OUTDIR = Path(__file__).parent / "txt"

RANGES = [
    ("2^-5",  "2^0"),
    ("2^-10", "2^-5"),
    ("2^-15", "2^-10"),
    ("2^-20", "2^-15"),
    ("2^-25", "2^-20"),
    ("2^-30", "2^-25"),
    ("2^-35", "2^-30"),
    ("2^-40", "2^-35"),
    ("2^-45", "2^-40"),
    ("2^-50", "2^-45"),
    ("2^-55", "2^-50"),
    ("2^-60", "2^-55"),
    ("2^-65", "2^-60"),
    ("2^-70", "2^-65"),
    ("2^-75", "2^-70"),
    ("2^-80", "2^-75"),
    ("2^-85", "2^-80"),
    ("2^-90", "2^-85"),
]


def extract_data_block(text: str, name: str, start: int):
    """Extract the values inside `data <name>/...../` starting from offset start.
    Returns (list of string tokens with D->E replaced, position after closing slash).
    """
    m = re.search(rf"data\s+{name}\s*/", text[start:])
    if not m:
        raise RuntimeError(f"could not find data {name}/ after offset {start}")
    body_start = start + m.end()
    close = re.search(r"/\s*$", text[body_start:], re.MULTILINE)
    if not close:
        raise RuntimeError(f"could not find closing / for data {name}/")
    body_end = body_start + close.start()
    body = text[body_start:body_end]
    # Strip Fortran continuation: each line begins with optional whitespace
    # and a single non-blank character in column 6 (digit or *).
    clean = re.sub(r"^\s*[0-9*]\s+", "", body, flags=re.MULTILINE)
    tokens = [t.strip() for t in clean.split(",") if t.strip()]
    # Convert Fortran D-notation to E-notation while preserving precision.
    tokens = [t.replace("D", "E").replace("d", "e") for t in tokens]
    return tokens, body_start + close.end()


def extract_one_rule(text: str, sub_idx: int):
    sub = re.search(rf"subroutine\s+load_quad{sub_idx}\b", text)
    if not sub:
        raise RuntimeError(f"could not find subroutine load_quad{sub_idx}")
    xs, after_x = extract_data_block(text, "xdata", sub.end())
    ws, _ = extract_data_block(text, "wdata", after_x)
    if len(xs) != len(ws):
        raise RuntimeError(
            f"rule {sub_idx}: |xdata|={len(xs)} != |wdata|={len(ws)}"
        )
    return xs, ws


def main() -> int:
    OUTDIR.mkdir(exist_ok=True)
    text = SRC.read_text()
    for i, (lo, hi) in enumerate(RANGES, start=1):
        xs, ws = extract_one_rule(text, i)
        out = OUTDIR / f"quad{i:02d}.txt"
        with out.open("w") as f:
            f.write(f"# GGQ rule {i:02d}: bm in [{lo}, {hi}]\n")
            f.write(f"# {len(xs)} nodes on [0, 1]\n")
            f.write(f"# Columns: x_i  w_i\n")
            for x, w in zip(xs, ws):
                f.write(f"{x}  {w}\n")
        print(f"wrote {out}: {len(xs)} nodes", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
