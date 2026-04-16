---
name: finish-epigen-300bcg-atacseq-pipeline-features_analysis_b
description: Use this skill when orchestrating the retained "features_analysis_b" step of the epigen 300bcg atacseq_pipeline finish finish workflow. It keeps the Features Analysis B stage tied to upstream `features_analysis_a`. It tracks completion via `results/finish/features_analysis_b.done`.
metadata:
  workflow_id: epigen-300bcg-atacseq_pipeline-finish
  workflow_name: epigen 300bcg atacseq_pipeline finish
  step_id: features_analysis_b
  step_name: Features Analysis B
---

# Scope
Use this skill only for the `features_analysis_b` step in `epigen-300bcg-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `features_analysis_a`
- Step file: `finish/epigen-300bcg-atacseq_pipeline-finish/steps/features_analysis_b.smk`
- Config file: `finish/epigen-300bcg-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/features_analysis_b.done`
- Representative outputs: `results/finish/features_analysis_b.done`
- Execution targets: `features_analysis_b`
- Downstream handoff: none

## Guardrails
- Treat `results/finish/features_analysis_b.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/features_analysis_b.smk` so the step remains separable and replayable inside the finish workflow.

## Done Criteria
Mark this step complete only when `results/finish/features_analysis_b.done` exists and matches the intended step boundary.
