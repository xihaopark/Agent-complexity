---
name: finish-snakemake-workflows-dna-seq-benchmark-collect_stratifications_fp_fn
description: Use this skill when orchestrating the retained "collect_stratifications_fp_fn" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the collect stratifications fp fn stage tied to upstream `collect_fp_fn` and the downstream handoff to `collect_fp_fn_benchmark`. It tracks completion via `results/finish/collect_stratifications_fp_fn.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: collect_stratifications_fp_fn
  step_name: collect stratifications fp fn
---

# Scope
Use this skill only for the `collect_stratifications_fp_fn` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `collect_fp_fn`
- Step file: `finish/dna-seq-benchmark-finish/steps/collect_stratifications_fp_fn.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/collect_stratifications_fp_fn.done`
- Representative outputs: `results/finish/collect_stratifications_fp_fn.done`
- Execution targets: `collect_stratifications_fp_fn`
- Downstream handoff: `collect_fp_fn_benchmark`

## Guardrails
- Treat `results/finish/collect_stratifications_fp_fn.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/collect_stratifications_fp_fn.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `collect_fp_fn_benchmark` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/collect_stratifications_fp_fn.done` exists and `collect_fp_fn_benchmark` can proceed without re-running collect stratifications fp fn.
