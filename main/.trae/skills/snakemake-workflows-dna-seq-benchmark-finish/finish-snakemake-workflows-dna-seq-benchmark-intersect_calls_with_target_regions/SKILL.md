---
name: finish-snakemake-workflows-dna-seq-benchmark-intersect_calls_with_target_regions
description: Use this skill when orchestrating the retained "intersect_calls_with_target_regions" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the intersect calls with target regions stage tied to upstream `remove_non_pass` and the downstream handoff to `restrict_to_reference_contigs`. It tracks completion via `results/finish/intersect_calls_with_target_regions.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: intersect_calls_with_target_regions
  step_name: intersect calls with target regions
---

# Scope
Use this skill only for the `intersect_calls_with_target_regions` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `remove_non_pass`
- Step file: `finish/dna-seq-benchmark-finish/steps/intersect_calls_with_target_regions.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/intersect_calls_with_target_regions.done`
- Representative outputs: `results/finish/intersect_calls_with_target_regions.done`
- Execution targets: `intersect_calls_with_target_regions`
- Downstream handoff: `restrict_to_reference_contigs`

## Guardrails
- Treat `results/finish/intersect_calls_with_target_regions.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/intersect_calls_with_target_regions.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `restrict_to_reference_contigs` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/intersect_calls_with_target_regions.done` exists and `restrict_to_reference_contigs` can proceed without re-running intersect calls with target regions.
