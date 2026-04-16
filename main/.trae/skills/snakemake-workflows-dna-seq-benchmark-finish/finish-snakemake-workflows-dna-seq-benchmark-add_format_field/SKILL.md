---
name: finish-snakemake-workflows-dna-seq-benchmark-add_format_field
description: Use this skill when orchestrating the retained "add_format_field" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the add format field stage tied to upstream `rename_contigs` and the downstream handoff to `remove_non_pass`. It tracks completion via `results/finish/add_format_field.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: add_format_field
  step_name: add format field
---

# Scope
Use this skill only for the `add_format_field` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `rename_contigs`
- Step file: `finish/dna-seq-benchmark-finish/steps/add_format_field.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/add_format_field.done`
- Representative outputs: `results/finish/add_format_field.done`
- Execution targets: `add_format_field`
- Downstream handoff: `remove_non_pass`

## Guardrails
- Treat `results/finish/add_format_field.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/add_format_field.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `remove_non_pass` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/add_format_field.done` exists and `remove_non_pass` can proceed without re-running add format field.
