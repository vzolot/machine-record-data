# Changelog

Releases are quarterly. Each release is archived on Zenodo under the concept DOI 10.5281/zenodo.22925531; the daily mirror in `data/` moves between releases.

## Unreleased (since 1.1.0)

2026-10-24: first inter-rater pilot, with a second language model as the blind annotator on 79 stratified cases: [irr/2026-10-model-pilot.md](irr/2026-10-model-pilot.md), codings in `irr/2026-10-model-pilot.csv`, scoring script `scripts/kappa.py`. Kappa 0.83 category, 0.73 severity, 0.64 incident type, 0.57 escalation stage, 0.54 environment.

Vocabulary and rules, following the pilot

- `incident_type` on rows from regulator documents is the type of the document: `collision` for NHTSA, `investigation` for OSHA, `recall` for CPSC and Safety Gate. The harm is in `severity`.
- `severity` of a case built on a court filing is what the filing alleges. A unit that catches fire is `property_damage` only when something other than the unit was damaged.
- `follow_up` is defined from the timeline, not from a single article.
- `environment` is `street` on every NHTSA row.

Data

- `environment` filled on 54 NHTSA cases (`street`) and corrected to `venue` on five cases coded `other` before that value existed.
- Company filled on four cases where every source named the maker (TMR-0153, TMR-0224, TMR-0229, TMR-0245).
- Date of TMR-0024 corrected to 2015-06-29.
- Eleven cases referred for a human read, listed in the pilot report.

## 1.1.0 (2026-10-23): first research release

Data as of 2026-10-23: 284 published cases, 720 timeline events, 694 source links across 326 domains, 14 links to NHTSA filings. Release 1.0.0 had 230 cases.

New files

- `data/events.csv`: the timeline of every case, one row per event, with the source that establishes it.
- `data/sources.csv`: every source with its tier, whether it counted as independent corroboration, its language, publication date and archived copy.
- `data/sgo_links.csv`: news cases about autonomous vehicles joined to the operator's NHTSA Standing General Order filing by rules (strong and probable links only).
- `CODEBOOK.md`, `ANNOTATION_GUIDELINES.md`, `LIMITATIONS.md`: column definitions, the rules by which fields are assigned, and what the data cannot support.

New columns in `cases.csv` (the first eleven are unchanged): `date_precision`, `environment`, `robot_model`, `company_slug`, `summary`, `origin`, `stage_evidence`, `disputed`, `units_affected`, `incident_reports`, `events`, `published_at`, `updated_at`.

Vocabulary changes

- `environment` is now a closed set (`street`, `factory`, `warehouse`, `home`, `hospital`, `retail`, `venue`, `other`); free-text values in earlier data were mapped to it.
- One free-text `incident_type` value was mapped to `malfunction`; one missing `severity` on a recall was set to `no_harm`.

Method changes since 1.0.0, all described on the register's methodology page

- Court records (dockets on CourtListener) can carry a case alone, with their own thresholds; six such cases were published in October 2026.
- The collector reads press in German, French, Italian, Spanish, Dutch, Polish, Japanese, Korean and Chinese; `sources.lang` records the language.
- The verification score threshold for press cases moved from 0.85 to 0.80 on 2026-10-22.
- The publication gates were released as the open-source package tmr-gates and the pipeline imports them unchanged.
- Three cases about the Cruise pedestrian-dragging event of 2023-10-02 were merged into TMR-0119; two Waymo recall cases of May 2025 and May 2026 remain to be separated.
- Four archived copies that pointed at the wrong page were removed from `archive_url`.

## 1.0.0 (2026-09-22)

First archived release: 230 cases, 11 columns, daily mirror from the public API.
