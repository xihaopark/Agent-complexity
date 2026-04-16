---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-arriba
description: Use this skill when orchestrating the retained "arriba" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the arriba stage tied to upstream `STAR_align` and the downstream handoff to `estimate_tmb`. It tracks completion via `results/finish/arriba.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: arriba
  step_name: arriba
---

# Scope
Use this skill only for the `arriba` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `STAR_align`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/arriba.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/arriba.done`
- Representative outputs: `results/finish/arriba.done`
- Execution targets: `arriba`
- Downstream handoff: `estimate_tmb`

## Guardrails
- Treat `results/finish/arriba.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/arriba.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `estimate_tmb` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/arriba.done` exists and `estimate_tmb` can proceed without re-running arriba.
