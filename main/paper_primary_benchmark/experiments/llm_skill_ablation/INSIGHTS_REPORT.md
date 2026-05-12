# Skill-arm Insights Report (V3 evaluator)

Batch timestamp: `20260416T194356Z`.  Source JSONs:

* `sweep_v3_none_20260416T194356Z.v3.json`
* `sweep_v3_paper_20260416T194356Z.v3.json`
* `sweep_v3_pipeline_20260416T194356Z.v3.json`
* `sweep_v3_llm_plan_20260416T194356Z.v3.json`

## 1 · Failure-mode distribution per arm

### Failure mode × arm

| arm | `ok` | `float_drift` | `row_drift` | `schema_drift` | `mixed` | `rscript_crashed` | `infinite_debug_loop` | `task_never_started` | total |
|-----|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `none` | 19 | 0 | 6 | 2 | 1 | 4 | 0 | 0 | 32 |
| `paper` | 5 | 0 | 2 | 0 | 0 | 2 | 0 | 23 | 32 |
| `pipeline` | 17 | 0 | 5 | 5 | 0 | 4 | 1 | 0 | 32 |
| `llm_plan` | 17 | 1 | 3 | 4 | 1 | 6 | 0 | 0 | 32 |

## 2 · Confidence grade distribution per arm

### Confidence × arm

| arm | `high` | `medium` | `low` | total |
|-----|---:|---:|---:|---:|
| `none` | 18 | 6 | 8 | 32 |
| `paper` | 27 | 2 | 3 | 32 |
| `pipeline` | 17 | 5 | 10 | 32 |
| `llm_plan` | 17 | 6 | 9 | 32 |

## 3 · Top 10 most-insightful task rows

Chosen deterministically by priority: paper-arm wins with non-empty skill token attribution > `no_rscript_call` / `infinite_debug_loop` > `rds_semantic_gap` / `float_drift` > other per-file modes with high skill coverage.

| # | task | arm | failure mode | actionable fix |
|--:|------|-----|--------------|-----------------|
| 1 | `methylkit2tibble_split` | `pipeline` | `infinite_debug_loop` | agent retried 7 times after first write; consider raising max_steps or injecting an explicit recipe |
| 2 | `star_deseq2_contrast` | `paper` | `ok` | no action needed |
| 3 | `star_deseq2_init` | `paper` | `ok` | no action needed |
| 4 | `snakepipes_scrna_qc` | `llm_plan` | `float_drift` | passes at V2 tolerance; regression only under strict byte compare |
| 5 | `akinyi_deseq2` | `pipeline` | `ok` | no action needed |
| 6 | `akinyi_deseq2` | `llm_plan` | `ok` | no action needed |
| 7 | `chipseq_plot_annotatepeaks_summary_homer` | `llm_plan` | `ok` | no action needed |
| 8 | `chipseq_plot_frip_score` | `llm_plan` | `ok` | no action needed |
| 9 | `chipseq_plot_peaks_count_macs2` | `llm_plan` | `ok` | no action needed |
| 10 | `clean_histoneHMM` | `llm_plan` | `ok` | no action needed |

## 4 · Cross-arm "same task, different failure mode" highlights

Found **15** tasks where the four arms disagree on failure mode (ignoring `task_never_started`). Highlights:

| task | mode by arm |
|------|-------------|
| `methylkit_to_tibble` | `none`=rscript_crashed, `paper`=row_drift, `pipeline`=rscript_crashed, `llm_plan`=schema_drift |
| `longseq_deseq2_init` | `none`=ok, `paper`=ok, `pipeline`=ok, `llm_plan`=schema_drift |
| `longseq_deseq2_contrast` | `none`=row_drift, `paper`=row_drift, `pipeline`=ok, `llm_plan`=ok |
| `snakepipes_merge_fc` | `none`=schema_drift, `paper`=ok, `pipeline`=schema_drift, `llm_plan`=rscript_crashed |
| `snakepipes_merge_ct` | `none`=ok, `pipeline`=schema_drift, `llm_plan`=rscript_crashed |
| `chipseq_plot_macs_qc` | `none`=row_drift, `pipeline`=schema_drift, `llm_plan`=schema_drift |
| `snakepipes_scrna_qc` | `none`=ok, `pipeline`=ok, `llm_plan`=float_drift |
| `spilterlize_filter_features` | `none`=ok, `pipeline`=row_drift, `llm_plan`=ok |
| `spilterlize_norm_voom` | `none`=ok, `pipeline`=row_drift, `llm_plan`=row_drift |
| `spilterlize_norm_edger` | `none`=ok, `pipeline`=ok, `llm_plan`=row_drift |
| `dea_limma` | `none`=mixed, `pipeline`=schema_drift, `llm_plan`=mixed |
| `methylkit_filt_norm` | `none`=rscript_crashed, `pipeline`=rscript_crashed, `llm_plan`=ok |
| `methylkit2tibble_split` | `none`=row_drift, `pipeline`=infinite_debug_loop, `llm_plan`=rscript_crashed |
| `nearest_gene` | `none`=row_drift, `pipeline`=row_drift, `llm_plan`=rscript_crashed |
| `epibtn_rpkm` | `none`=row_drift, `pipeline`=row_drift, `llm_plan`=ok |

