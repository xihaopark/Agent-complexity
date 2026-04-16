---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-vg2svg
description: Use this skill when orchestrating the retained "vg2svg" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the vg2svg stage tied to upstream `estimate_tmb` and the downstream handoff to `all`. It tracks completion via `results/finish/vg2svg.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: vg2svg
  step_name: vg2svg
---

# Scope
Use this skill only for the `vg2svg` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `estimate_tmb`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/vg2svg.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/vg2svg.done`
- Representative outputs: `results/finish/vg2svg.done`
- Execution targets: `vg2svg`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/vg2svg.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/vg2svg.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/vg2svg.done` exists and `all` can proceed without re-running vg2svg.
