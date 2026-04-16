---
name: finish-maxplanck-ie-snakepipes-sambamba_flagstat
description: Use this skill when orchestrating the retained "sambamba_flagstat" step of the maxplanck ie snakepipes finish finish workflow. It keeps the sambamba flagstat stage tied to upstream `link_bam_bai_external` and the downstream handoff to `bamCoverage`. It tracks completion via `results/finish/sambamba_flagstat.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: sambamba_flagstat
  step_name: sambamba flagstat
---

# Scope
Use this skill only for the `sambamba_flagstat` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `link_bam_bai_external`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/sambamba_flagstat.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/sambamba_flagstat.done`
- Representative outputs: `results/finish/sambamba_flagstat.done`
- Execution targets: `sambamba_flagstat`
- Downstream handoff: `bamCoverage`

## Guardrails
- Treat `results/finish/sambamba_flagstat.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/sambamba_flagstat.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bamCoverage` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/sambamba_flagstat.done` exists and `bamCoverage` can proceed without re-running sambamba flagstat.
