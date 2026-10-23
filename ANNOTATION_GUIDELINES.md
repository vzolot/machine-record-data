# Annotation guidelines

How the fields of a case are assigned. The register assigns them with a language model under these rules and then gates the result; a human annotator coding the same case should follow the same rules, so that agreement between the two can be measured. Every rule here is the one the production prompt and the gate code use.

## Unit of analysis

One case is one real-world event: something that happened at a time and a place involving a commercial physical robot or automated machine. A collision, the investigation of it, the recall it caused and the lawsuit that followed are one case with several timeline events, not four cases. Two articles about the same event are two sources of one case. Two events on different days are two cases even if the same machine was involved.

Out of scope: product launches, demos that went as planned, funding news, opinion pieces, fiction, military and police robots in combat use, and anything where no physical machine was involved.

## What counts as an incident

An event counts when a person, a vehicle or a piece of property was affected, or when a regulator, a court or a manufacturer acted (investigation, recall, lawsuit, fine, settlement). An event with `severity = no_harm` is kept only when `incident_type` is one of the acting or failing types: collision, malfunction, near_miss, fire, recall, investigation, lawsuit, settlement, fine, citation, runaway, entrapment. "No harm" plus "injury" is a contradiction and is rejected.

## Fields

### `date_of_incident` and `date_precision`

The date the event happened, not the date of the article. Take it from the body of the article, never from a headline or a URL. If the sources give only a month, record the first of the month and set `date_precision = month`; never invent a day. If the date is unknown, the case does not publish. A date in the future, or later than the earliest publication by more than two days, fails the gate.

### `location`

The most specific place the sources agree on, as reported: "Austin, Texas, USA" or "Shenzhen, China". Take it from the article body; a San Diego paper reporting a fire in Berkeley does not make the fire happen in San Diego. Do not infer a city from the company's headquarters.

### `company`

The manufacturer or operator the sources name as responsible for the machine. If the sources name the operator (a hospital) but the machine's maker is known (Intuitive Surgical), record the maker; the operator goes in the summary. If no company is named, leave empty. Do not guess the maker from the type of machine.

### `robot_model`

The product name as the maker writes it (Jaguar I-Pace, Unitree G1, da Vinci Xi). Empty if the sources give none.

### `category` (closed set)

The kind of machine, not what happened to it.

| Code | Definition |
|---|---|
| `autonomous_vehicle` | robotaxi, self-driving car, driverless shuttle or truck on public roads |
| `delivery` | sidewalk or road delivery robot, drone delivery |
| `humanoid` | bipedal humanoid platform (Unitree H1 or G1, Optimus, Figure, Digit) |
| `robot_arm` | fixed industrial or hobby manipulator arm, including chess and cooking robots |
| `cobot` | collaborative arm working next to people without a cage |
| `industrial` | other factory, plant, construction or logistics machinery with autonomy |
| `warehouse_amr` | autonomous mobile robot in a warehouse or fulfilment centre |
| `surgical` | surgical or medical robot in a clinical setting |
| `consumer` | home robot: vacuum, lawn mower, pool cleaner, toy, companion |
| `service` | commercial service robot: quadruped, security, cleaning, hospitality, patrol |
| `agricultural` | farm or field robot |
| `other` | physical robot that fits none of the above |

### `incident_type` (closed set)

What happened, one value. When several apply, the most consequential wins in this order: fatality, injury, fire, collision, entrapment, runaway, malfunction, near_miss, property_damage, then the procedural types recall, investigation, lawsuit, settlement, fine, citation, which are used when the case was created from that procedural act rather than from the underlying event.

| Code | Use when |
|---|---|
| `collision` | the machine struck or was struck by a person, vehicle or object |
| `malfunction` | the machine failed or behaved wrongly without a collision (froze, drove into a closed road, fell, caught in a loop) |
| `injury` | a person was hurt in a way the sources do not describe as a collision (crushed, pinned, burned) |
| `fatality` | a person died |
| `fire` | the machine caught fire or exploded |
| `near_miss` | no contact, but a documented dangerous situation |
| `entrapment` | a person was trapped or pinned by the machine |
| `runaway` | the machine left its area or moved without control |
| `property_damage` | damage to property with no collision described |
| `recall` | the case is a recall notice |
| `investigation` | the case is a regulator's investigation |
| `lawsuit` | the case is a court filing |
| `settlement` | the case is a settlement |
| `fine` | the case is a fine or penalty |
| `citation` | the case is a regulator's citation |

### `severity` (closed set, ordered)

The worst outcome to a person the sources establish. `no_harm` < `property_damage` < `minor_injury` < `serious_injury` < `fatality`. Minor: treated at the scene or outpatient. Serious: hospitalised, or an injury the sources call serious, critical or life-changing. If the sources say "injured" without detail, code `minor_injury`. Never upgrade on speculation. Severity in NHTSA-origin rows follows the operator's own label (minor or serious with or without hospitalisation, fatality).

### `environment` (closed set)

Where the machine was operating: `street` (roads, sidewalks, parking, public space outdoors), `factory`, `warehouse`, `home`, `hospital`, `retail`, `venue` (events, sports halls, exhibitions, gyms), `other`.

### `escalation_stage` and `stage_evidence`

The furthest point the consequences reached, as recorded on the timeline. The stages, from least to most consequential: `report`, `follow_up`, `investigation`, `regulator`, `recall`, `fine`, `lawsuit`, `settlement`, `criminal_charge`. A stage is `document` when established by a regulator or court document linked to the case, otherwise `press`. A tabloid saying a company "was fined" does not set the stage to fine; a regulator's notice does.

### `title` and `summary`

One factual sentence, then two to four factual sentences, every one traceable to a source. No adjectives of judgement. Written in English whatever the language of the sources. Company names as the company writes them, places in their usual English spelling.

Names of private individuals never appear: victims, patients, drivers, workers, relatives, witnesses. Officials, spokespeople and company representatives may be named when their role is stated. This rule is enforced by code after writing (`strip_private_names` in the tmr-gates package) and again by a human when a leak is found; a case page records the stripping in its audit trail.

### `disputed`

True when a named company has used the right of reply and the dispute is published on the case page. The mark follows the evidence, not the request: the re-verification runs the same gates on the same sources.

## Sources and tiers

Every source carries its tier at the time of publication. Tier 1: wire agencies, national outlets, public broadcasters, regulators, courts. Tier 2: every other outlet that does its own reporting, including unknown regional papers. Tier 3: social networks, blogs, tabloids, content farms and syndication portals; never counted as corroboration. The lists are published in [tmr-gates](https://github.com/vzolot/tmr-gates). `counted_independent` marks the sources that counted toward the two-domain rule when the case was published.

## Publication gates

A case publishes only when every rule in the [tmr-gates](https://github.com/vzolot/tmr-gates) package passes: same event across sources, two independent domains with at least one at tier 1 or 2, three sources with a tier 1 for a death or serious injury attributed to a named company, no material disagreement, verification score at or above 0.80 and risk score at or below 0.35, no blocking flag from the adversarial pass, dates sane. Court records have their own thresholds. The README of that package documents each rule with its threshold.

## For a second annotator

To double-code a case: open the case page, read every linked source, and assign every field above from the sources alone, without reading the register's own values first. Record disagreements per field. Severity, incident type and category are the fields the inter-rater study will report Cohen's kappa on.
