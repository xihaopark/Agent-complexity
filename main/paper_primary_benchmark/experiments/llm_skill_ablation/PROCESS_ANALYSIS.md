# V3 Sweep — Process-level Trajectory Analysis

- Sweep TS: `20260416T194356Z`
- Runs analysed: 105 (missing: 23)
- Source of walltime/cost: metadata.json does **not** contain `cost` or `wall_time_seconds`. `total_steps` from trajectory.jsonl is used as a proxy (same heuristic as the sweep summary).

## 1. Action profile per arm (means)

| arm | n | steps | rscript | read | write | shell | list_wd | submit_done | write_plan | check_prog | planning_used_frac |
|-----|---|------:|--------:|-----:|------:|------:|--------:|------------:|-----------:|-----------:|-------------------:|
| `none` | 32 | 7.188 | 2.844 | 0.75 | 0.062 | 0.094 | 0.094 | 0.844 | 1.25 | 1.219 | 1.0 |
| `paper` | 9 | 8.222 | 3.556 | 1.222 | 0.111 | 0 | 0.111 | 0.778 | 1.222 | 1.222 | 1.0 |
| `pipeline` | 32 | 6.938 | 3.156 | 0.844 | 0.062 | 0.062 | 0.156 | 0.875 | 1.125 | 0.656 | 1.0 |
| `llm_plan` | 32 | 7.625 | 3.844 | 0.344 | 0.062 | 0.062 | 0.125 | 0.812 | 1.219 | 1.156 | 0.969 |

## 2. First action distribution

| arm | first-action histogram |
|-----|------------------------|
| `none` | `write_plan`:30, `read_text_file`:2 |
| `paper` | `write_plan`:9 |
| `pipeline` | `write_plan`:31, `read_text_file`:1 |
| `llm_plan` | `write_plan`:31, `list_workdir`:1 |

## 3. Skill-signal token usage

For each run we extract tokens (length≥4, stripped of stop-words) that appear in the injected skill text but NOT in `OBJECTIVE.md` or the files under `input/`, then count occurrences of those tokens in the agent's `run_rscript` / `run_shell` / `write_text_file` arguments. `none` has no injected skill so hits are trivially 0.

| arm | mean hits/run | median hits/run | runs_with_any_hit (frac) | mean distinct tokens/run |
|-----|--------------:|----------------:|-------------------------:|-------------------------:|
| `none` | 0 | 0.0 | 0.0 | 0 |
| `paper` | 0.444 | 0 | 0.222 | 0.444 |
| `pipeline` | 8.562 | 3.0 | 0.688 | 3.375 |
| `llm_plan` | 43.312 | 16.0 | 1.0 | 12.656 |

Top 10 skill-unique tokens the agent actually wrote into its own code, per arm:

| arm | top tokens (token × runs_hit) |
|-----|-------------------------------|
| `none` | — |
| `paper` | `necessary`×1, `colData`×1, `DESeqDataSetFromMatrix`×1, `countData`×1 |
| `pipeline` | `length`×27, `Load`×21, `dplyr`×18, `mutate`×16, `tidyr`×13, `return`×13, `coverage`×13, `percMethylation`×13, `fread`×9, `frame`×7 |
| `llm_plan` | `dplyr`×36, `Save`×28, `Read`×28, `rename`×23, `select`×23, `Define`×21, `readRDS`×19, `statistics`×19, `frame`×18, `Create`×18 |

## 4. Error recovery

A `run_rscript` is called "errored" when the next observation starts `exit=<nonzero>`. Recovery = the agent subsequently issues another `run_rscript` whose next observation starts `exit=0`. `mean_recovery_gap` is averaged only over errors that were actually recovered; many runs time out with errors still unrecovered (captured separately).

| arm | mean rscript errors/run | mean recovery gap (steps) | total unrecovered errors |
|-----|------------------------:|--------------------------:|-------------------------:|
| `none` | 1.812 | 1.938 | 41 |
| `paper` | 2.333 | 2.75 | 17 |
| `pipeline` | 1.938 | 1.659 | 35 |
| `llm_plan` | 2.562 | 2.304 | 56 |

## 5. First `run_rscript` code style

| arm | mean LOC | `%>%` | `|>` | data.table refs | base-R refs |
|-----|---------:|------:|-----:|----------------:|------------:|
| `none` | 12.226 | 1.484 | 0 | 0.323 | 1.613 |
| `paper` | 10.111 | 1 | 0 | 0 | 1.333 |
| `pipeline` | 10.968 | 1.129 | 0 | 0.258 | 1.323 |
| `llm_plan` | 10.844 | 1.156 | 0 | 0.25 | 1.406 |

## 6. Run duration / cost

metadata.json did not capture `cost` or `wall_time_seconds` on this sweep (no `cost` / `wall_time` keys anywhere across 105 metadata files). The proxy is `total_steps` — which mirrors the best-effort estimate in `SWEEP_V3_20260416T194356Z_SUMMARY.md` (there the estimate was ~2.7k in / 0.25k out tokens per step × GPT-4o list price).

