---
name: finish-epigen-atacseq-pipeline-install_homer
description: Use this skill when orchestrating the retained "install_homer" step of the epigen atacseq_pipeline finish finish workflow. It keeps the install homer stage tied to upstream `annot_export` and the downstream handoff to `align`. It tracks completion via `results/finish/install_homer.done`.
metadata:
  workflow_id: epigen-atacseq_pipeline-finish
  workflow_name: epigen atacseq_pipeline finish
  step_id: install_homer
  step_name: install homer
---

# Scope
Use this skill only for the `install_homer` step in `epigen-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `annot_export`
- Step file: `finish/epigen-atacseq_pipeline-finish/steps/install_homer.smk`
- Config file: `finish/epigen-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/install_homer.done`
- Representative outputs: `results/finish/install_homer.done`
- Execution targets: `install_homer`
- Downstream handoff: `align`

## Guardrails
- Treat `results/finish/install_homer.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/install_homer.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `align` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/install_homer.done` exists and `align` can proceed without re-running install homer.
