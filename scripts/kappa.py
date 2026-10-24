#!/usr/bin/env python3
"""Cohen's kappa for a double-coded sample of cases.

Input: a CSV with the columns ref, origin, field, register, annotator_b, one row
per case and field (the layout of irr/*.csv in this repository). Output: per
field, the number of cases, raw agreement, unweighted kappa and, for the two
ordered scales (severity, escalation_stage), linear weighted kappa.

    python3 scripts/kappa.py irr/2026-10-model-pilot.csv
    python3 scripts/kappa.py irr/2026-10-model-pilot.csv --origin news

No dependencies beyond the standard library, so a second annotator can check
their own numbers without installing anything.
"""
from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict

SEVERITY = ["no_harm", "property_damage", "minor_injury", "serious_injury", "fatality"]
STAGES = ["report", "follow_up", "investigation", "regulator", "recall", "fine",
          "lawsuit", "settlement", "criminal_charge"]
ORDERED = {"severity": SEVERITY, "escalation_stage": STAGES}


def kappa(a: list[str], b: list[str], labels: list[str] | None = None,
          weights: str | None = None) -> float | None:
    if not a:
        return None
    labels = labels or sorted(set(a) | set(b))
    idx = {l: i for i, l in enumerate(labels)}
    k, n = len(labels), len(a)
    m = [[0] * k for _ in range(k)]
    for x, y in zip(a, b):
        m[idx[x]][idx[y]] += 1
    row = [sum(m[i]) for i in range(k)]
    col = [sum(m[i][j] for i in range(k)) for j in range(k)]

    def w(i: int, j: int) -> float:
        if weights is None:
            return 0.0 if i == j else 1.0
        d = abs(i - j) / (k - 1) if k > 1 else 0.0
        return d if weights == "linear" else d * d

    po = sum(w(i, j) * m[i][j] for i in range(k) for j in range(k)) / n
    pe = sum(w(i, j) * row[i] * col[j] for i in range(k) for j in range(k)) / (n * n)
    return 1.0 if pe == 0 else 1.0 - po / pe


def reading(k: float | None) -> str:
    if k is None:
        return "n/a"
    for limit, word in ((0.2, "slight"), (0.4, "fair"), (0.6, "moderate"), (0.8, "substantial")):
        if k < limit:
            return word
    return "almost perfect"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--origin", help="restrict to one origin, e.g. news or nhtsa")
    args = ap.parse_args()
    pairs: dict[str, list[tuple[str, str]]] = defaultdict(list)
    with open(args.csv, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if args.origin and r["origin"] != args.origin:
                continue
            pairs[r["field"]].append((r["register"] or "none", r["annotator_b"] or "none"))
    print(f"{'field':<18}{'n':>5}{'agree':>8}{'kappa':>8}{'w.kappa':>9}  reading")
    for field, rows in pairs.items():
        a = [x for x, _ in rows]
        b = [y for _, y in rows]
        agree = sum(1 for x, y in rows if x == y) / len(rows)
        k = kappa(a, b)
        kw = ""
        if field in ORDERED:
            labels = ORDERED[field] + sorted((set(a) | set(b)) - set(ORDERED[field]))
            kw = f"{kappa(a, b, labels, 'linear'):.2f}"
        print(f"{field:<18}{len(rows):>5}{agree:>8.0%}{k:>8.2f}{kw:>9}  {reading(k)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
