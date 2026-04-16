# riyadua-cervical-cancer-snakemake-workflow-finish LLM Execution Spec

## Purpose

- Source repository: `RiyaDua__cervical-cancer-snakemake-workflow`
- Source snakefile: `../workflow_candidates/RiyaDua__cervical-cancer-snakemake-workflow/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `preprocess`
2. `differential_expression`
3. `all`
