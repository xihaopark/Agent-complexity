---
name: finish-snakemake-workflows-dna-seq-benchmark-index_bcf
description: Use this skill when orchestrating the retained "index_bcf" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the index bcf stage tied to upstream `index_vcf` and the downstream handoff to `sort_vcf`. It tracks completion via `results/finish/index_bcf.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: index_bcf
  step_name: index bcf
---

# Scope
Use this skill only for the `index_bcf` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `index_vcf`
- Step file: `finish/dna-seq-benchmark-finish/steps/index_bcf.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/index_bcf.done`
- Representative outputs: `results/finish/index_bcf.done`
- Execution targets: `index_bcf`
- Downstream handoff: `sort_vcf`

## Guardrails
- Treat `results/finish/index_bcf.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/index_bcf.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `sort_vcf` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/index_bcf.done` exists and `sort_vcf` can proceed without re-running index bcf.
