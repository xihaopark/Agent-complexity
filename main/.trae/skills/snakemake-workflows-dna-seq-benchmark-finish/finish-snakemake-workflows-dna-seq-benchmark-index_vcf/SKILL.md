---
name: finish-snakemake-workflows-dna-seq-benchmark-index_vcf
description: Use this skill when orchestrating the retained "index_vcf" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the index vcf stage tied to upstream `norm_vcf` and the downstream handoff to `index_bcf`. It tracks completion via `results/finish/index_vcf.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: index_vcf
  step_name: index vcf
---

# Scope
Use this skill only for the `index_vcf` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `norm_vcf`
- Step file: `finish/dna-seq-benchmark-finish/steps/index_vcf.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/index_vcf.done`
- Representative outputs: `results/finish/index_vcf.done`
- Execution targets: `index_vcf`
- Downstream handoff: `index_bcf`

## Guardrails
- Treat `results/finish/index_vcf.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/index_vcf.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `index_bcf` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/index_vcf.done` exists and `index_bcf` can proceed without re-running index vcf.
