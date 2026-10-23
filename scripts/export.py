#!/usr/bin/env python3
"""Pull the register from the public API and write the mirror files.

The site is the source of truth; this repository is a convenience mirror so the
register can be loaded with one line of pandas, cited from a notebook, or picked
up by dataset indexes. Nothing here is derived that the site does not publish.

Four tables since release 1.1.0 (October 2026): cases, events (the timeline of
each case), sources (every source with its tier and archived copy) and
sgo_links (news cases joined to NHTSA Standing General Order filings). The
column definitions are in CODEBOOK.md.
"""
from __future__ import annotations

import csv
import json
import sys
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

API = "https://themachinerecord.com/api/public"
ROOT = Path(__file__).resolve().parent.parent / "data"

CASE_FIELDS = [
    # The first eleven columns keep the names and order of release 1.0.0.
    "ref", "url", "title", "date_of_incident", "company", "category",
    "incident_type", "severity", "location", "escalation_stage", "sources",
    # Added in 1.1.0.
    "date_precision", "environment", "robot_model", "company_slug", "summary",
    "origin", "stage_evidence", "disputed", "units_affected", "incident_reports",
    "events", "published_at", "updated_at",
]
EVENT_FIELDS = ["ref", "date", "event_type", "description", "source_url", "source_domain"]
SOURCE_FIELDS = [
    "ref", "url", "domain", "tier", "tier_at_publication", "counted_independent", "lang",
    "published_at", "archived_at", "archive_url", "has_full_text",
]
LINK_FIELDS = ["ref", "report_id", "confidence", "method", "linked_at"]


def fetch(path: str, page: int | None = None) -> dict:
    url = f"{API}/{path}"
    if page is not None:
        url += f"{'&' if '?' in url else '?'}page={page}&per_page=500"
    req = urllib.request.Request(url, headers={"User-Agent": "machine-record-data mirror"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def fetch_all(path: str, key: str) -> tuple[list[dict], dict]:
    first = fetch(path, 1)
    rows = list(first[key])
    for page in range(2, int(first.get("pages", 1)) + 1):
        rows.extend(fetch(path, page)[key])
    if len(rows) != int(first["total"]):
        raise SystemExit(f"{path}: expected {first['total']} rows, got {len(rows)}")
    return rows, first


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in fields})


def main() -> int:
    cases, head = fetch_all("cases", "cases")
    events, _ = fetch_all("events", "events")
    sources, _ = fetch_all("sources", "sources")
    links = fetch("sgo-links")["links"]

    # Stable order so diffs show real changes, not reshuffles.
    cases.sort(key=lambda c: c["ref"])
    events.sort(key=lambda e: (e["ref"], e.get("date") or "9999", e.get("event_type") or ""))
    sources.sort(key=lambda s: (s["ref"], s.get("published_at") or "9999", s["url"]))
    links.sort(key=lambda l: (l["ref"], l["report_id"]))
    ROOT.mkdir(parents=True, exist_ok=True)
    exported_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    with open(ROOT / "cases.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "license": head["license"],
                "attribution": head["attribution"],
                "note": head["note"],
                "source": "https://themachinerecord.com",
                "api": f"{API}/cases",
                "codebook": "https://github.com/vzolot/machine-record-data/blob/main/CODEBOOK.md",
                "exported_at": exported_at,
                "total": len(cases),
                "cases": cases,
            },
            f, ensure_ascii=False, indent=1,
        )
        f.write("\n")

    write_csv(ROOT / "cases.csv", cases, CASE_FIELDS)
    write_csv(ROOT / "events.csv", events, EVENT_FIELDS)
    write_csv(ROOT / "sources.csv", sources, SOURCE_FIELDS)
    write_csv(ROOT / "sgo_links.csv", links, LINK_FIELDS)

    years = Counter((c.get("date_of_incident") or "")[:4] or "unknown" for c in cases)
    summary = {
        "total": len(cases),
        "events": len(events),
        "sources": len(sources),
        "distinct_source_domains": len({s.get("domain") for s in sources if s.get("domain")}),
        "sgo_links": len(links),
        "by_category": dict(Counter(c.get("category") or "unknown" for c in cases).most_common()),
        "by_severity": dict(Counter(c.get("severity") or "unknown" for c in cases).most_common()),
        "by_escalation_stage": dict(Counter(c.get("escalation_stage") or "unknown" for c in cases).most_common()),
        "by_origin": dict(Counter(c.get("origin") or "unknown" for c in cases).most_common()),
        "by_company": dict(Counter(c.get("company") or "unattributed" for c in cases).most_common()),
        "by_year": dict(sorted(years.items())),
        "by_source_language": dict(Counter(s.get("lang") or "unknown" for s in sources).most_common()),
        "exported_at": exported_at,
    }
    with open(ROOT / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=1)
        f.write("\n")

    print(f"{len(cases)} cases, {len(events)} events, {len(sources)} sources, {len(links)} SGO links")
    return 0


if __name__ == "__main__":
    sys.exit(main())