| arm | total steps (sum) | mean steps/run | est. USD (sweep summary) |
|-----|------------------:|---------------:|-------------------------:|
| `none` | 230 | 7.188 | $2.013 |
| `paper` | 74 | 8.222 | $0.684 |
| `pipeline` | 222 | 6.938 | $2.054 |
| `llm_plan` | 244 | 7.625 | $2.257 |

## 7. Failure-mode classification (V2 fail + partial_fail + error)

| arm | failure-mode histogram |
|-----|------------------------|
| `none` | `infinite_loop_debug`:4, `wrong_values`:3, `rscript_crashed`:1, `partial_output_mismatch`:1 |
| `paper` | `infinite_loop_debug`:3 |
| `pipeline` | `wrong_values`:6, `infinite_loop_debug`:4 |
| `llm_plan` | `infinite_loop_debug`:6, `wrong_values`:2, `rscript_crashed`:1, `partial_output_mismatch`:1 |

## 8. Scatter: overall_score vs total_steps (per arm)

ASCII bin-plot, x=total_steps bucketed 0-4/5-9/10-14/15+, y=mean_overall_score.

| arm | 0-4 steps | 5-9 | 10-14 | 15+ |
|-----|----------:|----:|------:|----:|
| `none` | 0.97(n=4) | 0.90(n=21) | 0.47(n=2) | 0.23(n=5) |
| `paper` | 0.94(n=2) | 1.00(n=4) | — | 0.21(n=3) |
| `pipeline` | 1.00(n=4) | 0.83(n=23) | 0.65(n=1) | 0.17(n=4) |
| `llm_plan` | 0.90(n=12) | 0.84(n=12) | 0.95(n=2) | 0.10(n=6) |

## 9. Top 5 paper-arm unique behaviours

We compare the 9 completed paper-arm runs against the matching runs on the other three arms (same `task_id`). Evidence cited as `batch_sweep_v3_<arm>_20260416T194356Z/<idx>_<task_id>/trajectory.jsonl#t<timestep>`.

1. **`write_text_file` + `source()` pattern is over-represented in paper runs.** On the 9 overlap tasks paper's first `run_rscript` has mean LOC=10.1 vs none=11.3 / pipeline=12.9 / llm_plan=11.4; paper's first rscript is sometimes just `source('workspace/filter_and_deseq2.R')` after a preceding `write_text_file` call — e.g. `batch_sweep_v3_paper_.../000_akinyi_deseq2/trajectory.jsonl#t2` writes the full DESeq2 R script to a file and t=3 executes it via `source()`. Total `write_text_file` tool-calls: paper 1 (in 9 runs) vs none 2 (in 32 runs) — paper is more likely to externalise its code as a file before execution.
2. **Paper skill tokens rarely surface in R code.** Across the 9 paper runs only 2 runs wrote any skill-unique token (`akinyi_deseq2` hit 1 token — just the prose filler `necessary`; `star_deseq2_init` hit `DESeqDataSetFromMatrix`, `countData`, `colData`). The paper skill's distinctive tokens (`RPKM`, `FPKM`, `TPM`, `edgeR`, `Poisson`, `binomial`, `HTSeq`) never appear in any paper-arm generated code. `batch_sweep_v3_paper_.../000_akinyi_deseq2/trajectory.jsonl` → tokens ['necessary']; `batch_sweep_v3_paper_.../001_star_deseq2_init/trajectory.jsonl` → tokens ['colData', 'DESeqDataSetFromMatrix', 'countData']
3. **Paper agents error the *least* on the overlap, but still lose methylKit.** On the 9-task overlap mean rscript-error count is paper=2.33, none=3.22, pipeline=3.78, llm_plan=4.11. However on the methylKit trio (`methylkit_load` / `methylkit_unite` / `methylkit_to_tibble`) paper still produces 6+ rscript errors per task because the paper skill gives no methylKit-specific hint. See `batch_sweep_v3_paper_.../003_methylkit_load/trajectory.jsonl#t1..t14` — 11 consecutive rscript errors with no recovery path.
4. **Every paper-arm run opens with `write_plan`.** On the 9 paper runs `write_plan` is the first action 9/9 times and `write_plan`+`check_progress` fire in 9/9 runs (vs none 9/9, pipeline 9/9, llm_plan 8/9). There is no divergence in planning behaviour by arm — all four arms hit the plan tool near-universally, which undercuts any story that paper injection changes meta-reasoning style.
5. **Concrete behavioural win cases.** Paper-arm beats none on: `methylkit_to_tibble` paper=0.47 vs none=0.15; `snakepipes_merge_fc` paper=0.99 vs none=0.47. Best-documented behavioural delta is `snakepipes_merge_fc` (paper 0.99 vs none 0.47): both arms' agents follow identical tool-call skeletons (write_plan → read_text_file → run_rscript → check_progress → submit_done at t=0..4). The *only* meaningful difference is inside the first `run_rscript` — paper writes `rownames(merged_counts) <- merged_counts$Geneid; merged_counts <- merged_counts %>% select(-Geneid)` before `write.table(..., col.names=NA)`, while none writes `colnames(...) <- c('Geneid', 'sampleA', ...)` and keeps Geneid as a regular column. The reference output was written with rownames, so the paper arm gets `byte_identical` scoring and none does not. Cite `batch_sweep_v3_paper_.../008_snakepipes_merge_fc/trajectory.jsonl#t2` vs `batch_sweep_v3_none_.../008_snakepipes_merge_fc/trajectory.jsonl#t2`.

