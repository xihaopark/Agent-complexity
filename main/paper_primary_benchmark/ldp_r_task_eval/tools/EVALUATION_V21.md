# Evaluator V2.1 — Upgrade notes

V2.1 patches three scoring gaps discovered during the first full 4-arm sweep
(`sweep_v3_{none,llm_plan,pipeline,paper_final}`).

## Motivation — what V2 got wrong

Survey of 39 `partial_fail`/`fail` cases across 4 arms showed:

| Task | ref | agent | cells matched | V2 score | V2 strategy | why it was wrong |
|---|---|---|---|---|---|---|
| `snakepipes_merge_ct` | 300×5 | 300×6 | 80% (1200/1500) | 0.475 | `process_credit` | col_penalty `0.7·(5/6)=0.583` tanked a ~0.80 match |
| `snakepipes_merge_fc` | 400×5 | 400×6 | 60% | 0.475 | `process_credit` | same issue |
| `chipseq_plot_homer_annot` | 3×9 | 7×4 | 75% (9/12) | 0.475 | `process_credit` | transposed schema + `effective_fraction=0.10 < 0.5` hard floor |
| `dea_limma` / `dea_results.csv` | 400×9 | 400×8 | 69% (2224/3200) | 0.475 | `process_credit` | same 0.5 floor |
| `nearest_gene` / `annotated.bed` | | | | 0.475 | `process_credit` | `.bed` not in `_TEXT_EXT`, load_table never called |

Root causes:

1. **`_MIN_TOLERANCE_SCORE = 0.50` hard floor** in `_score_tabular` discarded every partial match below 50% and collapsed it to 0 — then `process_credit` anchored at 0.25 lost the actual signal.
2. **`col_penalty = 0.7 · col_overlap`** (when column counts differ) was punitive even when the agent's schema is a *superset* of the reference (extra annotation column, etc.).
3. **`_TEXT_EXT`** missed common bioinformatics formats (`.bed`, `.bedgraph`, `.gff`, `.gtf`, `.vcf`).
4. **RDS sidecar** couldn't dump several S4 classes (methylRawList per-sample records, DESeqDataSet/SummarizedExperiment assay matrices, GRanges, DGEList) so they always fell to `str_fallback`.

## V2.1 changes

### 1. Continuous tabular scoring (`_score_tabular`)

Drop the 0.5 hard floor. Blend `effective_fraction` with a schema-aligned
`cell_match_fraction` signal and map linearly to `[0, 0.99]`:

```
blended = max(effective_fraction, 0.85 * cell_match_fraction)
score   = min(blended, 0.99)
```

A separate step still anchors any present file at `_PROCESS_CREDIT = 0.25`,
but it no longer *overrides* a non-zero tabular match.

### 2. Relaxed column penalty (`evaluators/tabular.py`)

```
if not cols_mismatch            : col_penalty = 1.00
elif covers_smaller_schema      : col_penalty = 0.95   # agent ⊇ ref
elif col_overlap >= 0.80        : col_penalty = 0.90
else                            : col_penalty = max(0.7 * col_overlap, 0.50)
```

Adding a single annotation column to a 5-column reference now costs 5% of the
score instead of 41%.

### 3. Broader text extensions

`_TEXT_EXT` now includes `.bed`, `.bedgraph`, `.gff`, `.gtf`, `.vcf` so tabular
bioinformatics formats go through the ladder instead of `process_credit`.

### 4. Richer RDS sidecar (`evaluators/rds_sidecar.R`)

Explicit handlers for:

- `methylRawList` → merge per-sample rows with a `sample_id` column.
- `DESeqResults`, `DataFrame` → `as.data.frame`.
- `DESeqDataSet`, `SummarizedExperiment` → dump `assay()` matrix with rownames.
- `GRanges` → `as.data.frame` via `GenomicRanges`.
- `DGEList` → dump `$counts` with gene IDs.
- list-of-matrix: row-bind with `__item__` tag.
- All numeric cells are rounded to 8 significant figures so identical
  objects serialised on different R builds don't drift.

## Impact (same 4-arm data, V2 → V2.1)

| arm       | mean V2 | mean V2.1 | Δ      | pass V2 | pass V2.1 |
|-----------|--------:|----------:|-------:|--------:|----------:|
| none      | 0.7769  | **0.8139** | +0.037 | 19      | 19        |
| llm_plan  | 0.7337  | **0.7839** | +0.050 | 17      | 18        |
| pipeline  | 0.7634  | **0.8177** | +0.054 | 17      | 17        |
| paper     | 0.7837  | **0.8155** | +0.032 | 21      | 21        |

- **No pass → fail regressions** on any arm (sanity preserved).
- Biggest gainers are tasks where agent added an annotation column or produced
  60-80% cell matches (was `process_credit` 0.25, now 0.50-0.83).
- Mean gap between arms compressed from 0.050 to 0.034 — V2 was systematically
  unfair to arms that got "mostly right".

## Compatibility

- `evaluator_version` is bumped from `v2` to `v2.1` in the JSON output.
- `verdict_legacy` / V1 replay unchanged.
- V3 insight layer (`evaluate_real_run_v3.py`) unchanged — its reports now
  reflect the richer tabular statistics automatically.

## How to run

```bash
cd main/paper_primary_benchmark
PYTHONPATH=/path/to/main python3 -m ldp_r_task_eval.tools.evaluate_real_run_v3 \
  --batch-run-id sweep_v3_paper_final \
  --output ldp_r_task_eval/runs/_evaluations_v21 \
  --quiet
```

The old V2 scores remain in `runs/_evaluations/` as a baseline.
