---
name: finish-snakemake-workflows-dna-seq-benchmark-collect_fp_fn
description: Use this skill when orchestrating the retained "collect_fp_fn" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the collect fp fn stage tied to upstream `report_precision_recall` and the downstream handoff to `collect_stratifications_fp_fn`. It tracks completion via `results/finish/collect_fp_fn.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: collect_fp_fn
  step_name: collect fp fn
---

# Scope
Use this skill only for the `collect_fp_fn` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `report_precision_recall`
- Step file: `finish/dna-seq-benchmark-finish/steps/collect_fp_fn.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/collect_fp_fn.done`
- Representative outputs: `results/finish/collect_fp_fn.done`
- Execution targets: `collect_fp_fn`
- Downstream handoff: `collect_stratifications_fp_fn`

## Guardrails
- Treat `results/finish/collect_fp_fn.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/collect_fp_fn.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `collect_stratifications_fp_fn` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/collect_fp_fn.done` exists and `collect_stratifications_fp_fn` can proceed without re-running collect fp fn.
