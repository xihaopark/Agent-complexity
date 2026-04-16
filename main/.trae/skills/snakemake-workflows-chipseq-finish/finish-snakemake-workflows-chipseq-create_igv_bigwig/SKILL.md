---
name: finish-snakemake-workflows-chipseq-create_igv_bigwig
description: Use this skill when orchestrating the retained "create_igv_bigwig" step of the snakemake workflows chipseq finish finish workflow. It keeps the create igv bigwig stage tied to upstream `bedGraphToBigWig` and the downstream handoff to `compute_matrix`. It tracks completion via `results/finish/create_igv_bigwig.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: create_igv_bigwig
  step_name: create igv bigwig
---

# Scope
Use this skill only for the `create_igv_bigwig` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `bedGraphToBigWig`
- Step file: `finish/chipseq-finish/steps/create_igv_bigwig.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/create_igv_bigwig.done`
- Representative outputs: `results/finish/create_igv_bigwig.done`
- Execution targets: `create_igv_bigwig`
- Downstream handoff: `compute_matrix`

## Guardrails
- Treat `results/finish/create_igv_bigwig.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/create_igv_bigwig.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `compute_matrix` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/create_igv_bigwig.done` exists and `compute_matrix` can proceed without re-running create igv bigwig.
