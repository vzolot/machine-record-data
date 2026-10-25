# The Machine Record: a sourced register of incidents involving commercial robots and autonomous vehicles, followed from first report to legal or regulatory outcome

Draft data descriptor, prepared for submission to Data in Brief (Elsevier) or Scientific Data (Nature). Draft 1, 26 October 2026. Numbers below are the register as of that date and will be replaced by the figures of the release the paper describes (planned: release 1.2.0, January 2027).

## Authors

Volodymyr Zolotukhin (The Machine Record, Kyiv, Ukraine), hello@themachinerecord.com. Corresponding author.

Co-authors to be invited from the research contacts of outreach wave 8 (see PROJECT.md), on the condition that they contribute the inter-rater round described under Methods. The register's public editing is done under the editorial name Nils Marlow; the data descriptor is authored under the maintainer's legal name.

## Abstract

Public records of harm caused by commercial robots are fragmented across news coverage, regulator filings and court dockets, and existing AI incident databases record first reports rather than outcomes. The Machine Record is an open register of incidents involving commercial physical robots (autonomous vehicles and robotaxis, sidewalk delivery robots, humanoids, industrial arms and cobots, warehouse, surgical, consumer and service robots) in which each case is followed from the first report through any investigation, regulator action, recall, fine, lawsuit, settlement or criminal charge. The release described here holds 255 verified cases dated 1979 to 2026, 302 timeline events, 640 sources across 330 domains, of which 592 are archived, and 1,551 crash filings made by automated driving system operators under the United States National Highway Traffic Safety Administration Standing General Order, linked to news cases where the filing and the case describe the same event. Cases enter through a published, versioned set of publication gates implemented as an open-source package (tmr-gates), requiring at least two independent sources, a dated event and a named machine, with stricter rules for deaths and serious injuries. The data are distributed under CC BY 4.0 as CSV and JSON with a codebook, annotation guidelines and a limitations statement, mirrored daily on GitHub and archived quarterly on Zenodo.

## Specifications table

| | |
|---|---|
| Subject | Safety, Risk, Reliability and Quality; Robotics; Transportation |
| Specific subject area | Incident records of commercial robots and automated driving systems, with their regulatory and legal aftermath |
| Type of data | Tables (CSV, JSON); closed vocabularies; archived source links |
| Data collection | A pipeline reads Google News and Bing News in English and nine other languages, NHTSA Standing General Order files, OSHA inspection records, CPSC and EU Safety Gate recall notices and CourtListener dockets. Candidate finds are corroborated against independent sources, dated, classified and checked for duplicates by a language model and rule-based gates, then published or rejected; a sample is reviewed by a second annotator |
| Data source location | Worldwide; 164 of 255 cases are in the United States, 19 in China, 9 in the United Kingdom, 22 countries in all |
| Data accessibility | Repository: Zenodo, concept DOI 10.5281/zenodo.22925531 (versioned releases). Daily mirror: https://github.com/vzolot/machine-record-data. API without key: https://themachinerecord.com/api/public/cases. Mirrors on Hugging Face and Kaggle |
| Licence | CC BY 4.0 for case metadata; quoted source text stays with its publisher and is not distributed |

## Value of the data

- Every case carries the sequence after the first report. Of 255 cases, 88 reached a step beyond the initial report and 43 reached a regulator, a recall, a fine, a court or a settlement. This is the variable that existing incident databases lack and that liability, insurance and policy research need.
- Each claim is traceable. Every case links at least two independent sources (one for cases built on a regulator or court document), 92 percent of sources have an archived copy with its date, and the tier of each source at the time of publication is recorded, so the evidential basis of any row can be re-examined when rules change.
- The inclusion rules are public, versioned and executable. The gates are an open-source package with tests, so a reader can reproduce the publish or reject decision for any case from its recorded sources.
- The NHTSA Standing General Order filings are read by theme (what was struck, whether a safety driver intervened, whether the narrative was withheld), and 54 register cases are linked to their filing, which the federal file does not do.
- Errors are not deleted. Corrections, withdrawals and merges are recorded as events and audit entries, and each quarterly release is frozen with its codebook and changelog so that a paper can cite a fixed snapshot.

## Data description

The release has four tables.

`cases.csv` has one row per published case and 24 columns: a stable reference (`TMR-0123`), the permanent page URL, a one-sentence title without names of private individuals, date of incident and its precision (day, month or year), company, machine category, incident type, severity (ordered: no harm, property damage, minor injury, serious injury, fatality), free-text location, escalation stage (ordered: report, follow-up, investigation, regulator, recall, fine, lawsuit, settlement, criminal charge), number of sources and of events, environment, robot model, a public summary, origin (news, nhtsa, osha, cpsc, safetygate), the kind of evidence for the stage (document or press), a dispute flag, recall figures where applicable, and publication and update timestamps.

