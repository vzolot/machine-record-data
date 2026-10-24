# Inter-rater pilot, October 2026: the register against a blind second model

**What this is.** The dataset's labels (severity, incident type, category, environment, escalation stage) are assigned by a language model under the rules in [ANNOTATION_GUIDELINES.md](../ANNOTATION_GUIDELINES.md) and then gated by code. Nobody had measured how reproducible those labels are. The planned answer is a human second annotator and Cohen's kappa. This pilot is the dry run for that study with a different language model in the human's seat: `claude-opus-5-5` read the sources of 79 cases under the same guidelines, blind to the register's values, and coded every field. The production model is `claude-sonnet-4-6`. Agreement between two models reading the same rules is not inter-rater reliability in the human sense; it is a floor on how ambiguous the rules are and a list of where they bend. The human study follows with the same sample, the same form (`2026-10-model-pilot.csv`) and the same script (`scripts/kappa.py`).

**Sample.** Stratified by origin and severity, seeded (20261024), drawn from the 284 cases published on 24 October 2026: twelve press cases per severity level, and nineteen cases created from regulator documents (NHTSA, OSHA, CPSC). A candidate entered the sample only if at least 600 characters of its sources could be read; the EU Safety Gate stratum dropped out because those pages do not render without JavaScript. Sources were fetched live, from the Internet Archive copy when the page was gone, and from the stored excerpt when both failed; 46 of the 288 linked sources could not be read at all, so the second annotator saw less than the register did for some cases, which depresses agreement on dates and companies in particular.

**Headline.** Category is almost perfect (kappa 0.83), severity and incident type are substantial (0.73 and 0.64; linear weighted kappa for severity 0.80), environment and escalation stage are moderate (0.54 and 0.57). Press cases and document cases behave differently, and most of the moderate scores come from gaps in the rules rather than from disagreement about what happened. Each of those gaps is now written into the guidelines or fixed in the data; the list is below.

## Sample and sources
Date: 2026-10-24. Second annotator: `claude-opus-5-5` reading the sources of each case under ANNOTATION_GUIDELINES.md, blind to the register's values. The register's values were produced by `claude-sonnet-4-6` under the production prompt and then gated by rules. This is a model-versus-model pilot; it measures how far the written rules alone reproduce the register's labels. It is not the human inter-rater study the dataset still owes its users.

Cases coded: 79 (60 from press, 19 from regulator documents). Sources read: 242 (186 live pages, 56 archived copies, 0 stored excerpts only).

Strata: cpsc/no_harm 2, news/fatality 12, news/minor_injury 12, news/no_harm 12, news/property_damage 12, news/serious_injury 12, nhtsa/fatality 2, nhtsa/minor_injury 5, nhtsa/serious_injury 5, osha/fatality 2, osha/serious_injury 3

## All cases

| Field | n | Agreement | Kappa | Weighted kappa | Reading |
|---|---|---|---|---|---|
| `severity` | 79 | 78% | 0.73 | 0.80 | substantial |
| `incident_type` | 79 | 71% | 0.64 |  | substantial |
| `category` | 79 | 86% | 0.83 |  | almost perfect |
| `environment` | 79 | 63% | 0.54 |  | moderate |
| `escalation_stage` | 79 | 71% | 0.57 | 0.66 | moderate |

## Press cases only

| Field | n | Agreement | Kappa | Weighted kappa | Reading |
|---|---|---|---|---|---|
| `severity` | 60 | 75% | 0.69 | 0.77 | substantial |
| `incident_type` | 60 | 73% | 0.68 |  | substantial |
| `category` | 60 | 88% | 0.86 |  | almost perfect |
| `environment` | 60 | 82% | 0.76 |  | substantial |
| `escalation_stage` | 60 | 67% | 0.51 | 0.64 | moderate |

## Regulator-document cases only

| Field | n | Agreement | Kappa | Weighted kappa | Reading |
|---|---|---|---|---|---|
| `severity` | 19 | 89% | 0.85 | 0.85 | almost perfect |
| `incident_type` | 19 | 63% | 0.34 |  | fair |
| `category` | 19 | 79% | 0.63 |  | substantial |
| `environment` | 19 | 5% | 0.05 |  | slight |
| `escalation_stage` | 19 | 84% | 0.74 | 0.75 | substantial |

Kappa reading follows Landis and Koch: below 0.20 slight, 0.21 to 0.40 fair, 0.41 to 0.60 moderate, 0.61 to 0.80 substantial, above 0.80 almost perfect. Weighted kappa (linear) is given for the two ordered scales, severity and escalation stage, where a one-step disagreement counts less than a two-step one.

