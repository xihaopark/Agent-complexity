---
name: finish-mohammedemamkhattabunipd-atacseq-primary_atacseq
description: Use this skill when orchestrating the retained "primary_atacseq" step of the mohammedemamkhattabunipd atacseq finish finish workflow. It keeps the Primary ATACseq stage and the downstream handoff to `downstream_atacseq`. It tracks completion via `results/finish/primary_atacseq.done`.
metadata:
  workflow_id: mohammedemamkhattabunipd-atacseq-finish
  workflow_name: mohammedemamkhattabunipd atacseq finish
  step_id: primary_atacseq
  step_name: Primary ATACseq
---

# Scope
Use this skill only for the `primary_atacseq` step in `mohammedemamkhattabunipd-atacseq-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/mohammedemamkhattabunipd-atacseq-finish/steps/primary_atacseq.smk`
- Config file: `finish/mohammedemamkhattabunipd-atacseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/primary_atacseq.done`
- Representative outputs: `results/finish/primary_atacseq.done`
- Execution targets: `primary_atacseq`
- Downstream handoff: `downstream_atacseq`

## Guardrails
- Treat `results/finish/primary_atacseq.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/primary_atacseq.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `downstream_atacseq` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/primary_atacseq.done` exists and `downstream_atacseq` can proceed without re-running Primary ATACseq.
