---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-gather_calls
description: Use this skill when orchestrating the retained "gather_calls" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the gather calls stage tied to upstream `filter_odds` and the downstream handoff to `control_fdr`. It tracks completion via `results/finish/gather_calls.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: gather_calls
  step_name: gather calls
---

# Scope
Use this skill only for the `gather_calls` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `filter_odds`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/gather_calls.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/gather_calls.done`
- Representative outputs: `results/finish/gather_calls.done`
- Execution targets: `gather_calls`
- Downstream handoff: `control_fdr`

## Guardrails
- Treat `results/finish/gather_calls.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/gather_calls.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `control_fdr` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/gather_calls.done` exists and `control_fdr` can proceed without re-running gather calls.
