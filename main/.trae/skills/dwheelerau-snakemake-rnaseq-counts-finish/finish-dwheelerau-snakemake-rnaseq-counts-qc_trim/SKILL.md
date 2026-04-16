---
name: finish-dwheelerau-snakemake-rnaseq-counts-qc_trim
description: Use this skill when orchestrating the retained "qc_trim" step of the dwheelerau snakemake rnaseq counts finish finish workflow. It keeps the qc trim stage tied to upstream `make_index` and the downstream handoff to `aln`. It tracks completion via `results/finish/qc_trim.done`.
metadata:
  workflow_id: dwheelerau-snakemake-rnaseq-counts-finish
  workflow_name: dwheelerau snakemake rnaseq counts finish
  step_id: qc_trim
  step_name: qc trim
---

# Scope
Use this skill only for the `qc_trim` step in `dwheelerau-snakemake-rnaseq-counts-finish`.

## Orchestration
- Upstream requirements: `make_index`
- Step file: `finish/dwheelerau-snakemake-rnaseq-counts-finish/steps/qc_trim.smk`
- Config file: `finish/dwheelerau-snakemake-rnaseq-counts-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/qc_trim.done`
- Representative outputs: `results/finish/qc_trim.done`
- Execution targets: `qc_trim`
- Downstream handoff: `aln`

## Guardrails
- Treat `results/finish/qc_trim.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/qc_trim.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `aln` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/qc_trim.done` exists and `aln` can proceed without re-running qc trim.
