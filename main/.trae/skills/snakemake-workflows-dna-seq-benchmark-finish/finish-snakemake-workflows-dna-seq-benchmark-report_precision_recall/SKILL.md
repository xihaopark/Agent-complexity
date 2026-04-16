---
name: finish-snakemake-workflows-dna-seq-benchmark-report_precision_recall
description: Use this skill when orchestrating the retained "report_precision_recall" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the report precision recall stage tied to upstream `collect_precision_recall` and the downstream handoff to `collect_fp_fn`. It tracks completion via `results/finish/report_precision_recall.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: report_precision_recall
  step_name: report precision recall
---

# Scope
Use this skill only for the `report_precision_recall` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `collect_precision_recall`
- Step file: `finish/dna-seq-benchmark-finish/steps/report_precision_recall.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/report_precision_recall.done`
- Representative outputs: `results/finish/report_precision_recall.done`
- Execution targets: `report_precision_recall`
- Downstream handoff: `collect_fp_fn`

## Guardrails
- Treat `results/finish/report_precision_recall.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/report_precision_recall.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `collect_fp_fn` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/report_precision_recall.done` exists and `collect_fp_fn` can proceed without re-running report precision recall.