## Open fields

- Month of incident agrees in 48 of 79 cases; exact day in 38.
- Company agrees in 46 of 79 cases (case-insensitive, punctuation ignored).
- The second annotator judged 2 case(s) out of scope: TMR-0894, TMR-0141.

## Most frequent disagreements

| Field | Register | Second annotator | Cases |
|---|---|---|---|
| `environment` | empty | street | 12 |
| `escalation_stage` | follow_up | report | 7 |
| `severity` | serious_injury | minor_injury | 5 |
| `environment` | other | venue | 5 |
| `environment` | empty | factory | 5 |
| `severity` | property_damage | no_harm | 4 |
| `category` | industrial | robot_arm | 4 |
| `escalation_stage` | report | lawsuit | 3 |
| `escalation_stage` | follow_up | investigation | 3 |
| `escalation_stage` | report | regulator | 3 |
| `escalation_stage` | report | recall | 3 |
| `severity` | minor_injury | no_harm | 3 |
| `incident_type` | recall | collision | 3 |
| `incident_type` | investigation | collision | 3 |
| `incident_type` | lawsuit | fatality | 2 |


## What the disagreements were

Read with the tables in mind: 79 cases is enough to see patterns, not to put a second decimal on a kappa.

1. **Empty environment on regulator rows (17 cases).** The register had no environment for any NHTSA or OSHA case; the second annotator wrote `street` and `factory`. Not a disagreement about facts: the field was never filled for those origins. Fixed: all 54 NHTSA cases now carry `street`, and the guidelines say so. OSHA rows stay empty until a human reads each inspection record, because a palletiser can stand in a warehouse.
2. **`other` where `venue` applies (5 cases).** Stage shows, a festival, a race and an exhibition were coded `other` before `venue` existed in the vocabulary. Fixed in the data.
3. **Procedural incident types on document rows (7 cases).** The register codes an OSHA inspection as `investigation` and an NHTSA filing as `collision`; the second annotator coded the underlying event (`fatality`). The guidelines said both things. They now say: a row created from a regulator document carries the type of that document, and the harm is in severity.
4. **Severity one step lower in the second reading (12 of the 17 severity disagreements).** Five lawsuits where the complaint alleges a serious injury and the register coded what was alleged; the second annotator coded conservatively because a complaint establishes nothing. Three recalls after fires with no damage beyond the unit, coded `property_damage` by the register and `no_harm` by the second annotator. The rules now state the convention for both: a case built on a court filing takes the severity the filing alleges, and a unit catching fire is property damage only when something other than the unit was damaged. The three recall cases are referred for a human read under the new wording.
5. **`follow_up` versus `report` (7 cases).** The register sets `follow_up` when a later source added facts to the timeline; the second annotator could not see the timeline and saw one story. The guidelines now define the stage from the timeline rather than from any one article.
6. **`industrial` versus `robot_arm` (4 cases).** The register's rule-based normalisation prefers `industrial` for a factory incident unless the arm is named; the second annotator read "robot" in a factory as an arm. Left as is; the codebook definitions are the tiebreak and favour the register.
7. **Dates (31 of 79 months differ).** In 20 of those the second annotator returned no date, mostly because the article body it read did not carry one or the readable source was a docket page. Three are real conflicts between register and sources and are referred for review (TMR-0892, TMR-0173, TMR-0245), one was a plain error now fixed (TMR-0024, the Volkswagen Baunatal accident was on 29 June 2015, not 1 July), and two cases carried a year-only date recorded with day precision (TMR-0021, TMR-0139); the schema gained a `year` value for `date_precision` and both now carry it.
8. **Companies (33 differ, 7 of them formatting).** `Waymo` against `Waymo LLC` and `Unitree` against `Unitree Robotics` are the same company; the public CSV keeps the register's spelling. Twelve are the second annotator naming the operator or employer where the rules say maker; the register is right by its own rule there. Four were a maker named in every source and missing from the register (Zoox, Waymo and twice Intuitive Surgical), now filled. Two were substantive and were decided by the editor: TMR-0139 (and its sibling row TMR-0021), where the robot at a Tesla plant was made by KUKA and the rules say maker, now carry KUKA; TMR-0143, where a Tesla in autonomous mode destroyed a Promobot and the register named the victim's maker rather than the striking machine's, now carries Tesla.
9. **Two cases judged out of scope by the second annotator.** TMR-0141, where the headline says malfunction and the readable body describes none, was withdrawn by the editor on the same day; the withdrawal is listed on the register's corrections page. TMR-0894 was coded from a docket whose text the pilot could not fetch; the register read the filing itself, so this is a limit of the pilot, not of the case.

