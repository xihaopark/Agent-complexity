---
name: finish-fritjoflammers-snakemake-methylanalysis-extract_cpgs
description: Use this skill when orchestrating the retained "extract_CpGs" step of the fritjoflammers snakemake methylanalysis finish finish workflow. It keeps the extract CpGs stage and the downstream handoff to `destrand_calls`. It tracks completion via `results/finish/extract_CpGs.done`.
metadata:
  workflow_id: fritjoflammers-snakemake-methylanalysis-finish
  workflow_name: fritjoflammers snakemake methylanalysis finish
  step_id: extract_CpGs
  step_name: extract CpGs
---

# Scope
Use this skill only for the `extract_CpGs` step in `fritjoflammers-snakemake-methylanalysis-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/fritjoflammers-snakemake-methylanalysis-finish/steps/extract_CpGs.smk`
- Config file: `finish/fritjoflammers-snakemake-methylanalysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/extract_CpGs.done`
- Representative outputs: `results/finish/extract_CpGs.done`
- Execution targets: `extract_CpGs`
- Downstream handoff: `destrand_calls`

## Guardrails
- Treat `results/finish/extract_CpGs.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/extract_CpGs.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `destrand_calls` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/extract_CpGs.done` exists and `destrand_calls` can proceed without re-running extract CpGs.
