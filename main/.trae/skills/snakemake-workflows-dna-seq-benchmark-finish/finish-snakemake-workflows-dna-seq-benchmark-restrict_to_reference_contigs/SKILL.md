---
name: finish-snakemake-workflows-dna-seq-benchmark-restrict_to_reference_contigs
description: Use this skill when orchestrating the retained "restrict_to_reference_contigs" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the restrict to reference contigs stage tied to upstream `intersect_calls_with_target_regions` and the downstream handoff to `normalize_calls`. It tracks completion via `results/finish/restrict_to_reference_contigs.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: restrict_to_reference_contigs
  step_name: restrict to reference contigs
---

# Scope
Use this skill only for the `restrict_to_reference_contigs` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `intersect_calls_with_target_regions`
- Step file: `finish/dna-seq-benchmark-finish/steps/restrict_to_reference_contigs.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/restrict_to_reference_contigs.done`
- Representative outputs: `results/finish/restrict_to_reference_contigs.done`
- Execution targets: `restrict_to_reference_contigs`
- Downstream handoff: `normalize_calls`

## Guardrails
- Treat `results/finish/restrict_to_reference_contigs.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/restrict_to_reference_contigs.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `normalize_calls` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/restrict_to_reference_contigs.done` exists and `normalize_calls` can proceed without re-running restrict to reference contigs.
