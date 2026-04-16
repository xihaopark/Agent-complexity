---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-cutadapt_pipe
description: Use this skill when orchestrating the retained "cutadapt_pipe" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the cutadapt pipe stage tied to upstream `get_sra` and the downstream handoff to `cutadapt_pe`. It tracks completion via `results/finish/cutadapt_pipe.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: cutadapt_pipe
  step_name: cutadapt pipe
---

# Scope
Use this skill only for the `cutadapt_pipe` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `get_sra`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/cutadapt_pipe.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/cutadapt_pipe.done`
- Representative outputs: `results/finish/cutadapt_pipe.done`
- Execution targets: `cutadapt_pipe`
- Downstream handoff: `cutadapt_pe`

## Guardrails
- Treat `results/finish/cutadapt_pipe.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/cutadapt_pipe.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `cutadapt_pe` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/cutadapt_pipe.done` exists and `cutadapt_pe` can proceed without re-running cutadapt pipe.
