---
name: finish-snakemake-workflows-dna-seq-benchmark-vembrane_table_shared_fn
description: Use this skill when orchestrating the retained "vembrane_table_shared_fn" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the vembrane table shared fn stage tied to upstream `annotate_unique_fp_fn` and the downstream handoff to `vembrane_table_unique_fp_fn`. It tracks completion via `results/finish/vembrane_table_shared_fn.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: vembrane_table_shared_fn
  step_name: vembrane table shared fn
---

# Scope
Use this skill only for the `vembrane_table_shared_fn` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `annotate_unique_fp_fn`
- Step file: `finish/dna-seq-benchmark-finish/steps/vembrane_table_shared_fn.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/vembrane_table_shared_fn.done`
- Representative outputs: `results/finish/vembrane_table_shared_fn.done`
- Execution targets: `vembrane_table_shared_fn`
- Downstream handoff: `vembrane_table_unique_fp_fn`

## Guardrails
- Treat `results/finish/vembrane_table_shared_fn.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/vembrane_table_shared_fn.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `vembrane_table_unique_fp_fn` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/vembrane_table_shared_fn.done` exists and `vembrane_table_unique_fp_fn` can proceed without re-running vembrane table shared fn.