## 10. Top 5 llm_plan-arm failure patterns

llm_plan ended up tied with pipeline at 17/32 V2-pass but landed at lower mean_score (0.734). From trajectories, the pattern is consistent:

Failure-mode histogram: {'infinite_loop_debug': 6, 'wrong_values': 2, 'rscript_crashed': 1, 'partial_output_mismatch': 1}

**1. Repeat-identical-rscript loop (6 runs).** The agent issues the same failing `run_rscript` 10+ times with no code changes — e.g. `snakepipes_merge_fc` loops identical `list.files + full_join` code at exit=1 from t=1 through t=14. Cite `batch_sweep_v3_llm_plan_.../008_snakepipes_merge_fc/trajectory.jsonl#t1..t14`. The injected LLM-plan skill is extremely prescriptive about the plan but offers no recovery heuristic, so when its first proposal crashes the agent has nothing else to try.
**2. Skipping `OBJECTIVE.md` inspection (1 failing runs).** llm_plan is the only arm where a run starts with `list_workdir` instead of `write_plan` (`snakepipes_merge_fc` t=0). Across all 32 llm_plan runs the agent only issues `read_text_file` with mean 0.34/run — barely a third of paper's (1.22/run). The LLM-plan skill already re-summarises the objective, so the model appears to skip the real OBJECTIVE and trust the plan — including when the plan omits a detail from OBJECTIVE.
**3. methylkit family crashes (4 runs).** The llm_plan skill for `methylkit_load` hardcodes `methRead(file_paths, ...)` where `file_paths <- c(...)` — methRead actually requires `list(...)` for multi-file input, so the agent's first rscript crashes and the skill offers no corrective hint. Cite `batch_sweep_v3_llm_plan_.../003_methylkit_load/trajectory.jsonl#t1..t14`.
**4. Budget exhaustion at max_steps=15 (6 of the 10 failing runs).** These are the same runs that never call `submit_done`. The summary's step budget of 15 is hit disproportionately on llm_plan — across the 32 runs the arm has the highest total step count (244) and largest n_rscript/run (mean 3.84) among all four arms.
**5. Schema-mismatch on otherwise-correct output (2 wrong_values runs).** For `longseq_deseq2_init` (scored 0.72 / partial_pass) llm_plan's first rscript uses the right normalization pipeline (`DESeq(dds)` + `counts(dds, normalized=TRUE)`) but writes `write.table(..., row.names=FALSE)` — stripping gene IDs from the output. The LLM-plan skill fails to specify row-name handling, so the agent defaults to `FALSE`. Cite `batch_sweep_v3_llm_plan_.../006_longseq_deseq2_init/trajectory.jsonl#t1`. This is the same failure mode as the `snakepipes_merge_fc` none-arm bug — the non-llm-plan arms happened to guess rownames correctly more often.

## 11. Key finding — does paper-arm actually incorporate skill tokens?

**No — paper's lift is almost entirely from prompt framing, not from skill-token adoption.** Paper-arm runs that incorporate any skill-unique token into their own generated code: **22%** (n=9), with a mean of 0.44 hits/run. pipeline = 69% (mean 8.56/run), llm_plan = 100% (mean 43.31/run).

The paper skills are prose describing methodology in biological-paper language (`RPKM`, `FPKM`, `TPM`, `edgeR`, `Poisson`, `negative binomial`, `HTSeq`) which essentially never appears in the agent's R code. The *one* place paper-arm's behaviour demonstrably changes is schema-level details of `write.table` / rownames handling (see §9 bullet 5) — consistent with the interpretation that paper skill acts as a *soft prompt* reminding the LLM that 'this is RNA-seq best practices' rather than as a concrete code recipe. The pipeline and llm_plan skills, by contrast, include verbatim R snippets (`dplyr`, `mutate`, `readRDS`, `DESeqDataSetFromMatrix`, `methRead(treatment=c(0,0,0))`) which the agent copies directly — the skill-token hit rate reflects this: 69% / 100% of runs have at least one direct copy-through.

**Caveats on the skill-token metric.** (a) the paper arm has n=9 (23 runs crashed on OpenRouter HTTP 402); the 22% figure is computed across the 9 completed runs only. (b) a token is classed as skill-unique if it is in the skill text but not in OBJECTIVE.md / input/ — it may still be a token the model would produce on its own (e.g. `DESeqDataSetFromMatrix` appears in both paper-arm *and* none-arm generated code for `star_deseq2_init`, so counting it as a 'skill-token hit' on paper overstates the skill's influence). The relative ordering paper < pipeline < llm_plan is still valid because the higher-ranked skills include verbatim R snippets the agent demonstrably parrots (see §3 top-tokens: `percMethylation` / `as_tibble` / `readRDS` appear in code only when those skills inject them).
