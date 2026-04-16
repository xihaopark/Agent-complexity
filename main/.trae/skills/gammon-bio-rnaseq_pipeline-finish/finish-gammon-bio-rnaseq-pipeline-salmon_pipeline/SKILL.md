---
name: finish-gammon-bio-rnaseq-pipeline-salmon_pipeline
description: Use this skill when orchestrating the retained "salmon_pipeline" step of the gammon bio rnaseq_pipeline finish finish workflow. It keeps the Salmon Pipeline stage tied to upstream `rename_fastqs` and the downstream handoff to `run_deseq2`. It tracks completion via `results/finish/salmon_pipeline.done`.
metadata:
  workflow_id: gammon-bio-rnaseq_pipeline-finish
  workflow_name: gammon bio rnaseq_pipeline finish
  step_id: salmon_pipeline
  step_name: Salmon Pipeline
---

# Scope
Use this skill only for the `salmon_pipeline` step in `gammon-bio-rnaseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `rename_fastqs`
- Step file: `finish/gammon-bio-rnaseq_pipeline-finish/steps/salmon_pipeline.smk`
- Config file: `finish/gammon-bio-rnaseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/salmon_pipeline.done`
- Representative outputs: `results/finish/salmon_pipeline.done`
- Execution targets: `salmon_pipeline`
- Downstream handoff: `run_deseq2`

## Guardrails
- Treat `results/finish/salmon_pipeline.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/salmon_pipeline.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `run_deseq2` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/salmon_pipeline.done` exists and `run_deseq2` can proceed without re-running Salmon Pipeline.