`events.csv` has one row per timeline event (302 rows): case reference, date, event type, the register's wording of what the source established, and the source that establishes it. Each step of a case's history is one event; coverage of the same step by several outlets is kept in the source table, not repeated in the timeline.

`sources.csv` has one row per source linked to a case (640 distinct sources, 688 links): URL, domain, tier at publication and current tier, whether the source counted as an independent domain at the gates, language, publication date, archive URL and archive date.

`sgo_links.csv` links register cases to NHTSA Standing General Order report identifiers with a confidence level and the matching method.

Current composition: 112 autonomous vehicle cases, 28 humanoid, 25 delivery robot, 24 consumer robot, 17 surgical, 17 robot arm, 13 industrial, 8 service, 3 warehouse, 1 agricultural, 7 other. By severity: 29 fatal, 44 serious injury, 72 minor injury, 50 property damage, 60 no harm. By origin: 184 from the press through the gates, 54 from NHTSA filings, 11 from OSHA records, 3 from CPSC and 3 from EU Safety Gate notices.

## Experimental design, materials and methods

Collection. A scheduled pipeline queries news indexes with a vocabulary of machine terms and harm terms, in English and in German, French, Italian, Spanish, Dutch, Polish, Japanese, Korean and Chinese, and ingests regulator and court feeds directly. Each find is fetched, its language detected, and its text captured at 3,000 characters for later re-verification.

Corroboration. For each find the pipeline searches for independent coverage of the same event within a window around the event date, excluding syndicated copies of the same text and the find's own domain. The find and its corroborating sources form the source set.

Verification. A language model is asked three separate questions over the source set: what the sources jointly establish (date, place, machine, company, outcome), what an adversarial reader would object to (unattributed accusation, stale event presented as new, named private individual, promotional copy), and whether the summary's claims are each covered by a source. The model's answers are recorded with the case.

Gates. A rule-based package (tmr-gates, MIT licence, versioned on PyPI) decides publication from the recorded facts: at least two independent domains of tier 1 or 2 (three for deaths and serious injuries), a dated event, a named machine, a risk ceiling, and no blocking adversarial flag. For press in a language other than English two allowances apply and are disclosed on the case: two flags do not block on their own and the risk ceiling is higher. Documents from regulators and courts publish on their own authority. Every decision is logged with the gate version.

Deduplication. A new find is matched against existing cases by shared proper nouns, title and summary similarity and company; a development of a known case (an investigation opened, a fine imposed) is attached to the case timeline rather than published as a new case, after a model check against the case's existing events.

Privacy. Names of private individuals are removed from titles, summaries and events before publication; public figures and companies are kept. A right of reply is offered to every named company and any response is published unedited.

Reliability. A pilot inter-rater round in October 2026 used a second language model as a blind annotator on 79 stratified cases: Cohen's kappa 0.83 for category, 0.73 for severity, 0.64 for incident type, 0.57 for escalation stage and 0.54 for environment. Eleven cases flagged by the pilot were reviewed by the editor, with the outcomes listed in the changelog. A human inter-rater round is planned for the release this paper will describe.

## Limitations

The register measures what was reported in the press the pipeline reads and cleared verification, not the incidence of harm. Fleet sizes and exposure are not public, so no figure in the data is a rate. Coverage is biased towards the United States and towards operators whose filings are public; Tesla's Standing General Order narratives are withheld as confidential business information and cannot be read. Locations are free text and not geocoded. Dates of older events are sometimes known only to the month or year. The full set of sources weighed at publication is recorded only for cases published after the source table was introduced; for earlier cases the set is derived from timeline events and is a lower bound. The limitations document in the repository is maintained alongside the data.

## Ethics statement

The data consist of published reports about commercial machines and the companies that make or operate them. Names of private individuals, including the injured and the deceased, are removed before publication. No personal data is collected from readers of the register beyond what they choose to submit. The work involved no human participants or animals.

## CRediT author statement

Volodymyr Zolotukhin: conceptualisation, software, data curation, methodology, writing. Further authors: to be added with their contributions.

## Declaration of competing interest

The Machine Record sells email alerts, an API tier and company dossiers built on the same data; the data themselves are free under CC BY 4.0. The author has no financial relationship with any company named in the register.

## Data availability

Concept DOI 10.5281/zenodo.22925531 (Zenodo). Daily mirror at https://github.com/vzolot/machine-record-data with CODEBOOK.md, ANNOTATION_GUIDELINES.md, LIMITATIONS.md and CHANGELOG.md. Publication gates at https://github.com/vzolot/tmr-gates. Pipeline at https://github.com/vzolot/tmr-pipeline.
