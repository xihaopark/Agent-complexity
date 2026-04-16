---
name: finish-maxplanck-ie-snakepipes-samtools_index_external
description: Use this skill when orchestrating the retained "samtools_index_external" step of the maxplanck ie snakepipes finish finish workflow. It keeps the samtools index external stage tied to upstream `link_bam` and the downstream handoff to `link_bam_bai_external`. It tracks completion via `results/finish/samtools_index_external.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: samtools_index_external
  step_name: samtools index external
---

# Scope
Use this skill only for the `samtools_index_external` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `link_bam`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/samtools_index_external.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/samtools_index_external.done`
- Representative outputs: `results/finish/samtools_index_external.done`
- Execution targets: `samtools_index_external`
- Downstream handoff: `link_bam_bai_external`

## Guardrails
- Treat `results/finish/samtools_index_external.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/samtools_index_external.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `link_bam_bai_external` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/samtools_index_external.done` exists and `link_bam_bai_external` can proceed without re-running samtools index external.
