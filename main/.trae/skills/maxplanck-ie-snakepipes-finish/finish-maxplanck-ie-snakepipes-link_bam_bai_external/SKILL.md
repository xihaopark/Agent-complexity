---
name: finish-maxplanck-ie-snakepipes-link_bam_bai_external
description: Use this skill when orchestrating the retained "link_bam_bai_external" step of the maxplanck ie snakepipes finish finish workflow. It keeps the link bam bai external stage tied to upstream `samtools_index_external` and the downstream handoff to `sambamba_flagstat`. It tracks completion via `results/finish/link_bam_bai_external.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: link_bam_bai_external
  step_name: link bam bai external
---

# Scope
Use this skill only for the `link_bam_bai_external` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `samtools_index_external`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/link_bam_bai_external.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/link_bam_bai_external.done`
- Representative outputs: `results/finish/link_bam_bai_external.done`
- Execution targets: `link_bam_bai_external`
- Downstream handoff: `sambamba_flagstat`

## Guardrails
- Treat `results/finish/link_bam_bai_external.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/link_bam_bai_external.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `sambamba_flagstat` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/link_bam_bai_external.done` exists and `sambamba_flagstat` can proceed without re-running link bam bai external.
