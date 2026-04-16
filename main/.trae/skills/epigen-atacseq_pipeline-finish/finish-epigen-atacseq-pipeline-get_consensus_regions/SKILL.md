---
name: finish-epigen-atacseq-pipeline-get_consensus_regions
description: Use this skill when orchestrating the retained "get_consensus_regions" step of the epigen atacseq_pipeline finish finish workflow. It keeps the get consensus regions stage tied to upstream `get_promoter_regions` and the downstream handoff to `quantify_support_sample`. It tracks completion via `results/finish/get_consensus_regions.done`.
metadata:
  workflow_id: epigen-atacseq_pipeline-finish
  workflow_name: epigen atacseq_pipeline finish
  step_id: get_consensus_regions
  step_name: get consensus regions
---

# Scope
Use this skill only for the `get_consensus_regions` step in `epigen-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `get_promoter_regions`
- Step file: `finish/epigen-atacseq_pipeline-finish/steps/get_consensus_regions.smk`
- Config file: `finish/epigen-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_consensus_regions.done`
- Representative outputs: `results/finish/get_consensus_regions.done`
- Execution targets: `get_consensus_regions`
- Downstream handoff: `quantify_support_sample`

## Guardrails
- Treat `results/finish/get_consensus_regions.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_consensus_regions.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `quantify_support_sample` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_consensus_regions.done` exists and `quantify_support_sample` can proceed without re-running get consensus regions.
