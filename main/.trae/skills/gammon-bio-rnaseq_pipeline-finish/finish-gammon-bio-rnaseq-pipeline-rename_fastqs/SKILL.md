---
name: finish-gammon-bio-rnaseq-pipeline-rename_fastqs
description: Use this skill when orchestrating the retained "rename_fastqs" step of the gammon bio rnaseq_pipeline finish finish workflow. It keeps the Rename Fastqs stage tied to upstream `get_refs` and the downstream handoff to `salmon_pipeline`. It tracks completion via `results/finish/rename_fastqs.done`.
metadata:
  workflow_id: gammon-bio-rnaseq_pipeline-finish
  workflow_name: gammon bio rnaseq_pipeline finish
  step_id: rename_fastqs
  step_name: Rename Fastqs
---

# Scope
Use this skill only for the `rename_fastqs` step in `gammon-bio-rnaseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `get_refs`
- Step file: `finish/gammon-bio-rnaseq_pipeline-finish/steps/rename_fastqs.smk`
- Config file: `finish/gammon-bio-rnaseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/rename_fastqs.done`
- Representative outputs: `results/finish/rename_fastqs.done`
- Execution targets: `rename_fastqs`
- Downstream handoff: `salmon_pipeline`

## Guardrails
- Treat `results/finish/rename_fastqs.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/rename_fastqs.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `salmon_pipeline` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/rename_fastqs.done` exists and `salmon_pipeline` can proceed without re-running Rename Fastqs.
