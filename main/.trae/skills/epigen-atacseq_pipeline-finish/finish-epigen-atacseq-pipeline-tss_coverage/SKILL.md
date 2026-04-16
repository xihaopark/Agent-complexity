---
name: finish-epigen-atacseq-pipeline-tss_coverage
description: Use this skill when orchestrating the retained "tss_coverage" step of the epigen atacseq_pipeline finish finish workflow. It keeps the tss coverage stage tied to upstream `align` and the downstream handoff to `peak_calling`. It tracks completion via `results/finish/tss_coverage.done`.
metadata:
  workflow_id: epigen-atacseq_pipeline-finish
  workflow_name: epigen atacseq_pipeline finish
  step_id: tss_coverage
  step_name: tss coverage
---

# Scope
Use this skill only for the `tss_coverage` step in `epigen-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `align`
- Step file: `finish/epigen-atacseq_pipeline-finish/steps/tss_coverage.smk`
- Config file: `finish/epigen-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/tss_coverage.done`
- Representative outputs: `results/finish/tss_coverage.done`
- Execution targets: `tss_coverage`
- Downstream handoff: `peak_calling`

## Guardrails
- Treat `results/finish/tss_coverage.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/tss_coverage.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `peak_calling` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/tss_coverage.done` exists and `peak_calling` can proceed without re-running tss coverage.
