---
name: finish-snakemake-workflows-dna-seq-benchmark-write_unique_fp_vcf
description: Use this skill when orchestrating the retained "write_unique_fp_vcf" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the write unique fp vcf stage tied to upstream `write_unique_fn_vcf` and the downstream handoff to `report_fp_fn`. It tracks completion via `results/finish/write_unique_fp_vcf.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: write_unique_fp_vcf
  step_name: write unique fp vcf
---

# Scope
Use this skill only for the `write_unique_fp_vcf` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `write_unique_fn_vcf`
- Step file: `finish/dna-seq-benchmark-finish/steps/write_unique_fp_vcf.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/write_unique_fp_vcf.done`
- Representative outputs: `results/finish/write_unique_fp_vcf.done`
- Execution targets: `write_unique_fp_vcf`
- Downstream handoff: `report_fp_fn`

## Guardrails
- Treat `results/finish/write_unique_fp_vcf.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/write_unique_fp_vcf.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `report_fp_fn` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/write_unique_fp_vcf.done` exists and `report_fp_fn` can proceed without re-running write unique fp vcf.
