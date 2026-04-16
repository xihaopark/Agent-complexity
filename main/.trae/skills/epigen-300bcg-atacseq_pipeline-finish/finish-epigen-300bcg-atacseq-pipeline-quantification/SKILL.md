---
name: finish-epigen-300bcg-atacseq-pipeline-quantification
description: Use this skill when orchestrating the retained "quantification" step of the epigen 300bcg atacseq_pipeline finish finish workflow. It keeps the Quantification stage tied to upstream `qc_stats` and the downstream handoff to `features_analysis_a`. It tracks completion via `results/finish/quantification.done`.
metadata:
  workflow_id: epigen-300bcg-atacseq_pipeline-finish
  workflow_name: epigen 300bcg atacseq_pipeline finish
  step_id: quantification
  step_name: Quantification
---

# Scope
Use this skill only for the `quantification` step in `epigen-300bcg-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `qc_stats`
- Step file: `finish/epigen-300bcg-atacseq_pipeline-finish/steps/quantification.smk`
- Config file: `finish/epigen-300bcg-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/quantification.done`
- Representative outputs: `results/finish/quantification.done`
- Execution targets: `quantification`
- Downstream handoff: `features_analysis_a`

## Guardrails
- Treat `results/finish/quantification.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/quantification.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `features_analysis_a` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/quantification.done` exists and `features_analysis_a` can proceed without re-running Quantification.
