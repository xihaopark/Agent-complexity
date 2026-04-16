---
name: finish-snakemake-workflows-cyrcular-calling-bcf_index
description: Use this skill when orchestrating the retained "bcf_index" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the bcf index stage tied to upstream `samtools_faidx` and the downstream handoff to `bcftools_concat`. It tracks completion via `results/finish/bcf_index.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: bcf_index
  step_name: bcf index
---

# Scope
Use this skill only for the `bcf_index` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `samtools_faidx`
- Step file: `finish/cyrcular-calling-finish/steps/bcf_index.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bcf_index.done`
- Representative outputs: `results/finish/bcf_index.done`
- Execution targets: `bcf_index`
- Downstream handoff: `bcftools_concat`

## Guardrails
- Treat `results/finish/bcf_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bcf_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bcftools_concat` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bcf_index.done` exists and `bcftools_concat` can proceed without re-running bcf index.
