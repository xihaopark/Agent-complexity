---
name: finish-snakemake-workflows-dna-seq-benchmark-merge_callsets
description: Use this skill when orchestrating the retained "merge_callsets" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the merge callsets stage tied to upstream `get_reference_dict` and the downstream handoff to `liftover_callset`. It tracks completion via `results/finish/merge_callsets.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: merge_callsets
  step_name: merge callsets
---

# Scope
Use this skill only for the `merge_callsets` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `get_reference_dict`
- Step file: `finish/dna-seq-benchmark-finish/steps/merge_callsets.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/merge_callsets.done`
- Representative outputs: `results/finish/merge_callsets.done`
- Execution targets: `merge_callsets`
- Downstream handoff: `liftover_callset`

## Guardrails
- Treat `results/finish/merge_callsets.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/merge_callsets.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `liftover_callset` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/merge_callsets.done` exists and `liftover_callset` can proceed without re-running merge callsets.
