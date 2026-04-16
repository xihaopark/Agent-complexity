---
name: finish-snakemake-workflows-dna-seq-benchmark-write_unique_fn_vcf
description: Use this skill when orchestrating the retained "write_unique_fn_vcf" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the write unique fn vcf stage tied to upstream `write_shared_fn_vcf` and the downstream handoff to `write_unique_fp_vcf`. It tracks completion via `results/finish/write_unique_fn_vcf.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: write_unique_fn_vcf
  step_name: write unique fn vcf
---

# Scope
Use this skill only for the `write_unique_fn_vcf` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `write_shared_fn_vcf`
- Step file: `finish/dna-seq-benchmark-finish/steps/write_unique_fn_vcf.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/write_unique_fn_vcf.done`
- Representative outputs: `results/finish/write_unique_fn_vcf.done`
- Execution targets: `write_unique_fn_vcf`
- Downstream handoff: `write_unique_fp_vcf`

## Guardrails
- Treat `results/finish/write_unique_fn_vcf.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/write_unique_fn_vcf.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `write_unique_fp_vcf` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/write_unique_fn_vcf.done` exists and `write_unique_fp_vcf` can proceed without re-running write unique fn vcf.
