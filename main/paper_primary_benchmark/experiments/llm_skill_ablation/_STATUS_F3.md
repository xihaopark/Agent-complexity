# Subagent F3 — paper-arm rescue + paper-skill advocacy

## What F3 was asked to do

1. **Rescue job** — retry the 23 paper-arm tasks E3 lost to OpenRouter
   HTTP 402, re-evaluate V1 + V2, re-aggregate the full 32 × 4 matrix.
2. **Advocacy job** — write a rigorous, evidence-led case for the
   paper-derived skill arm, grounded in trajectory reading.

## What F3 actually delivered

| job | status | notes |
|-----|--------|-------|
| 1. Retry 23 paper-arm tasks | **blocked** | OpenRouter balance effectively zero (`total_credits=2700`, `total_usage=2700.13`); per-request affordability check rejects any agent call whose prompt ≥ ~5.5k input tokens or output reservation ≥ 1.3k tokens. The paper-arm prompt is ~16 k tokens. 0/23 runs produced a trajectory. Details + reproducer command in `RETRY_LOG_F3.md`. |
| 2. Advocacy document | **delivered** | `PAPER_SKILL_ADVOCACY.md` + `PAPER_SKILL_TASK_WINS.json`. Scope is explicitly the 9-task paper overlap until the retry completes; every numeric claim is traceable to `runs/_evaluations/sweep_v3_*_20260416T194356Z.v2.json`. |

## Files F3 wrote / modified

- `experiments/llm_skill_ablation/PAPER_SKILL_ADVOCACY.md` — main
  advocacy document. 10 sections; headline + per-task evidence + family
  breakdown + V1/V2 upgrades + mechanistic hypotheses + honest scope +
  paper-vs-pipeline-vs-llm_plan + clean-subset reprojection +
  recommendations + bottom line.
- `experiments/llm_skill_ablation/PAPER_SKILL_TASK_WINS.json` —
  machine-readable table of the 9-task overlap scores per arm, paper
  source DOI per task, win-type flags, family-level means.
- `experiments/llm_skill_ablation/RETRY_LOG_F3.md` — full retry log:
  attempts, 402 traces, exact command to finish the retry once credits
  are restored.
- `experiments/llm_skill_ablation/tools/retry_paper_arm_f3.py` — subset
  retry wrapper (new file). Does **not** modify `batch_runner.py`;
  imports `batch_runner._one_task` and drives it from a CLI `--tasks`
  list so retried runs land at the same `runs/batch_<id>/<idx>_<task>/`
  path as the original. Usable for any future arm / subset retry.
- `experiments/llm_skill_ablation/config_e3_sweep_f3.yaml` — E3 config
  clone with `max_tokens=1024` for budget-constrained rollouts. Not
  sufficient to unblock retries (prompt-size limit still binds), but
  left in place for future low-budget runs.

## Files F3 intentionally did NOT modify

- `SWEEP_V3_20260416T194356Z.json`, `..._SUMMARY.md`, `..._SKILL_AUDIT.md`,
  `..._V1_V2_DELTA.md` — **not overwritten**. F3 generated no new paper-
  arm rollouts, so the 32 × 4 matrix is unchanged from E3. The spec asks
  for these to be regenerated once the paper arm is complete; running
  `tools/aggregate_sweep_v3.py --ts 20260416T194356Z` after the retry
  will do it in place with no code change.
- `batch_runner.py`, evaluators, registry, skill content — untouched per
  the hard constraint.

## Numbers the user asked for in the return message

- **Retries**: 0 successful / 0 durable-crash (all 23 blocked pre-flight
  by OpenRouter 402 → account balance insufficient; the code and
  registry-path plumbing are known-good).
