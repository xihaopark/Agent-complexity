---
name: finish-snakemake-workflows-chipseq-genomecov
description: Use this skill when orchestrating the retained "genomecov" step of the snakemake workflows chipseq finish finish workflow. It keeps the genomecov stage tied to upstream `collect_multiple_metrics` and the downstream handoff to `sort_genomecov`. It tracks completion via `results/finish/genomecov.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: genomecov
  step_name: genomecov
---

# Scope
Use this skill only for the `genomecov` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `collect_multiple_metrics`
- Step file: `finish/chipseq-finish/steps/genomecov.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/genomecov.done`
- Representative outputs: `results/finish/genomecov.done`
- Execution targets: `genomecov`
- Downstream handoff: `sort_genomecov`

## Guardrails
- Treat `results/finish/genomecov.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/genomecov.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `sort_genomecov` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/genomecov.done` exists and `sort_genomecov` can proceed without re-running genomecov.
