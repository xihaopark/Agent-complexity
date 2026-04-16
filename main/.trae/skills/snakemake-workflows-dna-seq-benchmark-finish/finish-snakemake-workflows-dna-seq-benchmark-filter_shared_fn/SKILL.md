---
name: finish-snakemake-workflows-dna-seq-benchmark-filter_shared_fn
description: Use this skill when orchestrating the retained "filter_shared_fn" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the filter shared fn stage tied to upstream `collect_fp_fn_benchmark` and the downstream handoff to `filter_unique`. It tracks completion via `results/finish/filter_shared_fn.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: filter_shared_fn
  step_name: filter shared fn
---

# Scope
Use this skill only for the `filter_shared_fn` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `collect_fp_fn_benchmark`
- Step file: `finish/dna-seq-benchmark-finish/steps/filter_shared_fn.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/filter_shared_fn.done`
- Representative outputs: `results/finish/filter_shared_fn.done`
- Execution targets: `filter_shared_fn`
- Downstream handoff: `filter_unique`

## Guardrails
- Treat `results/finish/filter_shared_fn.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/filter_shared_fn.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `filter_unique` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/filter_shared_fn.done` exists and `filter_unique` can proceed without re-running filter shared fn.
