---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-microphaser_germline
description: Use this skill when orchestrating the retained "microphaser_germline" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the microphaser germline stage tied to upstream `microphaser_somatic` and the downstream handoff to `concat_proteome`. It tracks completion via `results/finish/microphaser_germline.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: microphaser_germline
  step_name: microphaser germline
---

# Scope
Use this skill only for the `microphaser_germline` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `microphaser_somatic`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/microphaser_germline.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/microphaser_germline.done`
- Representative outputs: `results/finish/microphaser_germline.done`
- Execution targets: `microphaser_germline`
- Downstream handoff: `concat_proteome`

## Guardrails
- Treat `results/finish/microphaser_germline.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/microphaser_germline.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `concat_proteome` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/microphaser_germline.done` exists and `concat_proteome` can proceed without re-running microphaser germline.