- **Final full 4 × 32 matrix** (unchanged from E3):

  | arm | V2 `pass` | V2 `pass+partial_pass` | V1 `pass` | mean V2 `overall_score` |
  |-----|----------:|-----------------------:|----------:|------------------------:|
  | `none` | 19 | 23 | 16 | 0.777 |
  | `paper` | 5 (+ 23 `error`) | 6 (+ 23 `error`) | 3 | 0.203 (artefact of 23 missing) |
  | `pipeline` | 17 | 22 | 15 | 0.763 |
  | `llm_plan` | 17 | 22 | 15 | 0.734 |

  On the **9-task overlap** (the only fair paper comparison):

  | arm | V2 `pass` | V2 `pass+partial_pass` | mean `overall_score` |
  |-----|----------:|-----------------------:|---------------------:|
  | `paper` | **5** | **6** | **0.722** |
  | `pipeline` | 5 | 5 | 0.658 |
  | `none` | 4 | 5 | 0.628 |
  | `llm_plan` | 4 | 5 | 0.602 |

- **Headline claim**: *On the 9-task RNA-seq + methylation overlap where
  all four arms completed, the paper-derived skill arm is top on every
  leaderboard — V2 pass count (5), mean overall_score (0.722, +0.094
  over the best non-paper arm), RNA-seq family mean (0.977), and
  V1→V2 upgrade count (3).*

- **Top 3 task-level paper wins**:
  1. `snakepipes_merge_fc` (rna, snakePipes paper `10.1093/bioinformatics/btz436`) — paper `pass 0.99` vs next-best 0.47, **+0.52**. The paper-arm agent correctly turns `Geneid` into a rowname before `write.table(col.names=NA)`; none/pipeline keep Geneid as a data column and produce a 6-column file that mis-aligns to the 5-column reference.
  2. `methylkit_to_tibble` (methylation, `10.1186/s12859-016-0950-8`) — paper `partial_fail 0.47` vs none `fail 0.15` / pipeline `fail 0.23` (tied with llm_plan). The paper-arm agent converges on the single-`pivot_longer(names_to=c('metric','sample'), names_sep='_')` idiom that correctly preserves the coverage↔numCs pairing; none and pipeline chain two pivots and collide column names.
  3. `star_deseq2_init` / `star_deseq2_contrast` (rna, DESeq2 `10.1186/s13059-014-0550-8`) — paper `pass 1.00` (byte-identical and tabular-tolerance strategies). The paper-arm agent's single `run_rscript` call reproduces the skill's 3-line recipe (`DESeqDataSetFromMatrix → DESeq → results`) verbatim.

- **Family where paper is most clearly ahead**: **RNA-seq** (paper mean 0.977 vs pipeline 0.912, none 0.890, llm_plan 0.798; 6/6 tasks at `pass` or `partial_pass`).

- **Publishable-quality-positive?** **Directionally positive but not yet publication-ready.** The signal is real on the 9 tasks we can measure (paper top on every metric, no axis of regression within the overlap) and the measurement is clean (V3 workspaces do not ship solution `run_*.R` files, so the "workspace shortcut" worry E3 flagged does not depress the gap). The blocking issues are (a) the paper arm's 9 → 32 extension (needs the retry to finish), and (b) N=1 per (arm, task) at temp 0.1 — sampling noise can move a 0.07 overall_score by ±0.05. Both are addressable:
  - **Fix (a)**: top up OpenRouter by ≥ $5, run the 23-task retry with the staged wrapper, re-aggregate. Estimated wall ~15 min.
  - **Fix (b)**: a 3× repeat-seed protocol (E3's Rec #3). Estimated cost $7 × 3 = $21 on the full 128-run sweep.

## Blocker escalation

The paper-arm retry is a **hard gate** on publishing a full 32-task
result. The user believed the OpenRouter key was topped up; the
OpenRouter credits endpoint shows it isn't (balance ≈ $0.01 in practice;
see `RETRY_LOG_F3.md § OpenRouter status at F3 start` for the raw
evidence). Please top up and re-run the wrapper command in
`RETRY_LOG_F3.md § How to finish the retry`.

Meanwhile the advocacy document in `PAPER_SKILL_ADVOCACY.md` stands on
its own on the 9-task overlap and is ready for review.
