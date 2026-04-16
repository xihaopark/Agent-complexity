---
name: finish-mohammedemamkhattabunipd-atacseq-downstream_atacseq
description: Use this skill when orchestrating the retained "downstream_atacseq" step of the mohammedemamkhattabunipd atacseq finish finish workflow. It keeps the Downstream ATACseq stage tied to upstream `primary_atacseq`. It tracks completion via `results/finish/downstream_atacseq.done`.
metadata:
  workflow_id: mohammedemamkhattabunipd-atacseq-finish
  workflow_name: mohammedemamkhattabunipd atacseq finish
  step_id: downstream_atacseq
  step_name: Downstream ATACseq
---

# Scope
Use this skill only for the `downstream_atacseq` step in `mohammedemamkhattabunipd-atacseq-finish`.

## Orchestration
- Upstream requirements: `primary_atacseq`
- Step file: `finish/mohammedemamkhattabunipd-atacseq-finish/steps/downstream_atacseq.smk`
- Config file: `finish/mohammedemamkhattabunipd-atacseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/downstream_atacseq.done`
- Representative outputs: `results/finish/downstream_atacseq.done`
- Execution targets: `downstream_atacseq`
- Downstream handoff: none

## Guardrails
- Treat `results/finish/downstream_atacseq.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/downstream_atacseq.smk` so the step remains separable and replayable inside the finish workflow.

## Done Criteria
Mark this step complete only when `results/finish/downstream_atacseq.done` exists and matches the intended step boundary.
