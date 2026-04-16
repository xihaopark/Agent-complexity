---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-merge_calls
description: Use this skill when orchestrating the retained "merge_calls" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the merge calls stage tied to upstream `control_fdr` and the downstream handoff to `change_samplenames`. It tracks completion via `results/finish/merge_calls.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: merge_calls
  step_name: merge calls
---

# Scope
Use this skill only for the `merge_calls` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `control_fdr`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/merge_calls.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/merge_calls.done`
- Representative outputs: `results/finish/merge_calls.done`
- Execution targets: `merge_calls`
- Downstream handoff: `change_samplenames`

## Guardrails
- Treat `results/finish/merge_calls.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/merge_calls.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `change_samplenames` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/merge_calls.done` exists and `change_samplenames` can proceed without re-running merge calls.
