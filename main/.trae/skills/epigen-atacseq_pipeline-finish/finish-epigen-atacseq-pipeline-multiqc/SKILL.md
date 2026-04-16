---
name: finish-epigen-atacseq-pipeline-multiqc
description: Use this skill when orchestrating the retained "multiqc" step of the epigen atacseq_pipeline finish finish workflow. It keeps the multiqc stage tied to upstream `symlink_stats` and the downstream handoff to `plot_sample_annotation`. It tracks completion via `results/finish/multiqc.done`.
metadata:
  workflow_id: epigen-atacseq_pipeline-finish
  workflow_name: epigen atacseq_pipeline finish
  step_id: multiqc
  step_name: multiqc
---

# Scope
Use this skill only for the `multiqc` step in `epigen-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `symlink_stats`
- Step file: `finish/epigen-atacseq_pipeline-finish/steps/multiqc.smk`
- Config file: `finish/epigen-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/multiqc.done`
- Representative outputs: `results/finish/multiqc.done`
- Execution targets: `multiqc`
- Downstream handoff: `plot_sample_annotation`

## Guardrails
- Treat `results/finish/multiqc.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/multiqc.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_sample_annotation` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/multiqc.done` exists and `plot_sample_annotation` can proceed without re-running multiqc.
