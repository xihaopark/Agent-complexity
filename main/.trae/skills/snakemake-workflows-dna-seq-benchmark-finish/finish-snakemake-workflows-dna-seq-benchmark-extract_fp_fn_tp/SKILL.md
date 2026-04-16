---
name: finish-snakemake-workflows-dna-seq-benchmark-extract_fp_fn_tp
description: Use this skill when orchestrating the retained "extract_fp_fn_tp" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the extract fp fn tp stage tied to upstream `extract_fp_fn` and the downstream handoff to `reformat_fp_fn_tp_tables`. It tracks completion via `results/finish/extract_fp_fn_tp.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: extract_fp_fn_tp
  step_name: extract fp fn tp
---

# Scope
Use this skill only for the `extract_fp_fn_tp` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `extract_fp_fn`
- Step file: `finish/dna-seq-benchmark-finish/steps/extract_fp_fn_tp.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/extract_fp_fn_tp.done`
- Representative outputs: `results/finish/extract_fp_fn_tp.done`
- Execution targets: `extract_fp_fn_tp`
- Downstream handoff: `reformat_fp_fn_tp_tables`

## Guardrails
- Treat `results/finish/extract_fp_fn_tp.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/extract_fp_fn_tp.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `reformat_fp_fn_tp_tables` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/extract_fp_fn_tp.done` exists and `reformat_fp_fn_tp_tables` can proceed without re-running extract fp fn tp.
