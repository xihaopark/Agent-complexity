---
name: finish-snakemake-workflows-dna-seq-benchmark-filter_unique
description: Use this skill when orchestrating the retained "filter_unique" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the filter unique stage tied to upstream `filter_shared_fn` and the downstream handoff to `write_shared_fn_vcf`. It tracks completion via `results/finish/filter_unique.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: filter_unique
  step_name: filter unique
---

# Scope
Use this skill only for the `filter_unique` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `filter_shared_fn`
- Step file: `finish/dna-seq-benchmark-finish/steps/filter_unique.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/filter_unique.done`
- Representative outputs: `results/finish/filter_unique.done`
- Execution targets: `filter_unique`
- Downstream handoff: `write_shared_fn_vcf`

## Guardrails
- Treat `results/finish/filter_unique.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/filter_unique.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `write_shared_fn_vcf` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/filter_unique.done` exists and `write_shared_fn_vcf` can proceed without re-running filter unique.
