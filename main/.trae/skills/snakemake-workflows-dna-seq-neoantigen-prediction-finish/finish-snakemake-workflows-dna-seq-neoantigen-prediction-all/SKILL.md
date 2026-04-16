---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-all
description: Use this skill when orchestrating the retained "all" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the all stage tied to upstream `vg2svg`. It tracks completion via `results/finish/all.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: all
  step_name: all
---

# Scope
Use this skill only for the `all` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `vg2svg`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/all.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/all.done`
- Representative outputs: `results/finish/all.done`
- Execution targets: `all`
- Downstream handoff: none

## Guardrails
- Treat `results/finish/all.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/all.smk` so the step remains separable and replayable inside the finish workflow.

## Done Criteria
Mark this step complete only when `results/finish/all.done` exists and matches the intended step boundary.
