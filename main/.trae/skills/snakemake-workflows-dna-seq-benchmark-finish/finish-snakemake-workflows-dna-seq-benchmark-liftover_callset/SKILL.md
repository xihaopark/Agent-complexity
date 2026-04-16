---
name: finish-snakemake-workflows-dna-seq-benchmark-liftover_callset
description: Use this skill when orchestrating the retained "liftover_callset" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the liftover callset stage tied to upstream `merge_callsets` and the downstream handoff to `rename_contigs`. It tracks completion via `results/finish/liftover_callset.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: liftover_callset
  step_name: liftover callset
---

# Scope
Use this skill only for the `liftover_callset` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `merge_callsets`
- Step file: `finish/dna-seq-benchmark-finish/steps/liftover_callset.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/liftover_callset.done`
- Representative outputs: `results/finish/liftover_callset.done`
- Execution targets: `liftover_callset`
- Downstream handoff: `rename_contigs`

## Guardrails
- Treat `results/finish/liftover_callset.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/liftover_callset.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `rename_contigs` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/liftover_callset.done` exists and `rename_contigs` can proceed without re-running liftover callset.
