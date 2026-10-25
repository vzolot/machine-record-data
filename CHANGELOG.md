# Changelog

Releases are quarterly. Each release is archived on Zenodo under the concept DOI 10.5281/zenodo.22925531; the daily mirror in `data/` moves between releases.

## Unreleased (since 1.1.0)

2026-10-24: first inter-rater pilot, with a second language model as the blind annotator on 79 stratified cases: [irr/2026-10-model-pilot.md](irr/2026-10-model-pilot.md), codings in `irr/2026-10-model-pilot.csv`, scoring script `scripts/kappa.py`. Kappa 0.83 category, 0.73 severity, 0.64 incident type, 0.57 escalation stage, 0.54 environment.

Vocabulary and rules, following the pilot

- `incident_type` on rows from regulator documents is the type of the document: `collision` for NHTSA, `investigation` for OSHA, `recall` for CPSC and Safety Gate. The harm is in `severity`.
- `severity` of a case built on a court filing is what the filing alleges. A unit that catches fire is `property_damage` only when something other than the unit was damaged.
- `follow_up` is defined from the timeline, not from a single article.
- `environment` is `street` on every NHTSA row.
- `date_precision` gains the value `year`, for events the sources date only to a year; `date_of_incident` is then the first of January by convention.

Data

- `environment` filled on 54 NHTSA cases (`street`) and corrected to `venue` on five cases coded `other` before that value existed.
- Company filled on four cases where every source named the maker (TMR-0153, TMR-0224, TMR-0229, TMR-0245).
- Date of TMR-0024 corrected to 2015-06-29.
- Eleven cases referred for a human read, listed in the pilot report. Decided on 2026-10-24: TMR-0141 withdrawn (the article describes no malfunction, harm or regulatory action); TMR-0021 and TMR-0139 moved to `year` precision (2021) and their company set to KUKA, the maker of the arm, in place of the operator; TMR-0143 company set to Tesla, the striking machine's maker, in place of the struck robot's, and its category to `autonomous_vehicle`.
- Later the same day: TMR-0021 merged into TMR-0139 as one event (its reference redirects); a 2025 lawsuit about a different worker detached from TMR-0139, whose stage is now `follow_up`; TMR-0173, the 2020 penalty for the 2016 Ajin USA death, merged into TMR-0022, whose stage is now `criminal_charge` on the federal docket; TMR-0245 dated to the surgery (2012-09-26) rather than the article; TMR-0050 raised to `property_damage` (nine incidents of property damage in the CPSC notice); TMR-0170 and TMR-0205 lowered to `no_harm` (fires contained to the unit), TMR-0170 stage set to `recall` with 2,606 units and one report; TMR-0892 kept as it was, the complaint itself dates the surgery to 2020-11-17 and alleges a death.
- Duplicate sweep, same day. The two duplicates the pilot had found were of a kind the rule-based merge does not catch: one event written up twice from different articles, with dates a year or more apart. All 227 non-NHTSA published cases were scored into 322 candidate pairs by shared words, place, company and date; a language model (claude-opus-5-5) read each pair's titles, summaries and timelines and judged 33 pairs the same event; 29 were merged after the editor's read, into 23 surviving cases (the Waymo school-drop-off strike, the Austin shooting blockage and the Xi'an hug each had three or four rows). Each merged reference redirects to its survivor and the merge is on the corrections page. Published cases went from 284 to 253.
- TMR-0051 split: it held two Waymo recalls, 1,212 vehicles in May 2025 (gates and chains) and 3,791 in May 2026 (flooded roads); the second is now TMR-0897.
- `environment = factory` on the eleven OSHA cases, after reading each narrative.

Method, 2026-10-25

- Press in a language other than English is judged with two disclosed allowances (tmr-gates 0.2.0, `evaluate(..., lang=)`): the adversarial flags `named_private_individual` and `stale_as_new` do not block on their own, because the name stripper removes the name before publication and the event date is still required, and the risk ceiling is 0.5 instead of 0.35. The two-source rule, the tiers, the three-source rule for deaths and serious injuries and the date rules are unchanged. The allowances are recorded on each case's audit entry (`flags_waived`, `foreign_press`). Reason: a first pass over 300 non-English finds published nothing, with these two flags and the ceiling accounting for most refusals after verification.
- The verification prompt now resolves relative dates in local press ("yesterday", "am Montag", "昨日") against the source's publication date instead of leaving the event undated.
- Timelines hold one entry per step. Merging duplicates had carried every outlet's write-up of the same step into the surviving case, so a timeline could repeat the incident seven times. A language model grouped the entries of every published case with two or more of them into steps (the incident, each investigation, regulator action, recall, fine, lawsuit, settlement or charge) and one entry was kept per step: the one dated to the step, from the strongest source, with the most concrete description. Documents from regulators and courts were never dropped, and an escalation label was never lowered. 418 of 544 entries were removed across 74 cases; the sources of removed entries stay in the case's source set (`sources.csv`), so no source left the register. Each case's audit entry `timeline_cleaned` holds the removed rows. Script: `tmr_pipeline/timeline_clean.py` in the pipeline repository.

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
