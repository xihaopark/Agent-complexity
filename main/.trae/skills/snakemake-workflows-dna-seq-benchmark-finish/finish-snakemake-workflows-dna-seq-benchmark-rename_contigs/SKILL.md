---
name: finish-snakemake-workflows-dna-seq-benchmark-rename_contigs
description: Use this skill when orchestrating the retained "rename_contigs" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the rename contigs stage tied to upstream `liftover_callset` and the downstream handoff to `add_format_field`. It tracks completion via `results/finish/rename_contigs.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: rename_contigs
  step_name: rename contigs
---

# Scope
Use this skill only for the `rename_contigs` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `liftover_callset`
- Step file: `finish/dna-seq-benchmark-finish/steps/rename_contigs.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/rename_contigs.done`
- Representative outputs: `results/finish/rename_contigs.done`
- Execution targets: `rename_contigs`
- Downstream handoff: `add_format_field`

## Guardrails
- Treat `results/finish/rename_contigs.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/rename_contigs.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `add_format_field` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/rename_contigs.done` exists and `add_format_field` can proceed without re-running rename contigs.
