---
name: finish-snakemake-workflows-dna-seq-benchmark-remove_non_pass
description: Use this skill when orchestrating the retained "remove_non_pass" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the remove non pass stage tied to upstream `add_format_field` and the downstream handoff to `intersect_calls_with_target_regions`. It tracks completion via `results/finish/remove_non_pass.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: remove_non_pass
  step_name: remove non pass
---

# Scope
Use this skill only for the `remove_non_pass` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `add_format_field`
- Step file: `finish/dna-seq-benchmark-finish/steps/remove_non_pass.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/remove_non_pass.done`
- Representative outputs: `results/finish/remove_non_pass.done`
- Execution targets: `remove_non_pass`
- Downstream handoff: `intersect_calls_with_target_regions`

## Guardrails
- Treat `results/finish/remove_non_pass.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/remove_non_pass.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `intersect_calls_with_target_regions` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/remove_non_pass.done` exists and `intersect_calls_with_target_regions` can proceed without re-running remove non pass.
