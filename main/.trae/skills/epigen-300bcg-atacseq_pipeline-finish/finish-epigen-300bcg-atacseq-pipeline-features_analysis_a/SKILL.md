---
name: finish-epigen-300bcg-atacseq-pipeline-features_analysis_a
description: Use this skill when orchestrating the retained "features_analysis_a" step of the epigen 300bcg atacseq_pipeline finish finish workflow. It keeps the Features Analysis A stage tied to upstream `quantification` and the downstream handoff to `features_analysis_b`. It tracks completion via `results/finish/features_analysis_a.done`.
metadata:
  workflow_id: epigen-300bcg-atacseq_pipeline-finish
  workflow_name: epigen 300bcg atacseq_pipeline finish
  step_id: features_analysis_a
  step_name: Features Analysis A
---

# Scope
Use this skill only for the `features_analysis_a` step in `epigen-300bcg-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `quantification`
- Step file: `finish/epigen-300bcg-atacseq_pipeline-finish/steps/features_analysis_a.smk`
- Config file: `finish/epigen-300bcg-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/features_analysis_a.done`
- Representative outputs: `results/finish/features_analysis_a.done`
- Execution targets: `features_analysis_a`
- Downstream handoff: `features_analysis_b`

## Guardrails
- Treat `results/finish/features_analysis_a.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/features_analysis_a.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `features_analysis_b` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/features_analysis_a.done` exists and `features_analysis_b` can proceed without re-running Features Analysis A.
