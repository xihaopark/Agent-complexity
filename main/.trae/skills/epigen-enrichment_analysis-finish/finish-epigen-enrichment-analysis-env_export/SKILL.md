---
name: finish-epigen-enrichment-analysis-env_export
description: Use this skill when orchestrating the retained "env_export" step of the epigen enrichment_analysis finish finish workflow. It keeps the env export stage tied to upstream `config_export` and the downstream handoff to `gene_ORA_GSEApy`. It tracks completion via `results/finish/env_export.done`.
metadata:
  workflow_id: epigen-enrichment_analysis-finish
  workflow_name: epigen enrichment_analysis finish
  step_id: env_export
  step_name: env export
---

# Scope
Use this skill only for the `env_export` step in `epigen-enrichment_analysis-finish`.

## Orchestration
- Upstream requirements: `config_export`
- Step file: `finish/epigen-enrichment_analysis-finish/steps/env_export.smk`
- Config file: `finish/epigen-enrichment_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/env_export.done`
- Representative outputs: `results/finish/env_export.done`
- Execution targets: `env_export`
- Downstream handoff: `gene_ORA_GSEApy`

## Guardrails
- Treat `results/finish/env_export.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/env_export.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `gene_ORA_GSEApy` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/env_export.done` exists and `gene_ORA_GSEApy` can proceed without re-running env export.
