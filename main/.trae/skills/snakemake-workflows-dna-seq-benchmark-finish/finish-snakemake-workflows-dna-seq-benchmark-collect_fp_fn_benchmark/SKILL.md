---
name: finish-snakemake-workflows-dna-seq-benchmark-collect_fp_fn_benchmark
description: Use this skill when orchestrating the retained "collect_fp_fn_benchmark" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the collect fp fn benchmark stage tied to upstream `collect_stratifications_fp_fn` and the downstream handoff to `filter_shared_fn`. It tracks completion via `results/finish/collect_fp_fn_benchmark.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: collect_fp_fn_benchmark
  step_name: collect fp fn benchmark
---

# Scope
Use this skill only for the `collect_fp_fn_benchmark` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `collect_stratifications_fp_fn`
- Step file: `finish/dna-seq-benchmark-finish/steps/collect_fp_fn_benchmark.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/collect_fp_fn_benchmark.done`
- Representative outputs: `results/finish/collect_fp_fn_benchmark.done`
- Execution targets: `collect_fp_fn_benchmark`
- Downstream handoff: `filter_shared_fn`

## Guardrails
- Treat `results/finish/collect_fp_fn_benchmark.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/collect_fp_fn_benchmark.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `filter_shared_fn` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/collect_fp_fn_benchmark.done` exists and `filter_shared_fn` can proceed without re-running collect fp fn benchmark.
