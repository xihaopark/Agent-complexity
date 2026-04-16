---
name: finish-snakemake-workflows-chipseq-all
description: Use this skill when orchestrating the retained "all" step of the snakemake workflows chipseq finish finish workflow. It keeps the all stage tied to upstream `create_deseq2_igv`. It tracks completion via `results/finish/all.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: all
  step_name: all
---

# Scope
Use this skill only for the `all` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `create_deseq2_igv`
- Step file: `finish/chipseq-finish/steps/all.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/all.done`
- Representative outputs: `results/finish/all.done`
- Execution targets: `all`
- Downstream handoff: none

## Guardrails
- Treat `results/finish/all.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/all.smk` so the step remains separable and replayable inside the finish workflow.

## Done Criteria
Mark this step complete only when `results/finish/all.done` exists and matches the intended step boundary.
