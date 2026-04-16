---
name: finish-epigen-atacseq-pipeline-get_promoter_regions
description: Use this skill when orchestrating the retained "get_promoter_regions" step of the epigen atacseq_pipeline finish finish workflow. It keeps the get promoter regions stage tied to upstream `sample_annotation` and the downstream handoff to `get_consensus_regions`. It tracks completion via `results/finish/get_promoter_regions.done`.
metadata:
  workflow_id: epigen-atacseq_pipeline-finish
  workflow_name: epigen atacseq_pipeline finish
  step_id: get_promoter_regions
  step_name: get promoter regions
---

# Scope
Use this skill only for the `get_promoter_regions` step in `epigen-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `sample_annotation`
- Step file: `finish/epigen-atacseq_pipeline-finish/steps/get_promoter_regions.smk`
- Config file: `finish/epigen-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_promoter_regions.done`
- Representative outputs: `results/finish/get_promoter_regions.done`
- Execution targets: `get_promoter_regions`
- Downstream handoff: `get_consensus_regions`

## Guardrails
- Treat `results/finish/get_promoter_regions.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_promoter_regions.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_consensus_regions` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_promoter_regions.done` exists and `get_consensus_regions` can proceed without re-running get promoter regions.
