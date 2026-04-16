---
name: finish-snakemake-workflows-dna-seq-benchmark-extract_fp_fn
description: Use this skill when orchestrating the retained "extract_fp_fn" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the extract fp fn stage tied to upstream `benchmark_variants_somatic` and the downstream handoff to `extract_fp_fn_tp`. It tracks completion via `results/finish/extract_fp_fn.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: extract_fp_fn
  step_name: extract fp fn
---

# Scope
Use this skill only for the `extract_fp_fn` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `benchmark_variants_somatic`
- Step file: `finish/dna-seq-benchmark-finish/steps/extract_fp_fn.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/extract_fp_fn.done`
- Representative outputs: `results/finish/extract_fp_fn.done`
- Execution targets: `extract_fp_fn`
- Downstream handoff: `extract_fp_fn_tp`

## Guardrails
- Treat `results/finish/extract_fp_fn.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/extract_fp_fn.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `extract_fp_fn_tp` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/extract_fp_fn.done` exists and `extract_fp_fn_tp` can proceed without re-running extract fp fn.
