---
name: finish-snakemake-workflows-dna-seq-benchmark-benchmark_variants_somatic
description: Use this skill when orchestrating the retained "benchmark_variants_somatic" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the benchmark variants somatic stage tied to upstream `benchmark_variants_germline` and the downstream handoff to `extract_fp_fn`. It tracks completion via `results/finish/benchmark_variants_somatic.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: benchmark_variants_somatic
  step_name: benchmark variants somatic
---

# Scope
Use this skill only for the `benchmark_variants_somatic` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `benchmark_variants_germline`
- Step file: `finish/dna-seq-benchmark-finish/steps/benchmark_variants_somatic.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/benchmark_variants_somatic.done`
- Representative outputs: `results/finish/benchmark_variants_somatic.done`
- Execution targets: `benchmark_variants_somatic`
- Downstream handoff: `extract_fp_fn`

## Guardrails
- Treat `results/finish/benchmark_variants_somatic.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/benchmark_variants_somatic.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `extract_fp_fn` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/benchmark_variants_somatic.done` exists and `extract_fp_fn` can proceed without re-running benchmark variants somatic.
