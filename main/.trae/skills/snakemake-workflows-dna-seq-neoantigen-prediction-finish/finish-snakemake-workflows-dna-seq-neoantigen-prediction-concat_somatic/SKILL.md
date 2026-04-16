---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-concat_somatic
description: Use this skill when orchestrating the retained "concat_somatic" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the concat somatic stage tied to upstream `vcf_to_bcf` and the downstream handoff to `get_tumor_from_somatic`. It tracks completion via `results/finish/concat_somatic.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: concat_somatic
  step_name: concat somatic
---

# Scope
Use this skill only for the `concat_somatic` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `vcf_to_bcf`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/concat_somatic.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/concat_somatic.done`
- Representative outputs: `results/finish/concat_somatic.done`
- Execution targets: `concat_somatic`
- Downstream handoff: `get_tumor_from_somatic`

## Guardrails
- Treat `results/finish/concat_somatic.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/concat_somatic.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_tumor_from_somatic` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/concat_somatic.done` exists and `get_tumor_from_somatic` can proceed without re-running concat somatic.
