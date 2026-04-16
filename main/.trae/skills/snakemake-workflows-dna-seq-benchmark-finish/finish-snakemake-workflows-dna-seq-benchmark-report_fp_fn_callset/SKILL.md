---
name: finish-snakemake-workflows-dna-seq-benchmark-report_fp_fn_callset
description: Use this skill when orchestrating the retained "report_fp_fn_callset" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the report fp fn callset stage tied to upstream `report_fp_fn` and the downstream handoff to `get_downsampled_vep_cache`. It tracks completion via `results/finish/report_fp_fn_callset.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: report_fp_fn_callset
  step_name: report fp fn callset
---

# Scope
Use this skill only for the `report_fp_fn_callset` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `report_fp_fn`
- Step file: `finish/dna-seq-benchmark-finish/steps/report_fp_fn_callset.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/report_fp_fn_callset.done`
- Representative outputs: `results/finish/report_fp_fn_callset.done`
- Execution targets: `report_fp_fn_callset`
- Downstream handoff: `get_downsampled_vep_cache`

## Guardrails
- Treat `results/finish/report_fp_fn_callset.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/report_fp_fn_callset.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_downsampled_vep_cache` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/report_fp_fn_callset.done` exists and `get_downsampled_vep_cache` can proceed without re-running report fp fn callset.
