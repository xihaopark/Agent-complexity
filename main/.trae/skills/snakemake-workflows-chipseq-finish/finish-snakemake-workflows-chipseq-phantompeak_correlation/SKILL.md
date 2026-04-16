---
name: finish-snakemake-workflows-chipseq-phantompeak_correlation
description: Use this skill when orchestrating the retained "phantompeak_correlation" step of the snakemake workflows chipseq finish finish workflow. It keeps the phantompeak correlation stage tied to upstream `phantompeakqualtools` and the downstream handoff to `phantompeak_multiqc`. It tracks completion via `results/finish/phantompeak_correlation.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: phantompeak_correlation
  step_name: phantompeak correlation
---

# Scope
Use this skill only for the `phantompeak_correlation` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `phantompeakqualtools`
- Step file: `finish/chipseq-finish/steps/phantompeak_correlation.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/phantompeak_correlation.done`
- Representative outputs: `results/finish/phantompeak_correlation.done`
- Execution targets: `phantompeak_correlation`
- Downstream handoff: `phantompeak_multiqc`

## Guardrails
- Treat `results/finish/phantompeak_correlation.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/phantompeak_correlation.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `phantompeak_multiqc` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/phantompeak_correlation.done` exists and `phantompeak_multiqc` can proceed without re-running phantompeak correlation.
