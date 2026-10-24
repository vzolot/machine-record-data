# Codebook

Release 1.1.0, October 2026. Four tables, one row per case, per timeline event, per source and per NHTSA link. All files are UTF-8 CSV with a header row; `cases.json` carries the case rows with a licence header. Empty string means unknown or not applicable. Dates are ISO 8601; timestamps are UTC.

Definitions of the closed vocabularies and the rules for assigning them are in [ANNOTATION_GUIDELINES.md](ANNOTATION_GUIDELINES.md). What the data cannot support is in [LIMITATIONS.md](LIMITATIONS.md).

## cases.csv

One row per published case. The first eleven columns keep the names and order of release 1.0.0.

| Column | Type | Meaning |
|---|---|---|
| `ref` | string | Stable case reference, `TMR-0123`. Never reused. A merged duplicate keeps its reference as a redirect and does not appear here |
| `url` | string | Permanent case page with timeline, sources, corrections and any dispute |
| `title` | string | One factual sentence describing the event, in English, without names of private individuals |
| `date_of_incident` | date | Date the event happened. When `date_precision` is `month`, the first day of that month by convention; when it is `year`, the first of January of that year |
| `company` | string | Manufacturer or operator named in the sources as responsible for the machine; empty if none named |
| `category` | enum | Kind of machine: `autonomous_vehicle`, `delivery`, `humanoid`, `robot_arm`, `cobot`, `industrial`, `warehouse_amr`, `surgical`, `consumer`, `service`, `agricultural`, `other` |
| `incident_type` | enum | What happened: `collision`, `malfunction`, `injury`, `fatality`, `fire`, `near_miss`, `entrapment`, `runaway`, `property_damage`, `recall`, `investigation`, `lawsuit`, `settlement`, `fine`, `citation`, `other` |
| `severity` | enum, ordered | Worst outcome to a person: `no_harm` < `property_damage` < `minor_injury` < `serious_injury` < `fatality` |
| `location` | string | Free text as reported, most specific place the sources agree on; not geocoded |
| `escalation_stage` | enum, ordered | Furthest consequence on record: `report` < `follow_up` < `investigation` < `regulator` < `recall` < `fine` < `lawsuit` < `settlement` < `criminal_charge` |
| `sources` | integer | Number of distinct sources linked to the case |
| `date_precision` | enum | `day`, `month` or `year` |
| `environment` | enum | Where the machine was operating: `street`, `factory`, `warehouse`, `home`, `hospital`, `retail`, `venue`, `other`; empty when the sources do not say |
| `robot_model` | string | Product name as the maker writes it; empty if not given |
| `company_slug` | string | Key of the company page, `https://themachinerecord.com/company/<company_slug>` |
| `summary` | string | Two to four factual sentences, each traceable to a source; public version with private names removed |
| `origin` | enum | Where the case came from: `news` (press, through the gates), `nhtsa` (Standing General Order filing), `osha` (workplace inspection record), `cpsc` (consumer product recall), `safetygate` (EU Safety Gate alert) |
| `stage_evidence` | enum | What establishes `escalation_stage`: `document` (a regulator or court document linked to the case) or `press` |
| `disputed` | boolean | A named company has contested the case through the right of reply; the dispute is published on the case page |
| `units_affected` | integer | For recalls, the number of units the notice covers; empty otherwise |
| `incident_reports` | integer | For recalls, the number of incidents the notice acknowledges; empty otherwise |
| `events` | integer | Number of timeline events in `events.csv` for this case |
| `published_at` | timestamp | When the case was published on the register |
| `updated_at` | timestamp | Last change to any field of the case |

## events.csv

One row per timeline event. A case has at least one. Together with `cases.csv` this is the sequence from first report to any recall, investigation, lawsuit or settlement.

| Column | Type | Meaning |
|---|---|---|
| `ref` | string | Case reference |
| `date` | date | Date of the event, or of the document that records it |
| `event_type` | enum | `report`, `follow_up`, `investigation`, `regulator`, `recall`, `lawsuit`, `settlement`, `fine`, `citation`, `criminal_charge`, `correction` |
| `description` | string | The register's own wording of what the source established, public version |
| `source_url` | string | The source that establishes this event, if any |
| `source_domain` | string | Its domain |

## sources.csv

One row per source linked to a case. A source used by two cases appears twice. Article text is not distributed; links and metadata only.

| Column | Type | Meaning |
|---|---|---|
| `ref` | string | Case reference |
| `url` | string | Canonical URL of the source |
| `domain` | string | Registered domain without `www.` |
| `tier` | integer | Current tier of the domain under the published lists: 1 wire agencies, national outlets, regulators, courts; 2 other outlets that do their own reporting, including unknown ones; 3 social networks, blogs, tabloids, syndication portals |
| `tier_at_publication` | integer | Tier the source had when the case was published; lists change, decisions are kept as made |
| `counted_independent` | boolean | Whether this source counted toward the independent-domain rule when the case was published; empty for cases published before the corroborating set was recorded |
| `lang` | string | ISO 639-1 language of the source text, detected; empty for sources recorded before October 2026 |
| `published_at` | date | Publication date of the source as reported by it |
| `archived_at` | timestamp | When the register saved a copy |
| `archive_url` | string | Copy on the Internet Archive, if one exists |
| `has_full_text` | boolean | Whether the register captured the full article text when verifying |

## sgo_links.csv

Rule-based links between news cases about autonomous vehicles and the operator's filing to NHTSA under the Standing General Order. Only links the rules rate `strong` or `probable` are published.

| Column | Type | Meaning |
|---|---|---|
| `ref` | string | Case reference |
| `report_id` | string | NHTSA report ID; the filing is searchable at `https://themachinerecord.com/reports/sgo?q=<report_id>` |
| `confidence` | enum | `strong` (single candidate, high score) or `probable` (single candidate, lower score) |
| `method` | string | Version of the linking rules, `rules_v1` |
| `linked_at` | timestamp | When the link was made |

## summary.json

Counts by category, severity, escalation stage, origin, company, year of incident and source language, with the export time. Derived from the tables above; recompute rather than cite.

## Provenance

Every value is either a primary document (NHTSA, OSHA, CPSC, EU Safety Gate, a court docket) or press reporting that passed the gates in the open-source package [tmr-gates](https://github.com/vzolot/tmr-gates): the same event across at least two independent domains, source tiers, three sources with a tier 1 for a death or serious injury attributed to a named company, an adversarial pass for satire, defamation and stale news, and date checks. The register's [methodology](https://themachinerecord.com/methodology) describes the same rules in prose.
