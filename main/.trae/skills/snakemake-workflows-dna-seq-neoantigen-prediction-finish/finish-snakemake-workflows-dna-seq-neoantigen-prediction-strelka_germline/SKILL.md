---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-strelka_germline
description: Use this skill when orchestrating the retained "strelka_germline" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the strelka germline stage tied to upstream `strelka_somatic` and the downstream handoff to `vcf_to_bcf`. It tracks completion via `results/finish/strelka_germline.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: strelka_germline
  step_name: strelka germline
---

# Scope
Use this skill only for the `strelka_germline` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `strelka_somatic`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/strelka_germline.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/strelka_germline.done`
- Representative outputs: `results/finish/strelka_germline.done`
- Execution targets: `strelka_germline`
- Downstream handoff: `vcf_to_bcf`

## Guardrails
- Treat `results/finish/strelka_germline.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/strelka_germline.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `vcf_to_bcf` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/strelka_germline.done` exists and `vcf_to_bcf` can proceed without re-running strelka germline.
