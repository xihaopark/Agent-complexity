---
name: finish-snakemake-workflows-dna-seq-benchmark-vembrane_table_unique_fp_fn
description: Use this skill when orchestrating the retained "vembrane_table_unique_fp_fn" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the vembrane table unique fp fn stage tied to upstream `vembrane_table_shared_fn` and the downstream handoff to `all`. It tracks completion via `results/finish/vembrane_table_unique_fp_fn.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: vembrane_table_unique_fp_fn
  step_name: vembrane table unique fp fn
---

# Scope
Use this skill only for the `vembrane_table_unique_fp_fn` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `vembrane_table_shared_fn`
- Step file: `finish/dna-seq-benchmark-finish/steps/vembrane_table_unique_fp_fn.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/vembrane_table_unique_fp_fn.done`
- Representative outputs: `results/finish/vembrane_table_unique_fp_fn.done`
- Execution targets: `vembrane_table_unique_fp_fn`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/vembrane_table_unique_fp_fn.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/vembrane_table_unique_fp_fn.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/vembrane_table_unique_fp_fn.done` exists and `all` can proceed without re-running vembrane table unique fp fn.
