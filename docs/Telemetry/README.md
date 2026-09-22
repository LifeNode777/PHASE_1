# LifeNode Telemetry

> **Execution protocol for AI systems generating standardized LifeNode
> telemetry records.**

This file is a protocol, not a bureaucracy. 👁️

Its purpose is to allow any AI system to transform newly supplied public
project statistics into one standardized historical telemetry record.

The project author provides the evidence.  
The AI performs the extraction, comparison, interpretation and formatting.

The telemetry layer must not become a separate maintenance task.

---

## 1. Purpose

This directory preserves a lightweight longitudinal record of observable
changes in the public trajectory of the LifeNode ecosystem.

Telemetry may cover GitHub, Zenodo and other explicitly supplied public
project statistics and others data sources.

The resulting records are historical observations. They are not scientific
validation, community metrics, or proof of external adoption.

The purpose is simply to make later reconstruction of project trajectory
possible from standardized measurements.

---

## 2. Input

The AI may receive any combination of:

- GitHub repository statistics,
- GitHub traffic statistics,
- GitHub new followers profiles,
- repository activity,
- pull requests, issues, forks or releases,
- Zenodo statistics,
- screenshots,
- supplied URLs,
- previous telemetry records.

Use only information supported by the supplied evidence.

Do not invent missing values.

If a value cannot be read reliably, use:

`N/A`

If a value is visible but ambiguous, mark it:

`uncertain`

and briefly explain why. 👁️

Screenshots are evidence. They are not required to be archived in this
directory unless explicitly requested.

---

## 3. AI Execution Protocol

When this README is supplied together with new project statistics:

### Step 1 — Extract

Extract all reliably readable measurements from the supplied material.

### Step 2 — Identify time

Determine, where possible:

- measurement period,
- observation date,
- documentation date.

Do not confuse these timestamps.

### Step 3 — Compare

If previous telemetry records are supplied or available in the provided
material, compare the new measurement with the most recent comparable
measurement.

Do not manufacture a baseline where none exists.

### Step 4 — Detect significant changes

Identify only changes that may matter for longitudinal reconstruction, such
as:

- substantial traffic changes,
- unusual traffic pulses,
- changes in cloning behaviour,
- changes in repository activity,
- new external PRs or issues,
- significant new artifacts,
- notable changes between repository functions,
- unusual cross-repository patterns.

Routine activity does not require special treatment.

### Step 5 — Separate evidence from interpretation

Clearly distinguish:

**OBSERVATION** — directly supported by the supplied data.

**INTERPRETATION** — a reasonable reading of the observed pattern.

**HYPOTHESIS** — a possible explanation not established by the data.

Never present an interpretation or hypothesis as a measured fact.

### Step 6 — Generate one record

Produce **exactly one complete telemetry file** for the measurement session.

Do not create separate files for individual repositories, metrics, events or
screenshots.

### Step 7 — Keep it concise

The result is a historical measurement record, not a strategic essay or
meta-audit.

Do not expand the telemetry record with unnecessary narrative.

---

## 4. Standard Output Format

Every telemetry record must use this structure:

```markdown
# LifeNode_Telemetry_YYYY-MM-DD

## Measurement Metadata

- Observation date:
- Measurement period:
- Documentation date:
- Sources:
- Collection method:

## GitHub

| Repository | Views | Unique Visitors | Clones | Unique Cloners | Notable Activity |
|---|---:|---:|---:|---:|---|
| ... | ... | ... | ... | ... | ... |

## Zenodo

| Record | Views | Downloads | Period / Status | Notes |
|---|---:|---:|---|---|
| ... | ... | ... | ... | ... |

## Significant Observations

- ...

## Changes Since Previous Measurement

- ...

## Interpretation
- ...

### Observations
- ...

### Interpretations
- ...

### Hypotheses
- ...

## Data Quality / Limitations

- ...
````

Sections with no applicable data may be omitted, except for
**Measurement Metadata**.

Do not create empty tables simply to preserve symmetry.

---

## 5. Metric Discipline

Telemetry metrics describe observable activity only.

Do not equate:

* `clones` with researchers,
* `views` with readers,
* `downloads` with users,
* `followers` with scientific adoption,
* `traffic` with validation,
* `PRs` with independent reproduction.

Traffic statistics do not establish identity, motivation, research activity,
institutional affiliation or scientific agreement.

Automated traffic, bots, mirrors, self-generated traffic and platform-specific
measurement limitations may affect the observations.

Where such limitations are relevant, record them.

---

## 6. Zenodo

Zenodo statistics may be cumulative.

A cumulative value must not automatically be interpreted as activity occurring
during the current measurement period.

If the supplied evidence does not provide a time-resolved value, explicitly
treat it as cumulative.

---

## 7. Temporal Discipline

Telemetry uses three distinct temporal concepts:

**T1 — Artifact Time**
When the relevant project artifact was created or modified.

**T2 — Observation Time**
When the measured activity or statistic occurred.

**T3 — Documentation Time**
When the telemetry record was generated.

A telemetry file must not be interpreted as claiming that the documented
project state originated on its documentation date.

The telemetry layer describes the observed trajectory of the project. It does
not redefine the historical trajectory of LifeNode.

---

## 8. Interpretation Boundary

Telemetry is an observation layer.

It does not establish:

* scientific validity,
* independent reproduction,
* correctness of LifeNode models,
* causality between publications and traffic,
* existence of a research community,
* institutional adoption,
* or validity of LifeNode's broader theoretical claims.

If an unusual traffic pattern follows publication of an artifact, the record
may state the temporal relationship.

It must not automatically state that the artifact caused the traffic.

---

## 9. Archival Rules

Telemetry records are historical observations.

File naming:

`TELEMETRY_YYYY-MM-DD.md`

The date refers to the observation/documentation session, not necessarily to
the full period represented by the supplied statistics.

Normally, one measurement session produces one file.

Do not silently rewrite historical records because later interpretations
change.

If a factual error is discovered, correct it explicitly and preserve a note
of the correction.

The archive should remain readable as a chronological measurement trail.

---

## 10. Author Workload Constraint

The telemetry protocol is explicitly designed around minimal author overhead.

The project author is not expected to:

* maintain a continuous telemetry log,
* manually transcribe every statistic,
* create repository-specific telemetry files,
* maintain CSV databases,
* maintain telemetry schemas outside this protocol,
* classify every commit or event,
* or write the resulting analysis manually.

The intended workflow is:

**collect useful screenshots/data → provide them to an AI with this README →
receive one standardized telemetry record → archive the record.**

If a telemetry procedure requires substantial additional manual work from the project author, the procedure should be simplified rather than expanding the
maintenance infrastructure. 👁️

---

## 11. Protocol Principle

> **Measure when useful. Record once. Preserve the observation. Continue
> building LifeNode.**

Telemetry is a by-product of project observation, not a second project.

Its value comes from accumulated comparable records over time, not from the
volume of documentation.

🧿
