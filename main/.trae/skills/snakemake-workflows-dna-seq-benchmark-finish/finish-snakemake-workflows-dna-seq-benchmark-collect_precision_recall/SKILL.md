---
name: finish-snakemake-workflows-dna-seq-benchmark-collect_precision_recall
description: Use this skill when orchestrating the retained "collect_precision_recall" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the collect precision recall stage tied to upstream `collect_stratifications` and the downstream handoff to `report_precision_recall`. It tracks completion via `results/finish/collect_precision_recall.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: collect_precision_recall
  step_name: collect precision recall
---

# Scope
Use this skill only for the `collect_precision_recall` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `collect_stratifications`
- Step file: `finish/dna-seq-benchmark-finish/steps/collect_precision_recall.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/collect_precision_recall.done`
- Representative outputs: `results/finish/collect_precision_recall.done`
- Execution targets: `collect_precision_recall`
- Downstream handoff: `report_precision_recall`

## Guardrails
- Treat `results/finish/collect_precision_recall.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/collect_precision_recall.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `report_precision_recall` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/collect_precision_recall.done` exists and `report_precision_recall` can proceed without re-running collect precision recall.
