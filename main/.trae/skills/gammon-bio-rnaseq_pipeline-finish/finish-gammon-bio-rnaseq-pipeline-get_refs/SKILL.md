---
name: finish-gammon-bio-rnaseq-pipeline-get_refs
description: Use this skill when orchestrating the retained "get_refs" step of the gammon bio rnaseq_pipeline finish finish workflow. It keeps the Get Refs stage and the downstream handoff to `rename_fastqs`. It tracks completion via `results/finish/get_refs.done`.
metadata:
  workflow_id: gammon-bio-rnaseq_pipeline-finish
  workflow_name: gammon bio rnaseq_pipeline finish
  step_id: get_refs
  step_name: Get Refs
---

# Scope
Use this skill only for the `get_refs` step in `gammon-bio-rnaseq_pipeline-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/gammon-bio-rnaseq_pipeline-finish/steps/get_refs.smk`
- Config file: `finish/gammon-bio-rnaseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_refs.done`
- Representative outputs: `results/finish/get_refs.done`
- Execution targets: `get_refs`
- Downstream handoff: `rename_fastqs`

## Guardrails
- Treat `results/finish/get_refs.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_refs.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `rename_fastqs` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_refs.done` exists and `rename_fastqs` can proceed without re-running Get Refs.
