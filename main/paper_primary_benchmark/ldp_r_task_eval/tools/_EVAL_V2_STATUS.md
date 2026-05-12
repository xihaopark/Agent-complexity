# B3 status — V2 lenient evaluator

## What was built

* **New evaluator** `tools/evaluate_real_run_v2.py`
  * Same CLI shape as V1 (`--batch-run-id`, `--all`, `--registry`),
    plus `--legacy`, `--per-file-json`, `--rds-helper`, `--rtol`,
    `--atol`, `--output`, `--quiet`.
  * Emits `<batch>.v2.json` + `<batch>.v2.md` under
    `runs/_evaluations/`.
  * JSON schema:
    ```
    batch_run_id, ts, evaluator_version:"v2", rtol, atol, legacy_active,
    n_tasks, mean_score,
    verdict_counts        -- V2 keys: pass / partial_pass / partial_fail / fail / error
    verdict_counts_legacy -- V1 keys: pass / partial / fail
    tasks: {task_id: {overall_score, verdict, verdict_legacy,
                       process_signals, process_mean, process_counts,
                       file_scores_mean, per_file: [...], ...}}
    per_file[]: {filename, expected_path, got_path, strategy_used,
                  strategy_score, bytes_identical, size_agent, size_ref,
                  notes, details}
    ```
* **Helper package** `tools/evaluators/`
  * `text_normalize.py` — BOM/CRLF/trailing-whitespace/blank-line
    normalisation + JSON canonicalisation.
  * `tabular.py` — pandas-based loader (sniff `\t,;|` or whitespace),
    canonical TSV form, and fingerprint-based tabular tolerance
    comparison (row multiset + cell overlap, `rtol=1e-3`, `atol=1e-5`).
  * `process_signals.py` — reads `trajectory.jsonl` to score the four
    process booleans and detect trajectory-level errors.
  * `rds_sidecar.R` — 53-line Rscript helper that dumps `.rds` objects
    to canonical TSVs (dispatches on `data.frame`, `matrix`,
    `methylRawList`/`methylBase*`, `DESeqDataSet`/`DESeqResults`,
    list-of-df, else `str()`). Always exits 0.
* **Docs** `tools/EVALUATION_V2.md` (≤ 3 pages, rubric + CLI).
* **V1 is not modified.** V2 imports V1's `evaluate_run_dir` directly to
  compute `verdict_legacy`, guaranteeing apples-to-apples comparisons.

## Coverage

Ran V2 against the 4 existing V2 sweep batches:

| batch_run_id                             | v2 path                                                           |
|------------------------------------------|-------------------------------------------------------------------|
| `sweep_v2_none_20260416T173242Z`         | `runs/_evaluations/sweep_v2_none_20260416T173242Z.v2.{json,md}`   |
| `sweep_v2_paper_20260416T173242Z`        | `runs/_evaluations/sweep_v2_paper_20260416T173242Z.v2.{json,md}`  |
| `sweep_v2_pipeline_20260416T173242Z`     | `runs/_evaluations/sweep_v2_pipeline_20260416T173242Z.v2.{json,md}` |
| `sweep_v2_llm_plan_20260416T173242Z`     | `runs/_evaluations/sweep_v2_llm_plan_20260416T173242Z.v2.{json,md}` |
| flattened per-file                       | `runs/_evaluations/sweep_v2_per_file.v2.json`                     |

V2 lift vs V1 (from `experiments/llm_skill_ablation/EVAL_V1_VS_V2_DELTA.md`):

| arm       | V1 pass/partial/fail | V2 pass/partial_pass/partial_fail/fail/error | V2 mean |
|-----------|-----------------------|------------------------------------------------|---------|
| none      | 2 / 2 / 2             | 3 / 1 / 0 / 2 / 0                              | 0.667   |
| paper     | 3 / 2 / 1             | 4 / 0 / 1 / 1 / 0                              | 0.757   |
| pipeline  | 3 / 0 / 3             | 3 / 0 / 0 / 3 / 0                              | 0.562   |
| llm_plan  | 2 / 2 / 2             | 3 / 1 / 0 / 2 / 0                              | 0.632   |

## Known gaps

* **No heuristic normalisation for leading index columns.** We chose to
  flag header-only diffs (`""` vs `"gene"`) as tabular_tolerance with
  a 0.99 cap instead of silently rewriting headers. Fine by V2 design,
  but A3 should normalise these at task-registry time (see
  `EVAL_V1_VS_V2_DELTA.md` §Takeaways).
* **R sidecar adds ~5–10 s per RDS file** on first call
  (`methylKit` namespace load). No caching layer; with 30 tasks and ≤ 2
  RDS files per task this totals ~10 min in the worst case.
* **`rds_semantic` only handles the classes enumerated in the switch.**
  Anything else falls through to `capture.output(str(obj))` → text
  comparison, which is brittle. Extend the sidecar if/when new task
  families introduce S4 classes we care about (e.g. Seurat).
* **Trajectory parser is best-effort.** `rscript_invoked_and_exited_zero`
  regexes for `exit_code: 0`; a run that emits exit code via stdout in
  an unusual shape could false-negative. The current V2 sweep doesn't
  trigger this, but E3's new tasks should keep the `exit=0\nstdout:`
  preamble that `run_rscript` already produces.
* **No image/plot comparison.** V2 doesn't score PNG/PDF/SVG outputs
  (they get `process_credit` at best). If E3 adds visual outputs,
  consider adding a perceptual-hash tier.

## Recommended calls for E3

1. Run the full sweep with V2:
   ```
   python3 tools/evaluate_real_run_v2.py \
       --all \
       --per-file-json runs/_evaluations/e3_per_file.v2.json
   ```
2. Keep V1 alive — every JSON already carries `verdict_legacy` so the
   existing sweep summariser in `experiments/llm_skill_ablation/tools/`
   can keep reading the old V1 JSON while migrating.
3. For any task that regresses from `pass` under V2, first verify with
   `--legacy` — if V1 also flips, the regression is real.
4. Tolerances: stay with the defaults `rtol=1e-3, atol=1e-5`. They were
   picked to span typical DESeq2/methylKit float jitter without letting
   genuinely wrong outputs score above `0.50`.
5. Ask A3 to pre-apply two tiny normalisations to reference outputs:
   * Name the first column `gene` (or `"row"` / `"feature"`) rather
     than leaving it empty.
   * Strip `db_path` from `unite_stats.tsv` (it leaks a local path into
     the canonical output and prevents byte-identical matches across
     machines).
6. Plug V2 JSON into the sweep summariser as `evaluator_version == "v2"`
   and keep a `verdict_v1` column during the transition.
