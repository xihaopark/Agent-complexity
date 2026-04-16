---
name: finish-epigen-300bcg-atacseq-pipeline-parse_regulatory_build
description: Use this skill when orchestrating the retained "parse_regulatory_build" step of the epigen 300bcg atacseq_pipeline finish finish workflow. It keeps the Parse Regulatory Build stage tied to upstream `prepare_references` and the downstream handoff to `prepare_pipeline_input`. It tracks completion via `results/finish/parse_regulatory_build.done`.
metadata:
  workflow_id: epigen-300bcg-atacseq_pipeline-finish
  workflow_name: epigen 300bcg atacseq_pipeline finish
  step_id: parse_regulatory_build
  step_name: Parse Regulatory Build
---

# Scope
Use this skill only for the `parse_regulatory_build` step in `epigen-300bcg-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `prepare_references`
- Step file: `finish/epigen-300bcg-atacseq_pipeline-finish/steps/parse_regulatory_build.smk`
- Config file: `finish/epigen-300bcg-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/parse_regulatory_build.done`
- Representative outputs: `results/finish/parse_regulatory_build.done`
- Execution targets: `parse_regulatory_build`
- Downstream handoff: `prepare_pipeline_input`

## Guardrails
- Treat `results/finish/parse_regulatory_build.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/parse_regulatory_build.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `prepare_pipeline_input` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/parse_regulatory_build.done` exists and `prepare_pipeline_input` can proceed without re-running Parse Regulatory Build.
