# Evaluation V2 — lenient scoring rubric

This document describes the V2 evaluator that lives at
`tools/evaluate_real_run_v2.py`. The V1 evaluator at
`tools/evaluate_real_run.py` is **not touched**; it remains the legacy
baseline and is re-used from V2 to compute the `verdict_legacy` field so the
numbers stay apples-to-apples.

V2 takes inspiration from BixBench: rather than insisting on byte-level
equality, it grades each expected file on a tiered ladder of tolerant
comparisons and mixes in four trajectory-level process signals.

## Per-file score (∈ `[0.0, 1.0]`)

Each expected file (from `registry.real.json → evaluation.expected_files`)
is scored by trying the tiers below **in order**; the file's final score is
the best (highest) that succeeds.

1. **`byte_identical` = 1.00** — `sha256(agent) == sha256(ref)`.
2. **`normalized_text_equal` = 1.00** — for text files, after we:
   * strip BOM,
   * convert CRLF/CR → LF,
   * rstrip every line,
   * drop trailing blank lines.
   If the file parses as JSON we additionally compare after
   `json.dumps(sort_keys=True)`.
3. **`normalized_table_equal` = 1.00** — for CSV/TSV, after canonicalising
   with pandas (sort rows by the leftmost non-trivial non-numeric column,
   or by all columns lexicographically, then `to_csv(float_format='%.6g')`).
4. **`tabular_tolerance` ∈ `[0.50, 0.99]`** — column alignment (by name
   when enough names overlap, else positional), then each row is
   fingerprinted into a tolerance bucket per cell (`rtol=1e-3`, `atol=1e-5`),
   and we count multiset row overlap. `effective_fraction` drops this score
   linearly when fewer rows overlap; column-count mismatches multiply
   by `0.7 · col_overlap`. Anything below `0.50` is discarded and we
   fall through.
5. **`rds_semantic` ∈ `[0.50, 0.99]`** — for `.rds` files we call the R
   sidecar `evaluators/rds_sidecar.R` which dumps the object to TSV by
   dispatching on its class:

   | class | dump via |
   |-------|----------|
   | `data.frame` / `tbl_df` | `write.table` |
   | `matrix` | `as.data.frame` + `write.table` |
   | `methylRawList` / `methylBase*` / `methylRaw*` | `methylKit::getData` |
   | `DESeqDataSet` / `DESeqResults` / `DataFrame` / `SummarizedExperiment` | `as.data.frame` |
   | `list of data.frames/tibbles` | stacked with an `[i]` index column |
   | anything else | `capture.output(str(obj))` |

   The two TSVs are then fed through `tabular_tolerance`. The sidecar
   *always* exits 0 and writes a one-line diagnostic to stderr so an
   R failure can't crash the evaluator.
6. **`process_credit` = 0.25** — file exists, size > 0, and parses as the
   expected type, but no higher tier produced ≥ 0.25.
7. **`missing` / `parse_error` = 0.00**.

## Process signals (∈ `[0.0, 1.0]`)

Parsed from `trajectory.jsonl` + `metadata.json`. Each is 0 or 1; the four
are averaged to yield `process_mean`.

| signal | meaning |
|--------|---------|
| `tool_calls_executed_meaningful` | > 2 non-trivial tool calls (ignoring `list_workdir`, `read_workdir`, `read_plan`) |
| `rscript_invoked_and_exited_zero` | ≥ 1 `run_rscript` observation with `exit_code: 0` and no `Error`/`Execution halted`/`traceback` marker |
| `submit_done_called` | trajectory ever calls `submit_done(success=...)` (any value) |
| `outputs_dir_nonempty_and_valid` | `workspace/output/` contains ≥ 1 file with size > 0 |

## Overall score

```
overall_score = 0.30 · mean(process_signals) + 0.70 · mean(per_file_scores)
```

Missing expected files count as 0 in the file mean. If the task has no
expected files (shouldn't happen for real tasks), `overall_score` defaults
to `process_mean`.

## Verdicts

| verdict        | condition                                                                                 |
|----------------|-------------------------------------------------------------------------------------------|
| `pass`         | `overall_score ≥ 0.90`                                                                    |
| `partial_pass` | `0.60 ≤ overall_score < 0.90`                                                             |
| `partial_fail` | `0.30 ≤ overall_score < 0.60`                                                             |
| `fail`         | `overall_score < 0.30`                                                                    |
| `error`        | trajectory ended with an exception *and* `outputs/` is empty                              |

V1 verdicts are copied verbatim from `evaluate_real_run.py` and stored as
`verdict_legacy`; they are not re-derived. Passing `--legacy` makes the
CLI swap the primary `verdict` for `verdict_legacy` so tooling built on
V1 stays functional.

## CLI

```
python3 tools/evaluate_real_run_v2.py \
    --batch-run-id sweep_v2_none_20260416T173242Z \
    --batch-run-id sweep_v2_paper_20260416T173242Z \
    --per-file-json runs/_evaluations/sweep_v2_per_file.v2.json \
    --rds-helper tools/evaluators/rds_sidecar.R \
    --rtol 1e-3 --atol 1e-5
```

Outputs:

* `runs/_evaluations/<batch>.v2.json` — machine-readable summary with
  `evaluator_version`, `verdict_counts`, `verdict_counts_legacy`, per-task
  `overall_score`, `process_signals`, `per_file[]`.
* `runs/_evaluations/<batch>.v2.md` — human-readable table with strategy
  summary per task and per-file detail.
* `--per-file-json` optionally flattens all per-file rows into a single
  array (useful for BI / cross-arm analysis).

## Tolerance defaults

`rtol=1e-3`, `atol=1e-5` are the defaults. Rationale:

* `1e-3` relative accommodates typical DESeq2/normalised-counts
  floating-point jitter that shows up when runs use slightly different
  BLAS/LAPACK builds or R versions.
* `1e-5` absolute catches near-zero values where relative tolerance
  collapses.

If you tighten tolerance (e.g. `--rtol 1e-6`) you should see V2 scores
collapse toward V1 verdicts; loosening further (`--rtol 1e-2`) tends to
cross into the "permissive" territory we explicitly want to avoid.

## Dependencies

* Python stdlib
* `pandas`, `numpy`, `pyyaml`
* `Rscript` + whatever R packages your RDS outputs actually need
  (`methylKit`, `DESeq2`, `tibble` were sufficient for the V2 sweep).

There is no LLM-as-judge, no network access, and no hidden state.
