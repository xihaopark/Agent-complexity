---
name: finish-epigen-atacseq-pipeline-quantify_counts_sample
description: Use this skill when orchestrating the retained "quantify_counts_sample" step of the epigen atacseq_pipeline finish finish workflow. It keeps the quantify counts sample stage tied to upstream `quantify_support_sample` and the downstream handoff to `quantify_aggregate`. It tracks completion via `results/finish/quantify_counts_sample.done`.
metadata:
  workflow_id: epigen-atacseq_pipeline-finish
  workflow_name: epigen atacseq_pipeline finish
  step_id: quantify_counts_sample
  step_name: quantify counts sample
---

# Scope
Use this skill only for the `quantify_counts_sample` step in `epigen-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `quantify_support_sample`
- Step file: `finish/epigen-atacseq_pipeline-finish/steps/quantify_counts_sample.smk`
- Config file: `finish/epigen-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/quantify_counts_sample.done`
- Representative outputs: `results/finish/quantify_counts_sample.done`
- Execution targets: `quantify_counts_sample`
- Downstream handoff: `quantify_aggregate`

## Guardrails
- Treat `results/finish/quantify_counts_sample.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/quantify_counts_sample.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `quantify_aggregate` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/quantify_counts_sample.done` exists and `quantify_aggregate` can proceed without re-running quantify counts sample.
