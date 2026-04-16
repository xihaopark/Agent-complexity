---
name: finish-snakemake-workflows-chipseq-create_deseq2_igv
description: Use this skill when orchestrating the retained "create_deseq2_igv" step of the snakemake workflows chipseq finish finish workflow. It keeps the create deseq2 igv stage tied to upstream `featurecounts_deseq2` and the downstream handoff to `all`. It tracks completion via `results/finish/create_deseq2_igv.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: create_deseq2_igv
  step_name: create deseq2 igv
---

# Scope
Use this skill only for the `create_deseq2_igv` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `featurecounts_deseq2`
- Step file: `finish/chipseq-finish/steps/create_deseq2_igv.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/create_deseq2_igv.done`
- Representative outputs: `results/finish/create_deseq2_igv.done`
- Execution targets: `create_deseq2_igv`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/create_deseq2_igv.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/create_deseq2_igv.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/create_deseq2_igv.done` exists and `all` can proceed without re-running create deseq2 igv.
