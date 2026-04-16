---
name: finish-snakemake-workflows-cyrcular-calling-samtools_faidx
description: Use this skill when orchestrating the retained "samtools_faidx" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the samtools faidx stage tied to upstream `samtools_index` and the downstream handoff to `bcf_index`. It tracks completion via `results/finish/samtools_faidx.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: samtools_faidx
  step_name: samtools faidx
---

# Scope
Use this skill only for the `samtools_faidx` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `samtools_index`
- Step file: `finish/cyrcular-calling-finish/steps/samtools_faidx.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/samtools_faidx.done`
- Representative outputs: `results/finish/samtools_faidx.done`
- Execution targets: `samtools_faidx`
- Downstream handoff: `bcf_index`

## Guardrails
- Treat `results/finish/samtools_faidx.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/samtools_faidx.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bcf_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/samtools_faidx.done` exists and `bcf_index` can proceed without re-running samtools faidx.