## Changes made on 24 October 2026

- Data: `environment = street` on 54 NHTSA cases; `environment = venue` on TMR-0035, TMR-0125, TMR-0131, TMR-0141, TMR-0217; company filled on TMR-0153 (Waymo), TMR-0224 and TMR-0245 (Intuitive Surgical), TMR-0229 (Zoox); date of TMR-0024 corrected to 2015-06-29. Each change is in the case's audit trail as `irr_pilot_fix`.
- Guidelines: conventions added for incident type on document rows, for severity in lawsuit-built cases and fire recalls, for `follow_up`, and for environment on SGO rows.
- Decided by the editor the same day: TMR-0141 withdrawn; TMR-0021 and TMR-0139 given `year` precision and the maker KUKA; TMR-0143 given Tesla as the responsible company.
- Still referred for a human read: TMR-0892, TMR-0173, TMR-0245 (dates); TMR-0050, TMR-0170, TMR-0205 (severity of fire recalls).

## What this pilot cannot tell you

- Two models trained on overlapping text agree for reasons a human would not share. A human study can come out lower on every field.
- The second annotator read what could be fetched in October 2026, not what the register read when it published; 46 sources were unreadable and some pages had changed.
- Nineteen document cases is too few for the per-origin kappas to be stable; read those rows as direction only.
- Kappa is computed on the register's values before the fixes above. Rerunning the script on today's data would flatter the register by exactly the corrections the pilot itself produced.

## Reproducing

```
python3 scripts/kappa.py irr/2026-10-model-pilot.csv
python3 scripts/kappa.py irr/2026-10-model-pilot.csv --origin news
```

The CSV holds one row per case and field with both codings. The annotator's prompt was the guidelines file verbatim plus the source texts; the sampling and scoring code lives in the register's pipeline repository and will be released with the human study.

## Every disagreement

