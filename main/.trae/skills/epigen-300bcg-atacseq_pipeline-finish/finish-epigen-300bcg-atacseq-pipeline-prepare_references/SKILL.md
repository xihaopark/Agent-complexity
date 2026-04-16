---
name: finish-epigen-300bcg-atacseq-pipeline-prepare_references
description: Use this skill when orchestrating the retained "prepare_references" step of the epigen 300bcg atacseq_pipeline finish finish workflow. It keeps the Prepare References stage and the downstream handoff to `parse_regulatory_build`. It tracks completion via `results/finish/prepare_references.done`.
metadata:
  workflow_id: epigen-300bcg-atacseq_pipeline-finish
  workflow_name: epigen 300bcg atacseq_pipeline finish
  step_id: prepare_references
  step_name: Prepare References
---

# Scope
Use this skill only for the `prepare_references` step in `epigen-300bcg-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/epigen-300bcg-atacseq_pipeline-finish/steps/prepare_references.smk`
- Config file: `finish/epigen-300bcg-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/prepare_references.done`
- Representative outputs: `results/finish/prepare_references.done`
- Execution targets: `prepare_references`
- Downstream handoff: `parse_regulatory_build`

## Guardrails
- Treat `results/finish/prepare_references.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/prepare_references.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `parse_regulatory_build` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/prepare_references.done` exists and `parse_regulatory_build` can proceed without re-running Prepare References.
