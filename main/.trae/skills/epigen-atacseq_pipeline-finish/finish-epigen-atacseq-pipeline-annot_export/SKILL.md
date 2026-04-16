---
name: finish-epigen-atacseq-pipeline-annot_export
description: Use this skill when orchestrating the retained "annot_export" step of the epigen atacseq_pipeline finish finish workflow. It keeps the annot export stage tied to upstream `config_export` and the downstream handoff to `install_homer`. It tracks completion via `results/finish/annot_export.done`.
metadata:
  workflow_id: epigen-atacseq_pipeline-finish
  workflow_name: epigen atacseq_pipeline finish
  step_id: annot_export
  step_name: annot export
---

# Scope
Use this skill only for the `annot_export` step in `epigen-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `config_export`
- Step file: `finish/epigen-atacseq_pipeline-finish/steps/annot_export.smk`
- Config file: `finish/epigen-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/annot_export.done`
- Representative outputs: `results/finish/annot_export.done`
- Execution targets: `annot_export`
- Downstream handoff: `install_homer`

## Guardrails
- Treat `results/finish/annot_export.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/annot_export.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `install_homer` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/annot_export.done` exists and `install_homer` can proceed without re-running annot export.
