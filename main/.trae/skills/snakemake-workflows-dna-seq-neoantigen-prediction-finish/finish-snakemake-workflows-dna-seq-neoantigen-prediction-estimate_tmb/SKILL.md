---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-estimate_tmb
description: Use this skill when orchestrating the retained "estimate_tmb" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the estimate tmb stage tied to upstream `arriba` and the downstream handoff to `vg2svg`. It tracks completion via `results/finish/estimate_tmb.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: estimate_tmb
  step_name: estimate tmb
---

# Scope
Use this skill only for the `estimate_tmb` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `arriba`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/estimate_tmb.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/estimate_tmb.done`
- Representative outputs: `results/finish/estimate_tmb.done`
- Execution targets: `estimate_tmb`
- Downstream handoff: `vg2svg`

## Guardrails
- Treat `results/finish/estimate_tmb.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/estimate_tmb.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `vg2svg` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/estimate_tmb.done` exists and `vg2svg` can proceed without re-running estimate tmb.
