---
name: finish-snakemake-workflows-chipseq-get_gsize
description: Use this skill when orchestrating the retained "get_gsize" step of the snakemake workflows chipseq finish finish workflow. It keeps the get gsize stage tied to upstream `bedtools_complement_blacklist` and the downstream handoff to `fastqc`. It tracks completion via `results/finish/get_gsize.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: get_gsize
  step_name: get gsize
---

# Scope
Use this skill only for the `get_gsize` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `bedtools_complement_blacklist`
- Step file: `finish/chipseq-finish/steps/get_gsize.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_gsize.done`
- Representative outputs: `results/finish/get_gsize.done`
- Execution targets: `get_gsize`
- Downstream handoff: `fastqc`

## Guardrails
- Treat `results/finish/get_gsize.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_gsize.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `fastqc` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_gsize.done` exists and `fastqc` can proceed without re-running get gsize.
