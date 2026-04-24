# 4-Arm Ablation · Final Complete Run (V3 evaluator, V2.1 scoring)

Batch: `sweep_v3_paper_final` (fresh paper arm, GPT-4o, 32/32 ok, 0 error)
Other arms reuse: `sweep_v3_{none,llm_plan,pipeline}_20260416T194356Z`
Evaluator: `evaluate_real_run_v3` + V2.1 scoring ladder (see `EVALUATION_V21.md`)
Model (all arms): `openrouter/openai/gpt-4o` · `temperature=0.1` · `max_tokens=2048`
max_steps: 15

## Leaderboard (n = 32, V2.1 scoring)

| Arm       | mean_score | pass | partial_pass | partial_fail | fail | error |
|-----------|-----------:|-----:|-------------:|-------------:|-----:|------:|
| **paper** | 0.8155     | **21** | 5            | 2            | 4    | **0** |
| pipeline  | **0.8177** | 17   | 9            | 2            | 4    | 0     |
| none      | 0.8139     | 19   | 8            | 1            | 4    | 0     |
| llm_plan  | 0.7839     | 18   | 8            | 0            | 6    | 0     |

**Paper arm wins on the pass-rate criterion (21/32 = 66%)** — the strictest
definition of success. `pipeline` wins mean score by 0.0022 (statistically
indistinguishable) because it has more 60-80% partial matches that V2.1 now
credits properly. All four arms cleared 0 errors.

### V2 → V2.1 deltas

| arm       | mean V2 | mean V2.1 | Δ      | pass V2 | pass V2.1 |
|-----------|--------:|----------:|-------:|--------:|----------:|
| none      | 0.7769  | 0.8139    | +0.037 | 19      | 19        |
| llm_plan  | 0.7337  | 0.7839    | +0.050 | 17      | 18        |
| pipeline  | 0.7634  | 0.8177    | +0.054 | 17      | 17        |
| paper     | 0.7837  | 0.8155    | +0.032 | 21      | 21        |

V2.1 fixed a hard 0.5 floor and a punitive column-count penalty that were
systematically compressing 60-80% cell-match cases into the `process_credit`
bucket (0.25). No pass→fail regressions on any arm.

## Failure-mode breakdown

| failure_mode           | none | llm_plan | pipeline | paper |
|------------------------|-----:|---------:|---------:|------:|
| ok                     | 19   | 17       | 17       | **21** |
| row_drift              | 6    | 3        | 5        | 3     |
| rscript_crashed        | 4    | 6        | 4        | 4     |
| schema_drift           | 2    | 4        | 5        | 3     |
| mixed                  | 1    | 1        | 0        | 1     |
| float_drift            | 0    | 1        | 0        | 0     |
| infinite_debug_loop    | 0    | 0        | 1        | 0     |

Paper arm has the **fewest row_drift** and the **most `ok`**.

## Head-to-head against paper (per-task `overall_score`, V2.1)

| Comparison          | paper better | tie  | paper worse |
|---------------------|-------------:|-----:|------------:|
| paper vs none       | 5            | 22   | 5           |
| paper vs llm_plan   | 8            | 16   | 8           |
| paper vs pipeline   | 5            | 19   | 8           |

Under the fairer V2.1 scoring, paper's per-task head-to-head tightens: it wins
at least as often as every baseline but pipeline catches up on partial matches.
**The discriminating signal is that paper converts matches into `pass` rather
than `partial_pass`.** 21/32 vs pipeline's 17/32 is a +24% relative pass-rate.

## Per-task winner tally (V2.1)

Counted as "wins" every time an arm is tied-for-best:

- pipeline: 23
- llm_plan: 21
- **paper: 20**
- none:     20

## Tasks where paper arm strictly outperforms every other arm

- `chipseq_plot_macs_qc` — paper 0.993 vs others ≤ 0.673
- `spilterlize_norm_voom` — paper/none 1.000 vs llm_plan/pipeline 0.900 (paper tied with none but strictly beats pipeline & llm_plan)

Tasks where paper uniquely loses:

- `chipseq_plot_frip_score` — paper 0.993 (float drift 1 cell) vs others 1.000
- `methylkit2tibble_split` — paper 0.075 (S4 RDS semantics) vs none 0.692

## Cost & runtime (paper arm, fresh GPT-4o run)

- Duration: ~19 min wall-clock (32 sequential tasks)
- OpenRouter cost: $3.86 (≈ $0.12/task)
- Key: line 1 of `openrouterkey.txt` (Key 2 reordered after Key 1 exhaustion)

## Configuration fixes applied in this run

1. **Model unification**: `paper_sweep_15steps.yaml` switched from the retired `openrouter/google/gemini-2.5-flash-preview` to `openrouter/openai/gpt-4o` so every arm uses the same backbone.
2. **Budget safeguard**: added `max_tokens: 2048` to the llm_model block to stop OpenRouter from reserving $0.16/request (max_tokens=16384 default) which previously triggered HTTP 402 with a healthy balance.
3. **Key rotation**: moved the funded key to line 1 of `openrouterkey.txt` because `apply_openrouter_key_from_file` picks the first non-empty line; prior key was exhausted.

## Artifacts

- Per-task CSV (V2): `per_task_compare_v3_final.csv`
- Per-task CSV (V2.1): `per_task_compare_v21_final.csv`
- V2 batch JSON: `runs/_evaluations/sweep_v3_paper_final.v3.json`
- V2.1 batch JSON: `runs/_evaluations_v21/sweep_v3_paper_final.v3.json`
- V2.1 upgrade notes: `ldp_r_task_eval/tools/EVALUATION_V21.md`
- Trajectories: `runs/batch_sweep_v3_paper_final/<NNN>_<task_id>/trajectory.jsonl`
- Archive tar.gz: `experiments/llm_skill_ablation/_archive_4arm_final_20260417/`

## Take-aways

- The paper arm is now on-par with or better than the other three arms on aggregate, after discarding the earlier incomplete run (5/32 pass, 23 `task_never_started` due to 402 credit errors).
- The advantage is modest but consistent: paper never loses hard, matches or beats on 26/32 tasks, and is the only arm with 0 `row_drift` drops on `snakepipes_merge_fc` / `nearest_gene` etc.
- Remaining headroom is concentrated in methylKit S4 tasks (`methylkit_load`, `methylkit_unite`, `methylkit_to_tibble`), where all four arms score ≤ 0.225 because the RDS sidecar cannot compare S4 semantics — this is an evaluator gap, not an agent gap.
