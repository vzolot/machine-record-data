# The Machine Record: incidents involving commercial physical robots

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22925531.svg)](https://doi.org/10.5281/zenodo.22925531)

A mirror of the public register at [themachinerecord.com](https://themachinerecord.com):
documented incidents involving commercial physical robots, from robotaxis and
sidewalk delivery robots to warehouse machines, surgical systems and humanoids.
Each case on the site is followed from the first report through any recall,
investigation, lawsuit or settlement, with every source archived at the moment
it was read.

This repository holds the **case metadata** as flat files, refreshed daily from
the site's open API. The site remains the source of truth; the case page linked
in every row carries the timeline, the sources and any correction or dispute.

## Files

| File | What it is |
|---|---|
| `data/cases.csv` | One row per published case, 24 columns |
| `data/events.csv` | The timeline of every case, one row per event, with the source that establishes it |
| `data/sources.csv` | Every source with its tier, independence, language, publication date and archived copy |
| `data/sgo_links.csv` | News cases about autonomous vehicles joined to NHTSA Standing General Order filings |
| `data/cases.json` | The case rows, with the licence and export time in the header |
| `data/summary.json` | Counts by category, severity, escalation stage, origin, company, year and source language |

Column definitions: [CODEBOOK.md](CODEBOOK.md). How fields are assigned: [ANNOTATION_GUIDELINES.md](ANNOTATION_GUIDELINES.md). What the data cannot support: [LIMITATIONS.md](LIMITATIONS.md). How reproducible the labels are: [irr/](irr/2026-10-model-pilot.md). Releases: [CHANGELOG.md](CHANGELOG.md).

## Columns

The first eleven columns of `cases.csv` are the same as in release 1.0.0; thirteen were added in 1.1.0. The full definitions, including every closed vocabulary, are in [CODEBOOK.md](CODEBOOK.md).

| Column | Meaning |
|---|---|
| `ref` | Stable case reference, `TMR-0123`. Never reused |
| `url` | Permanent case page. Cases are never deleted; a withdrawn case keeps its page and says why |
| `title` | One-sentence description of the event |
| `date_of_incident` | ISO date; `date_precision` says whether it is known to the day or the month |
| `company` | Manufacturer or operator named in the sources, or empty |
| `category` | Kind of machine: `autonomous_vehicle`, `delivery`, `humanoid`, `robot_arm`, `cobot`, `industrial`, `warehouse_amr`, `surgical`, `consumer`, `service`, `agricultural`, `other` |
| `incident_type` | What happened: collision, malfunction, injury and so on |
| `severity` | From `no_harm` to `fatality` |
| `location` | Free text as reported |
| `escalation_stage` | How far the consequences went: report, investigation, recall, lawsuit, settlement and so on |
| `sources` | Number of distinct sources the case rests on |
| `origin`, `stage_evidence` | Whether the case comes from press or a primary document, and what establishes its stage |
| `environment`, `robot_model`, `summary`, `disputed`, `units_affected`, `incident_reports`, `events`, `published_at`, `updated_at` | See the codebook |

## What counts as an incident

Something that happened to a person, a vehicle or a piece of property, or an
event a regulator or court acted on. Corporate news about robotics companies is
out of scope. Cases are corroborated across at least two independent domains
before publication; the rules are at
[themachinerecord.com/methodology](https://themachinerecord.com/methodology).

This is not a safety rating. Fleet sizes are not public, so incidents per
thousand machines cannot be computed honestly from this or any other file. The
one denominator that exists, driverless miles in California, is used on the
register's site for rates per million miles; see [LIMITATIONS.md](LIMITATIONS.md).

## Loading it

```python
import pandas as pd
cases = pd.read_csv(
    "https://raw.githubusercontent.com/vzolot/machine-record-data/main/data/cases.csv"
)
cases[cases.company == "Waymo"].groupby("severity").size()

events = pd.read_csv(
    "https://raw.githubusercontent.com/vzolot/machine-record-data/main/data/events.csv"
)
events[events.ref == "TMR-0119"].sort_values("date")
```

## Licence and citation

Case metadata is published under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Reuse it with
attribution to *The Machine Record (themachinerecord.com)*. Quoted text from
news sources is not covered by this licence and stays with its publisher, which
is why the files carry links rather than article text.

To cite a single case, use its reference and URL, for example
`TMR-0238, https://themachinerecord.com/case/...`. To cite the dataset, use the
Zenodo DOI, which resolves to the latest archived release:

> The Machine Record (2026). *The Machine Record: incidents involving commercial
> physical robots* [Data set]. Zenodo. https://doi.org/10.5281/zenodo.22925531

`CITATION.cff` carries the same reference in machine-readable form.

## Releases

A versioned research release is cut every quarter and archived on Zenodo with a
changelog, the codebook and the annotation guidelines frozen with it; the
daily mirror in `data/` moves between releases. Cite a release by its version
DOI when you need a fixed snapshot, or the concept DOI for the latest.

## Updates

A GitHub Action re-exports the data every day at 08:00 UTC, after the register's
own nightly run, and commits only when something changed. The live feed of new
cases is at [themachinerecord.com/feed.xml](https://themachinerecord.com/feed.xml).

Corrections go to corrections@themachinerecord.com. Companies named in a case
can use the [right of reply](https://themachinerecord.com/right-of-reply).
