---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-scatter_candidates
description: Use this skill when orchestrating the retained "scatter_candidates" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the scatter candidates stage tied to upstream `freebayes` and the downstream handoff to `render_scenario`. It tracks completion via `results/finish/scatter_candidates.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: scatter_candidates
  step_name: scatter candidates
---

# Scope
Use this skill only for the `scatter_candidates` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `freebayes`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/scatter_candidates.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/scatter_candidates.done`
- Representative outputs: `results/finish/scatter_candidates.done`
- Execution targets: `scatter_candidates`
- Downstream handoff: `render_scenario`

## Guardrails
- Treat `results/finish/scatter_candidates.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/scatter_candidates.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `render_scenario` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/scatter_candidates.done` exists and `render_scenario` can proceed without re-running scatter candidates.