### 4a · Signature cases

* **skill rescued an otherwise-crashing task** — `snakepipes_merge_fc`:
    - `none`: **schema_drift** (score 0.47) — produced 6 cols vs reference 5 (shared 5) on `merged_counts.tsv`
    - `paper`: **ok** (score 0.99) — no action needed
    - `pipeline`: **schema_drift** (score 0.47) — produced 6 cols vs reference 5 (shared 5) on `merged_counts.tsv`
    - `llm_plan`: **rscript_crashed** (score 0.07) — R error: Error in file(file, "rt") : invalid 'description' argument
* **skill rescued an otherwise-crashing task** — `snakepipes_merge_ct`:
    - `none`: **ok** (score 0.99) — no action needed
    - `pipeline`: **schema_drift** (score 0.47) — produced 6 cols vs reference 5 (shared 5) on `merged_tpm.tsv`
    - `llm_plan`: **rscript_crashed** (score 0.07) — R error: Error: '\.' is an unrecognized escape in character string (<input>:2:45)
* **skill flipped byte-match to tolerance-match** — `snakepipes_scrna_qc`:
    - `none`: **ok** (score 1.00) — no action needed
    - `pipeline`: **ok** (score 1.00) — no action needed
    - `llm_plan`: **float_drift** (score 0.65) — passes at V2 tolerance; regression only under strict byte compare
* **skill rescued an otherwise-crashing task** — `methylkit_filt_norm`:
    - `none`: **rscript_crashed** (score 0.15) — R error: Error in data.frame(sample = names(mk_norm), stats_df) :
    - `pipeline`: **rscript_crashed** (score 0.23) — R error: Error: unable to find an inherited method for function ‘percMethylation’ for signature ‘methylBase.o
    - `llm_plan`: **ok** (score 0.99) — no action needed
* **skill triggered an infinite debug loop** — `methylkit2tibble_split`:
    - `none`: **row_drift** (score 0.69) — cells matched 14/24 (58%) on `mean_mcpg_split.tsv`
    - `pipeline`: **infinite_debug_loop** (score 0.65) — agent retried 7 times after first write; consider raising max_steps or injecting an explicit recipe
    - `llm_plan`: **rscript_crashed** (score 0.23) — R error: Error in select(., chr, mCpG) : unused argument (mCpG)

## 5 · Skill-token attribution evidence

How often does a skill actually show up in the agent's tool-call arguments? V3 records matched tokens per task; the per-arm averages below show how code-actionable each skill source is.

| arm | mean tokens available | mean tokens matched | mean coverage |
|-----|----------------------:|--------------------:|--------------:|
| `none` | 0.0 | 0.00 | 0.0% |
| `paper` | 0.4 | 0.16 | 5.2% |
| `pipeline` | 30.2 | 2.97 | 9.9% |
| `llm_plan` | 13.6 | 11.84 | 87.9% |

The `paper` arm column is almost zero because vision-adapter skills are prose summaries — they contain almost no code-actionable tokens for the matcher to fire on. This is itself an insight: paper skills transmit *ideas*, not APIs.

## 6 · Recommended publication-ready figures

1. **Stacked bar — failure mode × arm.** X-axis = arm, Y-axis = task count, stacks coloured by failure mode. Source: `failure_mode_counts` in each `<batch>.v3.json`.
2. **Heatmap — task × arm, cell = failure mode.** One row per task, four columns. Helps the reader spot cross-arm disagreements. Source: `insights[task].failure_mode` per arm.
3. **Bar chart — paper-arm wins with skill-token coverage > 0.** Makes the "did the agent attend to the skill" question legible.
4. **CDF of `overall_score` per arm** overlaid with per-task failure-mode labels. Shows that V2 already separates arms by score, and V3 explains *why*.

---

Report generated by `tools/build_insights_report.py`. V3 evaluator: `main/paper_primary_benchmark/ldp_r_task_eval/tools/evaluate_real_run_v3.py`. Rubric: `.../tools/EVALUATION_V3.md`.