| Case | Field | Register | Second annotator | Annotator's note |
|---|---|---|---|---|
| TMR-0169 | `category` | robot_arm | industrial | The only source has no usable body text: just a headline and standfirst saying a Co Armagh firm was fined £50,000 after an employee was killed by a falling robot. The incident date, the firm's name, the machine type and  |
| TMR-0169 | `environment` | factory | empty | The only source has no usable body text: just a headline and standfirst saying a Co Armagh firm was fined £50,000 after an employee was killed by a falling robot. The incident date, the firm's name, the machine type and  |
| TMR-0044 | `incident_type` | lawsuit | fatality | The robot's maker is not named, so the operator named in the lawsuit is recorded as the company. The lawsuit alleges medication errors, missed bleeding and a late transfer rather than a fault in the surgical robot, so sc |
| TMR-0044 | `escalation_stage` | report | lawsuit | The robot's maker is not named, so the operator named in the lawsuit is recorded as the company. The lawsuit alleges medication errors, missed bleeding and a late transfer rather than a fault in the surgical robot, so sc |
| TMR-0135 | `escalation_stage` | follow_up | investigation | The date comes from Asiae citing Goseong police (around 7:45 PM on the 7th) and is consistent with the 'Tuesday' in Koreaboo and Fox; BBC's 'Wednesday' conflicts. The robot's maker is not named, so the plant owner and op |
| TMR-0024 | `escalation_stage` | follow_up | investigation | Sources published Wednesday 1 July 2015 say the death occurred on Monday, so the date is taken as 2015-06-29. The robot's maker is not named, so Volkswagen, the plant owner named in every source, is recorded; one source  |
| TMR-0023 | `escalation_stage` | report | lawsuit | The day comes from the body's statement that the death fell on the 58th anniversary of the R.U.R. premiere, which matches the 'Jan. 25, 1979' headline. The robot's maker is not named, so the operator Ford is recorded. Th |
| TMR-0156 | `category` | industrial | other | The source dates the event only as 'Monday'; with publication on Tuesday 2022-05-17, this was resolved to 2022-05-16. The machine is an automated compacting 'robot dumpster', which fits no listed category, so it is coded |
| TMR-0892 | `severity` | fatality | minor_injury | The only source is a D. Mass. docket (personal injury / medical malpractice, filed 2026-03-20), so the date is the filing date; the date of the underlying surgery is not given and no robot model is named. Severity is min |
| TMR-0167 | `escalation_stage` | report | fine | The only source gives the court fine date (reported 2025-05-26) but not the date of the fatal accident, so the date is null and the case cannot publish; date_precision is a placeholder. The company named is the operator, |
| TMR-0891 | `incident_type` | lawsuit | fatality | The underlying event is the 25 April 2019 Key Largo crash of a 2019 Model S with Autopilot engaged, in which one person died and another was severely injured. I coded it as fatality rather than lawsuit because the record |
| TMR-0136 | `category` | other | industrial | The single source reports a worker death at Scott Technology's Dunedin robotics factory but never names the machine or says a robot or automated machine caused the death, so scope and the 'industrial' category are uncert |
| TMR-0100 | `severity` | serious_injury | no_harm | The lawsuits are undated, so the date used is the only dated event in the body: Intuitive's 8 May 2013 Urgent Medical Device Notification on micro-cracks in the Monopolar Curved Scissors. Burn injuries are only alleged b |
| TMR-0100 | `incident_type` | injury | lawsuit | The lawsuits are undated, so the date used is the only dated event in the body: Intuitive's 8 May 2013 Urgent Medical Device Notification on micro-cracks in the Monopolar Curved Scissors. Burn injuries are only alleged b |
| TMR-0100 | `escalation_stage` | report | lawsuit | The lawsuits are undated, so the date used is the only dated event in the body: Intuitive's 8 May 2013 Urgent Medical Device Notification on micro-cracks in the Monopolar Curved Scissors. Burn injuries are only alleged b |
| TMR-0224 | `incident_type` | lawsuit | settlement | The case was coded from the procedural act: the settlement was announced on the Wednesday before the 22 April 2016 post (20 April 2016), because the underlying 2009 hysterectomy has no day or month given. Serious injury  |
| TMR-0056 | `incident_type` | other | citation | The case stems from an FDA warning letter dated 2024-07-15, which follows a February to March 2024 inspection; I coded the warning letter as a citation at the regulator stage, but the evidence is press only since no FDA doc |
| TMR-0056 | `escalation_stage` | report | regulator | The case stems from an FDA warning letter dated 2024-07-15, which follows a February to March 2024 inspection; I coded the warning letter as a citation at the regulator stage, but the evidence is press only since no FDA doc |
| TMR-0104 | `severity` | serious_injury | minor_injury | The sources aggregate 14 separate Tesla Robotaxi crashes in Austin, which by the unit-of-analysis rule are separate events; this coding follows the most detailed one, the July 2025 2 mph right-turn collision with an SUV, |
| TMR-0104 | `escalation_stage` | follow_up | report | The sources aggregate 14 separate Tesla Robotaxi crashes in Austin, which by the unit-of-analysis rule are separate events; this coding follows the most detailed one, the July 2025 2 mph right-turn collision with an SUV, |
| TMR-0895 | `severity` | serious_injury | minor_injury | The only source is a D. Colorado docket (personal injury product liability, filed 2025-10-31 against E-Gym North America and YMCA of Greater Montgomery); the date recorded is the filing date because the underlying injury |
| TMR-0895 | `incident_type` | malfunction | lawsuit | The only source is a D. Colorado docket (personal injury product liability, filed 2025-10-31 against E-Gym North America and YMCA of Greater Montgomery); the date recorded is the filing date because the underlying injury |
| TMR-0245 | `severity` | serious_injury | minor_injury | The lawsuit says a piece of a da Vinci robot was left in the patient's abdomen during surgery at Legacy Emanuel Medical Center, causing months of severe pain and a second surgery to remove it. Severity is coded minor_inj |
| TMR-0144 | `category` | other | industrial | The source describes two separate injuries from remote-controlled demolition machines on Washington State construction sites, which by the unit-of-analysis rule may be two cases. Neither gives a date, and the 2019-06-03  |
| TMR-0144 | `environment` | factory | other | The source describes two separate injuries from remote-controlled demolition machines on Washington State construction sites, which by the unit-of-analysis rule may be two cases. Neither gives a date, and the 2019-06-03  |
| TMR-0144 | `escalation_stage` | report | investigation | The source describes two separate injuries from remote-controlled demolition machines on Washington State construction sites, which by the unit-of-analysis rule may be two cases. Neither gives a date, and the 2019-06-03  |
| TMR-0001 | `incident_type` | malfunction | injury | The date is derived from 'Wednesday' in an article published Thursday 2018-12-06. Injury was chosen over collision because harm came from fumes after the robot punctured a can, not from contact with a person; severity is |
| TMR-0001 | `escalation_stage` | follow_up | investigation | The date is derived from 'Wednesday' in an article published Thursday 2018-12-06. Injury was chosen over collision because harm came from fumes after the robot punctured a can, not from contact with a person; severity is |
| TMR-0151 | `category` | other | surgical | The source, a journal case report, gives no date and names no exoskeleton maker or model, so date and company are null and the case would fail the date gate. Category is surgical because a powered rehabilitation exoskele |
| TMR-0151 | `environment` | other | empty | The source, a journal case report, gives no date and names no exoskeleton maker or model, so date and company are null and the case would fail the date gate. Category is surgical because a powered rehabilitation exoskele |
| TMR-0894 | `severity` | serious_injury | no_harm | The only source is a CourtListener docket for a Federal Tort Claims Act medical-malpractice suit against the United States (VA claim exhibits), filed 2025-12-08. It does not mention any robot or automated machine, any ma |
| TMR-0894 | `category` | surgical | other | The only source is a CourtListener docket for a Federal Tort Claims Act medical-malpractice suit against the United States (VA claim exhibits), filed 2025-12-08. It does not mention any robot or automated machine, any ma |
| TMR-0894 | `environment` | hospital | empty | The only source is a CourtListener docket for a Federal Tort Claims Act medical-malpractice suit against the United States (VA claim exhibits), filed 2025-12-08. It does not mention any robot or automated machine, any ma |
| TMR-0021 | `severity` | serious_injury | minor_injury | The source dates the event only to 2021 with no month, so the date is null and the case would not publish under the date rule; date_precision is set to month only because the field requires a value. Severity is coded min |
| TMR-0139 | `severity` | serious_injury | minor_injury | Severity is coded minor_injury because the injury report records only a hand laceration with no time off work; NY Post and the AI-generated OECD summary call the injuries 'serious', but other sources do not. The sources  |
| TMR-0139 | `escalation_stage` | lawsuit | report | Severity is coded minor_injury because the injury report records only a hand laceration with no time off work; NY Post and the AI-generated OECD summary call the injuries 'serious', but other sources do not. The sources  |
| TMR-0053 | `escalation_stage` | report | recall | The case was created from Medtronic's European urgent field safety notice for Hugo surgeon-console power supply failures, coded as recall at the press level because no regulator document is linked. Severity is minor_inju |
| TMR-0012 | `environment` | other | street | The date comes from 'last September' in September 2024 articles, so it is coded as month precision for September 2023. Severity is minor_injury because the sources report a four-inch arm gash and lower back pain treated  |
| TMR-0012 | `escalation_stage` | follow_up | report | The date comes from 'last September' in September 2024 articles, so it is coded as month precision for September 2023. Severity is minor_injury because the sources report a four-inch arm gash and lower back pain treated  |
| TMR-0217 | `severity` | minor_injury | no_harm | The date comes from the article body, dated 2025-08-16, which says the race was 'yesterday'; this matches the 2025-08-15 listing date. The source says the H1 struck a person but does not establish any injury, so severity |
| TMR-0217 | `environment` | other | venue | The date comes from the article body, dated 2025-08-16, which says the race was 'yesterday'; this matches the 2025-08-15 listing date. The source says the H1 struck a person but does not establish any injury, so severity |
| TMR-0131 | `severity` | minor_injury | no_harm | The only explicit date (February 9) and the location (Tianjin) come from the Daily Mail, a tier-3 tabloid; The Conversation instead places the event at a lantern festival in Taishan, Guangdong, so location is disputed an |
| TMR-0131 | `incident_type` | injury | malfunction | The only explicit date (February 9) and the location (Tianjin) come from the Daily Mail, a tier-3 tabloid; The Conversation instead places the event at a lantern festival in Taishan, Guangdong, so location is disputed an |
| TMR-0131 | `environment` | other | venue | The only explicit date (February 9) and the location (Tianjin) come from the Daily Mail, a tier-3 tabloid; The Conversation instead places the event at a lantern festival in Taishan, Guangdong, so location is disputed an |
| TMR-0131 | `escalation_stage` | follow_up | report | The only explicit date (February 9) and the location (Tianjin) come from the Daily Mail, a tier-3 tabloid; The Conversation instead places the event at a lantern festival in Taishan, Guangdong, so location is disputed an |
| TMR-0214 | `incident_type` | recall | collision | Coded as collision rather than recall because the source describes the underlying June 3 crash, with the 80-vehicle software recall and the NHTSA investigation as later timeline events; the 'injury' code is excluded beca |
| TMR-0164 | `incident_type` | recall | collision | Sources 2-6 describe the May 8, 2025 San Francisco e-scooter collision and the 270-vehicle voluntary software recall that followed it. Source 1 (kcra.com) describes a separate April 4 cyclist collision at 11th and Bryant |
| TMR-0124 | `severity` | minor_injury | no_harm | The case is coded from the recall notice. The body gives no exact recall date, so it is recorded as March 2025 at month precision based on the publication; the two motorcycle rear-end collisions and NHTSA's May 2024 prel |
| TMR-0124 | `escalation_stage` | report | recall | The case is coded from the recall notice. The body gives no exact recall date, so it is recorded as March 2025 at month precision based on the publication; the two motorcycle rear-end collisions and NHTSA's May 2024 prel |
| TMR-0125 | `incident_type` | injury | collision | The only date in the body is the 2026-02-18 X post sharing the footage; the incident date itself is not stated, so it is left null. The kick is coded as a collision (the robot struck a person). Severity is minor_injury b |
| TMR-0125 | `environment` | other | venue | The only date in the body is the 2026-02-18 X post sharing the footage; the incident date itself is not stated, so it is left null. The kick is coded as a collision (the robot struck a person). Severity is minor_injury b |
| TMR-0035 | `severity` | property_damage | no_harm | Newsweek, Inc. and Geo give November 10 (Monday) at the Yarovit Hall Congress Center in Moscow, while United24 says November 11; the majority date was used. The robot shed pieces when it fell, but no person was harmed, s |
| TMR-0035 | `environment` | other | venue | Newsweek, Inc. and Geo give November 10 (Monday) at the Yarovit Hall Congress Center in Moscow, while United24 says November 11; the majority date was used. The robot shed pieces when it fell, but no person was harmed, s |
| TMR-0035 | `escalation_stage` | follow_up | report | Newsweek, Inc. and Geo give November 10 (Monday) at the Yarovit Hall Congress Center in Moscow, while United24 says November 11; the majority date was used. The robot shed pieces when it fell, but no person was harmed, s |
| TMR-0170 | `severity` | property_damage | no_harm | The case comes from a Health Canada recall of 2,606 Aiper Seagull Pro ZT6001 pool cleaners, prompted by one report of a unit catching fire while charging with no injuries or property damage, so it is coded as a recall ra |
| TMR-0170 | `environment` | home | empty | The case comes from a Health Canada recall of 2,606 Aiper Seagull Pro ZT6001 pool cleaners, prompted by one report of a unit catching fire while charging with no injuries or property damage, so it is coded as a recall ra |
| TMR-0170 | `escalation_stage` | report | recall | The case comes from a Health Canada recall of 2,606 Aiper Seagull Pro ZT6001 pool cleaners, prompted by one report of a unit catching fire while charging with no injuries or property damage, so it is coded as a recall ra |
| TMR-0205 | `severity` | property_damage | no_harm | The case is built on an OPSS safety recall of the Automower 435X and 535 after five undated fire incidents during charging. No injuries or described damage are reported, so severity is coded no_harm rather than property_ |
| TMR-0143 | `category` | service | autonomous_vehicle | Two robotic machines were involved: the striking Tesla Model S, reportedly in self-driving mode, and the struck Promobot v4 service robot, which had strayed into the roadway. I coded the striking vehicle and Tesla, but s |
| TMR-0229 | `incident_type` | recall | collision | The articles were prompted by the recall, but they describe the underlying April 8 collision in full, so I coded the collision under the priority order, with the recall of 270 vehicles as the escalation stage (press evid |
| TMR-0108 | `severity` | property_damage | no_harm | The incident date is not established: TechSpot calls the video undated, and the earliest dated reference is a tweet of 2 May 2025, so the date is left null and the case would not publish under the date gate. Malfunction  |
| TMR-0108 | `incident_type` | injury | malfunction | The incident date is not established: TechSpot calls the video undated, and the earliest dated reference is a tweet of 2 May 2025, so the date is left null and the case would not publish under the date gate. Malfunction  |
| TMR-0108 | `escalation_stage` | follow_up | report | The incident date is not established: TechSpot calls the video undated, and the earliest dated reference is a tweet of 2 May 2025, so the date is left null and the case would not publish under the date gate. Malfunction  |
| TMR-0159 | `escalation_stage` | follow_up | report | The sources cover two separate events: a Serve Robotics robot shattering a West Town bus shelter on Sunday, March 22, 2026, and a Coco Robotics robot shattering an Old Town shelter on March 24, 2026. Under the one-event  |
| TMR-0208 | `escalation_stage` | follow_up | report | No source gives the incident date: Sound of Hope reported it on 1 May 2025 as 'recent' and a 4 May post says 'last week', so it could fall in late April or 1 May; date left null, which means the case would not publish un |
| TMR-0199 | `incident_type` | other | malfunction | The robotaxi stalled across the road mid U-turn on West Sixth Street, Austin, and blocked an ATCEMS ambulance for about a minute until a police officer moved it. There was no contact, and EMS said response time was not a |
| TMR-0153 | `incident_type` | other | entrapment | The source gives only 'In January' (2026), so the date is coded to the first of the month. I chose entrapment over collision because the passengers were stuck in a stopped Waymo while a man punched the windows; an assaul |
| TMR-0141 | `environment` | other | venue | The headline mentions a malfunction, but the article body describes no malfunction, harm or regulatory action. It only reports a university presenting a commercially available Chinese robot dog as its own and being eject |
| TMR-0768 | `incident_type` | recall | malfunction | The underlying event was an unoccupied Zoox robotaxi in Las Vegas that failed to detect heavy smoke and entered an active fire scene, with no contact and no injuries reported, so it is coded malfunction rather than recal |
| TMR-0770 | `incident_type` | collision | fatality | The SGO filing gives only August 2026, so the first of the month is recorded. Fatality follows the operator's label: an SUV struck the pedestrian, who was thrown into the rear left of the yielding Waymo Jaguar I-PACE. Es |
| TMR-0770 | `environment` | empty | street | The SGO filing gives only August 2026, so the first of the month is recorded. Fatality follows the operator's label: an SUV struck the pedestrian, who was thrown into the rear left of the yielding Waymo Jaguar I-PACE. Es |
| TMR-0718 | `incident_type` | collision | fatality | Severity follows the operator's own NHTSA label (Fatality), although the narrative says the motorcyclist was struck by a hit-and-run passenger car after falling from the motorcycle that hit the Waymo AV. The stage is set |
| TMR-0718 | `environment` | empty | street | Severity follows the operator's own NHTSA label (Fatality), although the narrative says the motorcyclist was struck by a hit-and-run passenger car after falling from the motorcycle that hit the Waymo AV. The stage is set |
| TMR-0718 | `escalation_stage` | report | regulator | Severity follows the operator's own NHTSA label (Fatality), although the narrative says the motorcyclist was struck by a hit-and-run passenger car after falling from the motorcycle that hit the Waymo AV. The stage is set |
| TMR-0698 | `environment` | empty | street | Severity follows the operator's NHTSA label 'Moderate W/ Hospitalization', mapped to serious_injury as hospitalised; the narrative itself says one passenger had minor and one moderate injuries, both transported by ambula |
| TMR-0698 | `escalation_stage` | report | regulator | Severity follows the operator's NHTSA label 'Moderate W/ Hospitalization', mapped to serious_injury as hospitalised; the narrative itself says one passenger had minor and one moderate injuries, both transported by ambula |
| TMR-0771 | `environment` | empty | street | Severity follows the operator's NHTSA label 'Moderate W/ Hospitalization' (bus driver taken to hospital, injuries unknown); the stationary Waymo AV was struck by a bus, so the case is coded as a collision rather than an  |
| TMR-0772 | `environment` | empty | street | An SUV rear-ended a stationary Waymo Jaguar I-PACE (ADS engaged) in Atlanta, GA. The filing says 'the collision resulted in a fire' without saying which vehicle burned, so I coded collision rather than fire. Severity fol |
| TMR-0709 | `environment` | empty | street | The filing calls this a collision: the slowing AV's rear tire stopped on the foot of a passenger exiting mid-ride. Collision outranks entrapment even though the foot stayed pinned until emergency services lifted the car. |
| TMR-0683 | `environment` | empty | street | The operator's label 'Moderate W/ Hospitalization' (two passengers taken to hospital by ambulance) is coded serious_injury under the hospitalisation rule for NHTSA-origin rows. Escalation is kept at report because the SG |
| TMR-0888 | `environment` | empty | street | Severity follows Waymo's own NHTSA label 'Minor W/ Hospitalization', so it is coded minor_injury, not serious; the stopped Waymo AV was struck by an SUV deflected from a separate two-SUV crash. The stage is coded conserv |
| TMR-0690 | `environment` | empty | street | The operator labelled the injury 'Moderate W/O Hospitalization' and the narrative says the motorcyclist was treated at the scene, so it maps to minor_injury rather than serious. The escalation stage is report because the |
| TMR-0725 | `environment` | empty | street | The filing gives only the month (day redacted), so the date is recorded as the first of the month. Severity follows the operator's own 'Minor W/ Hospitalization' label under the NHTSA rule, even though the cyclist was ta |
| TMR-0717 | `environment` | empty | street | Severity follows the operator's NHTSA label 'Minor W/ Hospitalization' (coded minor_injury rather than serious, per the NHTSA-origin rule); the day is redacted, so the incident date is recorded at month precision. Escala |
| TMR-0686 | `environment` | empty | street | Severity follows the operator's NHTSA label 'Minor W/ Hospitalization', although the narrative says only 'unknown injuries'. Escalation is coded conservatively as 'report' because a mandatory SGO filing is not regulator  |
| TMR-0730 | `incident_type` | investigation | fatality | The company recorded is the establishment (operator/employer) named in the OSHA report; the robot's maker is not named. Coded robot_arm rather than cobot because the arm worked inside a sensor-guarded enclosure, and the  |
| TMR-0730 | `category` | industrial | robot_arm | The company recorded is the establishment (operator/employer) named in the OSHA report; the robot's maker is not named. Coded robot_arm rather than cobot because the arm worked inside a sensor-guarded enclosure, and the  |
| TMR-0730 | `environment` | empty | factory | The company recorded is the establishment (operator/employer) named in the OSHA report; the robot's maker is not named. Coded robot_arm rather than cobot because the arm worked inside a sensor-guarded enclosure, and the  |
| TMR-0746 | `incident_type` | investigation | fatality | Only an OSHA accident record exists: the inspection opened 2021-01-15 at employer Ambrose Sales Inc., the operator, and no citation or penalty appears, so the stage is investigation (document). The caged Okura palletizer |
| TMR-0746 | `category` | industrial | robot_arm | Only an OSHA accident record exists: the inspection opened 2021-01-15 at employer Ambrose Sales Inc., the operator, and no citation or penalty appears, so the stage is investigation (document). The caged Okura palletizer |
| TMR-0746 | `environment` | empty | factory | Only an OSHA accident record exists: the inspection opened 2021-01-15 at employer Ambrose Sales Inc., the operator, and no citation or penalty appears, so the stage is investigation (document). The caged Okura palletizer |
| TMR-0750 | `incident_type` | investigation | collision | The OSHA record describes a 'robot press machine' without saying whether it is a manipulator arm, so it is coded as industrial rather than robot_arm. The employee was struck in the head and hospitalised; because the sour |
| TMR-0750 | `environment` | empty | factory | The OSHA record describes a 'robot press machine' without saying whether it is a manipulator arm, so it is coded as industrial rather than robot_arm. The employee was struck in the head and hospitalised; because the sour |
| TMR-0750 | `escalation_stage` | investigation | regulator | The OSHA record describes a 'robot press machine' without saying whether it is a manipulator arm, so it is coded as industrial rather than robot_arm. The employee was struck in the head and hospitalised; because the sour |
| TMR-0753 | `incident_type` | investigation | collision | OSHA accident report: a caged palletizing robot arm restarted and struck a worker in the chest while he was reconnecting a loose hose, breaking his sternum and two ribs; he was hospitalised. The source describes a strike |
| TMR-0753 | `category` | industrial | robot_arm | OSHA accident report: a caged palletizing robot arm restarted and struck a worker in the chest while he was reconnecting a loose hose, breaking his sternum and two ribs; he was hospitalised. The source describes a strike |
| TMR-0753 | `environment` | empty | factory | OSHA accident report: a caged palletizing robot arm restarted and struck a worker in the chest while he was reconnecting a loose hose, breaking his sternum and two ribs; he was hospitalised. The source describes a strike |
| TMR-0752 | `incident_type` | investigation | collision | The OSHA record names only the employer and operator, Hwashin America Corporation, not the robot's maker, so the operator is recorded. The incident type is collision because the record says the arm struck the worker, and |
| TMR-0752 | `category` | industrial | robot_arm | The OSHA record names only the employer and operator, Hwashin America Corporation, not the robot's maker, so the operator is recorded. The incident type is collision because the record says the arm struck the worker, and |
| TMR-0752 | `environment` | empty | factory | The OSHA record names only the employer and operator, Hwashin America Corporation, not the robot's maker, so the operator is recorded. The incident type is collision because the record says the arm struck the worker, and |
| TMR-0183 | `severity` | no_harm | minor_injury | The case was created from the CPSC recall announced August 24, 2023 (date from Source 3's body), so incident_type is recall, and the stage rests on press reports because no CPSC filing was supplied. Severity is minor_inj |
| TMR-0183 | `environment` | empty | home | The case was created from the CPSC recall announced August 24, 2023 (date from Source 3's body), so incident_type is recall, and the stage rests on press reports because no CPSC filing was supplied. Severity is minor_inj |
| TMR-0050 | `severity` | no_harm | property_damage | The case is coded as a recall because it was created from the CPSC recall notice (No. 26-372), so the date is the recall date rather than the dates of the ten underlying overheating and fire reports, which the sources do |
