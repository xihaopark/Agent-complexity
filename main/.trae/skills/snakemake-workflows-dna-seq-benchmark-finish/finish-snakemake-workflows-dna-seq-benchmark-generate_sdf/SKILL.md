---
name: finish-snakemake-workflows-dna-seq-benchmark-generate_sdf
description: Use this skill when orchestrating the retained "generate_sdf" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the generate sdf stage tied to upstream `stat_truth` and the downstream handoff to `benchmark_variants_germline`. It tracks completion via `results/finish/generate_sdf.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: generate_sdf
  step_name: generate sdf
---

# Scope
Use this skill only for the `generate_sdf` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `stat_truth`
- Step file: `finish/dna-seq-benchmark-finish/steps/generate_sdf.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/generate_sdf.done`
- Representative outputs: `results/finish/generate_sdf.done`
- Execution targets: `generate_sdf`
- Downstream handoff: `benchmark_variants_germline`

## Guardrails
- Treat `results/finish/generate_sdf.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/generate_sdf.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `benchmark_variants_germline` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/generate_sdf.done` exists and `benchmark_variants_germline` can proceed without re-running generate sdf.
