---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-strelka_somatic
description: Use this skill when orchestrating the retained "strelka_somatic" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the strelka somatic stage tied to upstream `apply_bqsr` and the downstream handoff to `strelka_germline`. It tracks completion via `results/finish/strelka_somatic.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: strelka_somatic
  step_name: strelka somatic
---

# Scope
Use this skill only for the `strelka_somatic` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `apply_bqsr`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/strelka_somatic.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/strelka_somatic.done`
- Representative outputs: `results/finish/strelka_somatic.done`
- Execution targets: `strelka_somatic`
- Downstream handoff: `strelka_germline`

## Guardrails
- Treat `results/finish/strelka_somatic.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/strelka_somatic.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `strelka_germline` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/strelka_somatic.done` exists and `strelka_germline` can proceed without re-running strelka somatic.
