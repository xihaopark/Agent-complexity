---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-microphaser_somatic
description: Use this skill when orchestrating the retained "microphaser_somatic" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the microphaser somatic stage tied to upstream `reheader_varlociraptor` and the downstream handoff to `microphaser_germline`. It tracks completion via `results/finish/microphaser_somatic.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: microphaser_somatic
  step_name: microphaser somatic
---

# Scope
Use this skill only for the `microphaser_somatic` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `reheader_varlociraptor`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/microphaser_somatic.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/microphaser_somatic.done`
- Representative outputs: `results/finish/microphaser_somatic.done`
- Execution targets: `microphaser_somatic`
- Downstream handoff: `microphaser_germline`

## Guardrails
- Treat `results/finish/microphaser_somatic.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/microphaser_somatic.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `microphaser_germline` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/microphaser_somatic.done` exists and `microphaser_germline` can proceed without re-running microphaser somatic.
