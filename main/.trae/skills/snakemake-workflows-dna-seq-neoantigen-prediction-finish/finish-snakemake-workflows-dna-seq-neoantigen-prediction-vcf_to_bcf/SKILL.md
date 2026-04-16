---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-vcf_to_bcf
description: Use this skill when orchestrating the retained "vcf_to_bcf" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the vcf to bcf stage tied to upstream `strelka_germline` and the downstream handoff to `concat_somatic`. It tracks completion via `results/finish/vcf_to_bcf.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: vcf_to_bcf
  step_name: vcf to bcf
---

# Scope
Use this skill only for the `vcf_to_bcf` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `strelka_germline`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/vcf_to_bcf.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/vcf_to_bcf.done`
- Representative outputs: `results/finish/vcf_to_bcf.done`
- Execution targets: `vcf_to_bcf`
- Downstream handoff: `concat_somatic`

## Guardrails
- Treat `results/finish/vcf_to_bcf.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/vcf_to_bcf.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `concat_somatic` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/vcf_to_bcf.done` exists and `concat_somatic` can proceed without re-running vcf to bcf.
