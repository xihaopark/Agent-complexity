---
name: finish-snakemake-workflows-dna-seq-benchmark-report_fp_fn
description: Use this skill when orchestrating the retained "report_fp_fn" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the report fp fn stage tied to upstream `write_unique_fp_vcf` and the downstream handoff to `report_fp_fn_callset`. It tracks completion via `results/finish/report_fp_fn.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: report_fp_fn
  step_name: report fp fn
---

# Scope
Use this skill only for the `report_fp_fn` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `write_unique_fp_vcf`
- Step file: `finish/dna-seq-benchmark-finish/steps/report_fp_fn.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/report_fp_fn.done`
- Representative outputs: `results/finish/report_fp_fn.done`
- Execution targets: `report_fp_fn`
- Downstream handoff: `report_fp_fn_callset`

## Guardrails
- Treat `results/finish/report_fp_fn.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/report_fp_fn.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `report_fp_fn_callset` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/report_fp_fn.done` exists and `report_fp_fn_callset` can proceed without re-running report fp fn.
