---
name: finish-maxplanck-ie-snakepipes-link_bam
description: Use this skill when orchestrating the retained "link_bam" step of the maxplanck ie snakepipes finish finish workflow. It keeps the link bam stage and the downstream handoff to `samtools_index_external`. It tracks completion via `results/finish/link_bam.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: link_bam
  step_name: link bam
---

# Scope
Use this skill only for the `link_bam` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/link_bam.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/link_bam.done`
- Representative outputs: `results/finish/link_bam.done`
- Execution targets: `link_bam`
- Downstream handoff: `samtools_index_external`

## Guardrails
- Treat `results/finish/link_bam.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/link_bam.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `samtools_index_external` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/link_bam.done` exists and `samtools_index_external` can proceed without re-running link bam.
