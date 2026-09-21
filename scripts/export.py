#!/usr/bin/env python3
"""Pull every published case from the public API and write the mirror files.

The site is the source of truth; this repository is a convenience mirror so the
register can be loaded with one line of pandas, cited from a notebook, or picked
up by dataset indexes. Nothing here is derived that the site does not publish.
"""
from __future__ import annotations

import csv
import json
import sys
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

API = "https://themachinerecord.com/api/public/cases"
FIELDS = [
    "ref", "url", "title", "date_of_incident", "company", "category",
    "incident_type", "severity", "location", "escalation_stage", "sources",
]
ROOT = Path(__file__).resolve().parent.parent / "data"


def fetch(page: int) -> dict:
    req = urllib.request.Request(
        f"{API}?page={page}", headers={"User-Agent": "machine-record-data mirror"}
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def main() -> int:
    first = fetch(1)
    cases = list(first["cases"])
    for page in range(2, int(first.get("pages", 1)) + 1):
        cases.extend(fetch(page)["cases"])
    if len(cases) != int(first["total"]):
        print(f"expected {first['total']} cases, got {len(cases)}", file=sys.stderr)
        return 1

    # Stable order so diffs show real changes, not reshuffles.
    cases.sort(key=lambda c: c["ref"])
    ROOT.mkdir(parents=True, exist_ok=True)

    with open(ROOT / "cases.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "license": first["license"],
                "attribution": first["attribution"],
                "note": first["note"],
                "source": "https://themachinerecord.com",
                "api": API,
                "exported_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "total": len(cases),
                "cases": cases,
            },
            f, ensure_ascii=False, indent=1,
        )
        f.write("\n")

    with open(ROOT / "cases.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        for c in cases:
            w.writerow({k: ("" if c.get(k) is None else c.get(k)) for k in FIELDS})

    years = Counter((c.get("date_of_incident") or "")[:4] or "unknown" for c in cases)
    summary = {
        "total": len(cases),
        "by_category": dict(Counter(c.get("category") or "unknown" for c in cases).most_common()),
        "by_severity": dict(Counter(c.get("severity") or "unknown" for c in cases).most_common()),
        "by_escalation_stage": dict(Counter(c.get("escalation_stage") or "unknown" for c in cases).most_common()),
        "by_company": dict(Counter(c.get("company") or "unattributed" for c in cases).most_common()),
        "by_year": dict(sorted(years.items())),
        "exported_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    with open(ROOT / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=1)
        f.write("\n")

    print(f"{len(cases)} cases written to {ROOT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
