# epigen-spilterlize_integrate-finish LLM Execution Spec

## Purpose

- Source repository: `epigen__spilterlize_integrate`
- Source snakefile: `../workflow_candidates/epigen__spilterlize_integrate/workflow/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `split`
2. `filter_features`
3. `select_hvf`
4. `norm_edgeR`
5. `norm_cqn`
6. `norm_voom`
7. `integrate_limma`
8. `plot_cfa`
9. `plot_diagnostics`
10. `plot_heatmap`
11. `env_export`
12. `config_export`
13. `annot_export`
14. `all`
