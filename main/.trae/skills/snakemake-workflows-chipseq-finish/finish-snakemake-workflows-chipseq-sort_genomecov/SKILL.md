---
name: finish-snakemake-workflows-chipseq-sort_genomecov
description: Use this skill when orchestrating the retained "sort_genomecov" step of the snakemake workflows chipseq finish finish workflow. It keeps the sort genomecov stage tied to upstream `genomecov` and the downstream handoff to `bedGraphToBigWig`. It tracks completion via `results/finish/sort_genomecov.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: sort_genomecov
  step_name: sort genomecov
---

# Scope
Use this skill only for the `sort_genomecov` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `genomecov`
- Step file: `finish/chipseq-finish/steps/sort_genomecov.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/sort_genomecov.done`
- Representative outputs: `results/finish/sort_genomecov.done`
- Execution targets: `sort_genomecov`
- Downstream handoff: `bedGraphToBigWig`

## Guardrails
- Treat `results/finish/sort_genomecov.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/sort_genomecov.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bedGraphToBigWig` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/sort_genomecov.done` exists and `bedGraphToBigWig` can proceed without re-running sort genomecov.
