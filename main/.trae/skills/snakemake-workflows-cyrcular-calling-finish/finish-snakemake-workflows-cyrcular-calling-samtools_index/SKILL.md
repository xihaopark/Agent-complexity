---
name: finish-snakemake-workflows-cyrcular-calling-samtools_index
description: Use this skill when orchestrating the retained "samtools_index" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the samtools index stage tied to upstream `merge_fastqs` and the downstream handoff to `samtools_faidx`. It tracks completion via `results/finish/samtools_index.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: samtools_index
  step_name: samtools index
---

# Scope
Use this skill only for the `samtools_index` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `merge_fastqs`
- Step file: `finish/cyrcular-calling-finish/steps/samtools_index.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/samtools_index.done`
- Representative outputs: `results/finish/samtools_index.done`
- Execution targets: `samtools_index`
- Downstream handoff: `samtools_faidx`

## Guardrails
- Treat `results/finish/samtools_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/samtools_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `samtools_faidx` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/samtools_index.done` exists and `samtools_faidx` can proceed without re-running samtools index.
