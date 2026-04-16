---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-get_transcript_info
description: Use this skill when orchestrating the retained "get_transcript_info" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the get transcript info stage tied to upstream `get_annotation` and the downstream handoff to `get_pfam`. It tracks completion via `results/finish/get_transcript_info.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: get_transcript_info
  step_name: get transcript info
---

# Scope
Use this skill only for the `get_transcript_info` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `get_annotation`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/get_transcript_info.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_transcript_info.done`
- Representative outputs: `results/finish/get_transcript_info.done`
- Execution targets: `get_transcript_info`
- Downstream handoff: `get_pfam`

## Guardrails
- Treat `results/finish/get_transcript_info.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_transcript_info.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_pfam` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_transcript_info.done` exists and `get_pfam` can proceed without re-running get transcript info.
