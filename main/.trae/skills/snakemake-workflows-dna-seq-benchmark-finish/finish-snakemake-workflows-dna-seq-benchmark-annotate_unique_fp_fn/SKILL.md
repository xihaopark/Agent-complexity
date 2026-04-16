---
name: finish-snakemake-workflows-dna-seq-benchmark-annotate_unique_fp_fn
description: Use this skill when orchestrating the retained "annotate_unique_fp_fn" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the annotate unique fp fn stage tied to upstream `annotate_shared_fn` and the downstream handoff to `vembrane_table_shared_fn`. It tracks completion via `results/finish/annotate_unique_fp_fn.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: annotate_unique_fp_fn
  step_name: annotate unique fp fn
---

# Scope
Use this skill only for the `annotate_unique_fp_fn` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `annotate_shared_fn`
- Step file: `finish/dna-seq-benchmark-finish/steps/annotate_unique_fp_fn.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/annotate_unique_fp_fn.done`
- Representative outputs: `results/finish/annotate_unique_fp_fn.done`
- Execution targets: `annotate_unique_fp_fn`
- Downstream handoff: `vembrane_table_shared_fn`

## Guardrails
- Treat `results/finish/annotate_unique_fp_fn.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/annotate_unique_fp_fn.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `vembrane_table_shared_fn` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/annotate_unique_fp_fn.done` exists and `vembrane_table_shared_fn` can proceed without re-running annotate unique fp fn.
