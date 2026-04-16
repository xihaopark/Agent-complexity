---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-get_pfam
description: Use this skill when orchestrating the retained "get_pfam" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the get pfam stage tied to upstream `get_transcript_info` and the downstream handoff to `convert_pfam`. It tracks completion via `results/finish/get_pfam.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: get_pfam
  step_name: get pfam
---

# Scope
Use this skill only for the `get_pfam` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `get_transcript_info`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/get_pfam.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_pfam.done`
- Representative outputs: `results/finish/get_pfam.done`
- Execution targets: `get_pfam`
- Downstream handoff: `convert_pfam`

## Guardrails
- Treat `results/finish/get_pfam.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_pfam.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `convert_pfam` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_pfam.done` exists and `convert_pfam` can proceed without re-running get pfam.
