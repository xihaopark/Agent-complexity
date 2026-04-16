---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-kallisto_long_index
description: Use this skill when orchestrating the retained "kallisto_long_index" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the kallisto long index stage tied to upstream `get_main_transcripts_fasta` and the downstream handoff to `kallisto_long_bus`. It tracks completion via `results/finish/kallisto_long_index.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: kallisto_long_index
  step_name: kallisto long index
---

# Scope
Use this skill only for the `kallisto_long_index` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `get_main_transcripts_fasta`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/kallisto_long_index.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/kallisto_long_index.done`
- Representative outputs: `results/finish/kallisto_long_index.done`
- Execution targets: `kallisto_long_index`
- Downstream handoff: `kallisto_long_bus`

## Guardrails
- Treat `results/finish/kallisto_long_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/kallisto_long_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `kallisto_long_bus` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/kallisto_long_index.done` exists and `kallisto_long_bus` can proceed without re-running kallisto long index.
