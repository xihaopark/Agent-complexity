---
name: finish-gammon-bio-rnaseq-pipeline-run_deseq2
description: Use this skill when orchestrating the retained "run_deseq2" step of the gammon bio rnaseq_pipeline finish finish workflow. It keeps the Run DESeq2 stage tied to upstream `salmon_pipeline`. It tracks completion via `results/finish/run_deseq2.done`.
metadata:
  workflow_id: gammon-bio-rnaseq_pipeline-finish
  workflow_name: gammon bio rnaseq_pipeline finish
  step_id: run_deseq2
  step_name: Run DESeq2
---

# Scope
Use this skill only for the `run_deseq2` step in `gammon-bio-rnaseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `salmon_pipeline`
- Step file: `finish/gammon-bio-rnaseq_pipeline-finish/steps/run_deseq2.smk`
- Config file: `finish/gammon-bio-rnaseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/run_deseq2.done`
- Representative outputs: `results/finish/run_deseq2.done`
- Execution targets: `run_deseq2`
- Downstream handoff: none

## Guardrails
- Treat `results/finish/run_deseq2.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/run_deseq2.smk` so the step remains separable and replayable inside the finish workflow.

## Done Criteria
Mark this step complete only when `results/finish/run_deseq2.done` exists and matches the intended step boundary.
