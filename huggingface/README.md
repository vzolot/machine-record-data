---
license: cc-by-4.0
language:
  - en
pretty_name: "The Machine Record: incidents involving commercial physical robots"
size_categories:
  - n<1K
task_categories:
  - tabular-classification
  - text-classification
tags:
  - robotics
  - robot-safety
  - autonomous-vehicles
  - robotaxi
  - humanoid-robots
  - incidents
  - recalls
configs:
  - config_name: default
    data_files:
      - split: train
        path: data/cases.csv
---

# The Machine Record: incidents involving commercial physical robots

A mirror of the public register at [themachinerecord.com](https://themachinerecord.com).
Each row is a documented incident involving a commercial physical robot
(robotaxis, delivery robots, warehouse and industrial machines, surgical
systems, humanoids), with a permanent case page that carries the timeline from
first report through any recall, investigation, lawsuit or settlement, and the
archived sources.

- One row per case, 11 columns; see the column table on GitHub:
  https://github.com/vzolot/machine-record-data
- Refreshed daily from the site's open API
- Not a safety rating: fleet sizes are not public, so rates cannot be computed
  honestly from this file

## Licence

Case metadata is CC BY 4.0, attribution to *The Machine Record
(themachinerecord.com)*. Quoted text from news sources is not included and stays
with its publisher.

## Citation

Cite a case by its reference and URL (`TMR-0238`, `https://themachinerecord.com/case/...`),
or the register as a whole via the CITATION.cff in the GitHub repository.
