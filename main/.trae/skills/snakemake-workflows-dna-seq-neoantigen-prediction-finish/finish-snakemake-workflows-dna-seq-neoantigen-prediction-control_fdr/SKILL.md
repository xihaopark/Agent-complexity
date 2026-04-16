---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-control_fdr
description: Use this skill when orchestrating the retained "control_fdr" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the control fdr stage tied to upstream `gather_calls` and the downstream handoff to `merge_calls`. It tracks completion via `results/finish/control_fdr.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: control_fdr
  step_name: control fdr
---

# Scope
Use this skill only for the `control_fdr` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `gather_calls`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/control_fdr.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/control_fdr.done`
- Representative outputs: `results/finish/control_fdr.done`
- Execution targets: `control_fdr`
- Downstream handoff: `merge_calls`

## Guardrails
- Treat `results/finish/control_fdr.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/control_fdr.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `merge_calls` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/control_fdr.done` exists and `merge_calls` can proceed without re-running control fdr.
