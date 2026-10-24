# Known limitations

What this dataset cannot tell you, stated before you find out the hard way. Read this before computing anything that looks like a rate or a ranking.

## 1. The register counts reporting, not events

A case exists because somebody wrote about the event in a form that passed the publication gates, or because a regulator or court recorded it. Incidents that never reach the press, a regulator or a court are absent. Routine faults, near misses that nobody filmed and injuries settled quietly are the majority of what happens and almost none of what is here.

## 2. Attention is uneven across companies

A widely covered company accumulates more cases than a small manufacturer with the same incident. Waymo has the most cases in the register partly because it reports every contact to NHTSA under the Standing General Order and partly because it drives the most miles. Case counts per company measure visibility as well as safety. Do not rank companies by row count.

## 3. There is a denominator only for driverless cars in California

Rates per million miles exist where an operator reports both its crashes to NHTSA and its miles to the California Public Utilities Commission for the same months; the register publishes those on its site. For every other row there is a numerator and no base. Fleet sizes of delivery robots, humanoids, surgical systems and industrial arms are not public. A rate per unit is possible only for recalls, where `units_affected` is given.

## 4. Coverage was English-only until October 2026

Until release 1.1.0 an incident in Shenzhen or Osaka entered the register only if somebody wrote about it in English. The collector now also reads German, French, Italian, Spanish, Dutch, Polish, Japanese, Korean and Chinese press, with the same gates, and `sources.lang` records the language of every source. That coverage is newer and thinner, so Asia and continental Europe remain under-represented relative to reality, and the share of non-English sources in this release is small.

## 5. Dates and places carry stated precision

`date_precision` is `day`, `month` or `year`. Where it is `month`, `date_of_incident` is the first of that month by convention; the event happened some time in that month. Where it is `year`, it is the first of January and the event happened some time in that year. NHTSA filings only ever give the month. `location` is free text as reported and has not been geocoded; the same city appears with and without a state or country.

## 6. Fields were extracted by a language model, then gated by rules

`title`, `summary`, `company`, `robot_model`, `date_of_incident`, `location`, `severity`, `incident_type`, `category` and `environment` were extracted from the sources by a model under the rules in ANNOTATION_GUIDELINES.md, cross-checked against the sources, and accepted only when the gates passed. `category` is normalised to a closed vocabulary by rules after extraction. Model extraction has an error rate that has not yet been measured against a second human annotator. A first pilot with a different language model as the blind second annotator ([irr/2026-10-model-pilot.md](irr/2026-10-model-pilot.md), 79 cases) found Cohen's kappa of 0.83 for `category`, 0.73 for `severity`, 0.64 for `incident_type`, 0.57 for `escalation_stage` and 0.54 for `environment`; most of the moderate scores traced to gaps in the written rules, which were then closed, and to fields never filled for regulator rows, which were then filled. A human study on the same sample is the next step. Treat severity and incident type as good but not yet human-audited labels.

## 7. Older cases keep fewer sources than they were verified on

140 news cases published before the corroborating set was recorded keep only the source they were written from. The second domain was required at the time and simply not retained, and each of those case pages says so. `sources.counted_independent` is null for those rows.

## 8. Cases from regulator documents did not go through the news gates

Rows with `origin` of `nhtsa`, `osha`, `cpsc` or `safetygate` were created from one primary document each, on purpose: the document is the evidence rather than an account of it. They carry `stage_evidence = document`. NHTSA rows are a severe subset of the SGO file (hospitalisation or worse), not every filing; the full SGO table is on the site.

## 9. Duplicates have been found and merged, and more may exist

The same event can arrive months apart under different company names or with dates one or two days apart, and automatic matching does not always catch it. Merged cases keep their reference as a redirect to the surviving case and are not in this file. If you find two rows for one event, write to corrections@themachinerecord.com.

## 10. Links to NHTSA filings are rule-based and incomplete

`sgo_links.csv` joins news cases to the operator's NHTSA filing by month, state, city, counterpart and severity. Only `strong` and `probable` links are published; where several filings tie, no link is given. Absence of a link does not mean the operator did not file.

## 11. Nothing here is a finding of fault

A case records that an event was reported, what the sources said and what happened next. A lawsuit is an allegation; an investigation is not a conclusion; a recall is a manufacturer's or regulator's decision. `disputed = true` means a named company has contested the case and the dispute is published on the case page.
