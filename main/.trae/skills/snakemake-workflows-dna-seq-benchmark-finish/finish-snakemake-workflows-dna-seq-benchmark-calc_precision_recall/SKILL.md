---
name: finish-snakemake-workflows-dna-seq-benchmark-calc_precision_recall
description: Use this skill when orchestrating the retained "calc_precision_recall" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the calc precision recall stage tied to upstream `reformat_fp_fn_tp_tables` and the downstream handoff to `collect_stratifications`. It tracks completion via `results/finish/calc_precision_recall.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: calc_precision_recall
  step_name: calc precision recall
---

# Scope
Use this skill only for the `calc_precision_recall` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `reformat_fp_fn_tp_tables`
- Step file: `finish/dna-seq-benchmark-finish/steps/calc_precision_recall.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/calc_precision_recall.done`
- Representative outputs: `results/finish/calc_precision_recall.done`
- Execution targets: `calc_precision_recall`
- Downstream handoff: `collect_stratifications`

## Guardrails
- Treat `results/finish/calc_precision_recall.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/calc_precision_recall.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `collect_stratifications` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/calc_precision_recall.done` exists and `collect_stratifications` can proceed without re-running calc precision recall.
