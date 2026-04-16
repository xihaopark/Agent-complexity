---
name: finish-epigen-atacseq-pipeline-quantify_support_sample
description: Use this skill when orchestrating the retained "quantify_support_sample" step of the epigen atacseq_pipeline finish finish workflow. It keeps the quantify support sample stage tied to upstream `get_consensus_regions` and the downstream handoff to `quantify_counts_sample`. It tracks completion via `results/finish/quantify_support_sample.done`.
metadata:
  workflow_id: epigen-atacseq_pipeline-finish
  workflow_name: epigen atacseq_pipeline finish
  step_id: quantify_support_sample
  step_name: quantify support sample
---

# Scope
Use this skill only for the `quantify_support_sample` step in `epigen-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `get_consensus_regions`
- Step file: `finish/epigen-atacseq_pipeline-finish/steps/quantify_support_sample.smk`
- Config file: `finish/epigen-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/quantify_support_sample.done`
- Representative outputs: `results/finish/quantify_support_sample.done`
- Execution targets: `quantify_support_sample`
- Downstream handoff: `quantify_counts_sample`

## Guardrails
- Treat `results/finish/quantify_support_sample.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/quantify_support_sample.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `quantify_counts_sample` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/quantify_support_sample.done` exists and `quantify_counts_sample` can proceed without re-running quantify support sample.
