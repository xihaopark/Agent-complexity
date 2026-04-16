---
name: finish-epigen-atacseq-pipeline-align
description: Use this skill when orchestrating the retained "align" step of the epigen atacseq_pipeline finish finish workflow. It keeps the align stage tied to upstream `install_homer` and the downstream handoff to `tss_coverage`. It tracks completion via `results/finish/align.done`.
metadata:
  workflow_id: epigen-atacseq_pipeline-finish
  workflow_name: epigen atacseq_pipeline finish
  step_id: align
  step_name: align
---

# Scope
Use this skill only for the `align` step in `epigen-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `install_homer`
- Step file: `finish/epigen-atacseq_pipeline-finish/steps/align.smk`
- Config file: `finish/epigen-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/align.done`
- Representative outputs: `results/finish/align.done`
- Execution targets: `align`
- Downstream handoff: `tss_coverage`

## Guardrails
- Treat `results/finish/align.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/align.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `tss_coverage` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/align.done` exists and `tss_coverage` can proceed without re-running align.
