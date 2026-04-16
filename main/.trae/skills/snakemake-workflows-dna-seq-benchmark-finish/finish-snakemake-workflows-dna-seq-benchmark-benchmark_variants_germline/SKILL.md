---
name: finish-snakemake-workflows-dna-seq-benchmark-benchmark_variants_germline
description: Use this skill when orchestrating the retained "benchmark_variants_germline" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the benchmark variants germline stage tied to upstream `generate_sdf` and the downstream handoff to `benchmark_variants_somatic`. It tracks completion via `results/finish/benchmark_variants_germline.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: benchmark_variants_germline
  step_name: benchmark variants germline
---

# Scope
Use this skill only for the `benchmark_variants_germline` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `generate_sdf`
- Step file: `finish/dna-seq-benchmark-finish/steps/benchmark_variants_germline.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/benchmark_variants_germline.done`
- Representative outputs: `results/finish/benchmark_variants_germline.done`
- Execution targets: `benchmark_variants_germline`
- Downstream handoff: `benchmark_variants_somatic`

## Guardrails
- Treat `results/finish/benchmark_variants_germline.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/benchmark_variants_germline.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `benchmark_variants_somatic` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/benchmark_variants_germline.done` exists and `benchmark_variants_somatic` can proceed without re-running benchmark variants germline.
