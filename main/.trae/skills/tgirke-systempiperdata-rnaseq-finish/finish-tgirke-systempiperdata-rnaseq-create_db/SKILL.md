---
name: finish-tgirke-systempiperdata-rnaseq-create_db
description: Use this skill when orchestrating the retained "create_db" step of the tgirke systempiperdata rnaseq finish finish workflow. It keeps the create db stage tied to upstream `bam_IGV` and the downstream handoff to `read_counting`. It tracks completion via `results/finish/create_db.done`.
metadata:
  workflow_id: tgirke-systempiperdata-rnaseq-finish
  workflow_name: tgirke systempiperdata rnaseq finish
  step_id: create_db
  step_name: create db
---

# Scope
Use this skill only for the `create_db` step in `tgirke-systempiperdata-rnaseq-finish`.

## Orchestration
- Upstream requirements: `bam_IGV`
- Step file: `finish/tgirke-systempiperdata-rnaseq-finish/steps/create_db.smk`
- Config file: `finish/tgirke-systempiperdata-rnaseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/create_db.done`
- Representative outputs: `results/finish/create_db.done`
- Execution targets: `create_db`
- Downstream handoff: `read_counting`

## Guardrails
- Treat `results/finish/create_db.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/create_db.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `read_counting` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/create_db.done` exists and `read_counting` can proceed without re-running create db.
