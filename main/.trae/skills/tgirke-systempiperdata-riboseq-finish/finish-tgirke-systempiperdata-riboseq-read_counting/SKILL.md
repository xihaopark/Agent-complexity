---
name: finish-tgirke-systempiperdata-riboseq-read_counting
description: Use this skill when orchestrating the retained "read_counting" step of the tgirke systempiperdata riboseq finish finish workflow. It keeps the read counting stage tied to upstream `coverage_nuc_level` and the downstream handoff to `sample_tree`. It tracks completion via `results/finish/read_counting.done`.
metadata:
  workflow_id: tgirke-systempiperdata-riboseq-finish
  workflow_name: tgirke systempiperdata riboseq finish
  step_id: read_counting
  step_name: read counting
---

# Scope
Use this skill only for the `read_counting` step in `tgirke-systempiperdata-riboseq-finish`.

## Orchestration
- Upstream requirements: `coverage_nuc_level`
- Step file: `finish/tgirke-systempiperdata-riboseq-finish/steps/read_counting.smk`
- Config file: `finish/tgirke-systempiperdata-riboseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/read_counting.done`
- Representative outputs: `results/finish/read_counting.done`
- Execution targets: `read_counting`
- Downstream handoff: `sample_tree`

## Guardrails
- Treat `results/finish/read_counting.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/read_counting.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `sample_tree` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/read_counting.done` exists and `sample_tree` can proceed without re-running read counting.
