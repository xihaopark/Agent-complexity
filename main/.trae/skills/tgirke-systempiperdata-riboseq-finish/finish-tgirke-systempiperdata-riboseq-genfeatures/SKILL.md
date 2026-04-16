---
name: finish-tgirke-systempiperdata-riboseq-genfeatures
description: Use this skill when orchestrating the retained "genFeatures" step of the tgirke systempiperdata riboseq finish finish workflow. It keeps the genFeatures stage tied to upstream `bam_IGV` and the downstream handoff to `featuretypeCounts`. It tracks completion via `results/finish/genFeatures.done`.
metadata:
  workflow_id: tgirke-systempiperdata-riboseq-finish
  workflow_name: tgirke systempiperdata riboseq finish
  step_id: genFeatures
  step_name: genFeatures
---

# Scope
Use this skill only for the `genFeatures` step in `tgirke-systempiperdata-riboseq-finish`.

## Orchestration
- Upstream requirements: `bam_IGV`
- Step file: `finish/tgirke-systempiperdata-riboseq-finish/steps/genFeatures.smk`
- Config file: `finish/tgirke-systempiperdata-riboseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/genFeatures.done`
- Representative outputs: `results/finish/genFeatures.done`
- Execution targets: `genFeatures`
- Downstream handoff: `featuretypeCounts`

## Guardrails
- Treat `results/finish/genFeatures.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/genFeatures.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `featuretypeCounts` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/genFeatures.done` exists and `featuretypeCounts` can proceed without re-running genFeatures.
