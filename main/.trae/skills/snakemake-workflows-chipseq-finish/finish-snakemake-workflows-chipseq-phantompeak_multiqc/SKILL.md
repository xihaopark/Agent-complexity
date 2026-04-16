---
name: finish-snakemake-workflows-chipseq-phantompeak_multiqc
description: Use this skill when orchestrating the retained "phantompeak_multiqc" step of the snakemake workflows chipseq finish finish workflow. It keeps the phantompeak multiqc stage tied to upstream `phantompeak_correlation` and the downstream handoff to `plot_fingerprint`. It tracks completion via `results/finish/phantompeak_multiqc.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: phantompeak_multiqc
  step_name: phantompeak multiqc
---

# Scope
Use this skill only for the `phantompeak_multiqc` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `phantompeak_correlation`
- Step file: `finish/chipseq-finish/steps/phantompeak_multiqc.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/phantompeak_multiqc.done`
- Representative outputs: `results/finish/phantompeak_multiqc.done`
- Execution targets: `phantompeak_multiqc`
- Downstream handoff: `plot_fingerprint`

## Guardrails
- Treat `results/finish/phantompeak_multiqc.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/phantompeak_multiqc.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_fingerprint` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/phantompeak_multiqc.done` exists and `plot_fingerprint` can proceed without re-running phantompeak multiqc.
