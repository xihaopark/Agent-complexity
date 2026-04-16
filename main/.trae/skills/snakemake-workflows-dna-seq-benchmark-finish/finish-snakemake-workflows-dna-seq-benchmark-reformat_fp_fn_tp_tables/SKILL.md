---
name: finish-snakemake-workflows-dna-seq-benchmark-reformat_fp_fn_tp_tables
description: Use this skill when orchestrating the retained "reformat_fp_fn_tp_tables" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the reformat fp fn tp tables stage tied to upstream `extract_fp_fn_tp` and the downstream handoff to `calc_precision_recall`. It tracks completion via `results/finish/reformat_fp_fn_tp_tables.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: reformat_fp_fn_tp_tables
  step_name: reformat fp fn tp tables
---

# Scope
Use this skill only for the `reformat_fp_fn_tp_tables` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `extract_fp_fn_tp`
- Step file: `finish/dna-seq-benchmark-finish/steps/reformat_fp_fn_tp_tables.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/reformat_fp_fn_tp_tables.done`
- Representative outputs: `results/finish/reformat_fp_fn_tp_tables.done`
- Execution targets: `reformat_fp_fn_tp_tables`
- Downstream handoff: `calc_precision_recall`

## Guardrails
- Treat `results/finish/reformat_fp_fn_tp_tables.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/reformat_fp_fn_tp_tables.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `calc_precision_recall` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/reformat_fp_fn_tp_tables.done` exists and `calc_precision_recall` can proceed without re-running reformat fp fn tp tables.
