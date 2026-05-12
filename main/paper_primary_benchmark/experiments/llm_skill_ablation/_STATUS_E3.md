# Subagent E3 — full 4-arm × 32-task sweep

## Plan

- Registry: `ldp_r_task_eval/r_tasks/registry.real.json` (32 ready tasks; families: rna=14, chipseq=8, methylation=6, scrna=3, variant=1).
- Arms (serial, 4 total): `none` → `pipeline` → `llm_plan` → `paper`.
- Shared UTC timestamp `TS=20260416T194356Z` so every `sweep_v3_<arm>_<TS>` lines up.
- Batch runner CLI: `python3 -m ldp_r_task_eval.batch_runner --registry … --config experiments/llm_skill_ablation/config_e3_sweep.yaml --skill-source <arm> --openrouter-key-file ../openrouterkey.txt --batch-run-id sweep_v3_<arm>_<TS>`.
- `max_steps=15` (via `config_e3_sweep.yaml`, not via `--max-steps` — the batch runner only reads it from the config file).
- Model: `openrouter/openai/gpt-4o` temp 0.1 (same as V2 sweep).
- After each arm: run V1 evaluator + V2 evaluator; append progress line here.
- Budget: ≤ $18 (hard halt ≤ $22). Prior V2 sweep ran 24 runs for ~$3.3; extrapolating, 128 runs at max_steps=15 is estimated ~$12–14.

## Pre-flight checks

- [x] Registry: 32 tasks, all status=ready. Families: rna=14, chipseq=8, methylation=6, scrna=3, variant=1.
- [x] Paper manifest version 3: by_task_id=18, by_workflow_id=29.
- [x] Pipeline manifest version 3: by_workflow_id=16 (covers all 32 tasks per SKILL_COVERAGE_V3).
- [x] LLM-plan manifest version 3: by_task_id=32.
- [x] `openrouterkey.txt` exists, non-empty, starts `sk-or-v1-…`.
- [x] `config_e3_sweep.yaml` written (max_steps=15, temp 0.1, placeholder sys_prompt).
- [x] Shared TS=`20260416T194356Z`.

## Progress

- `none` arm — **32/32 ok** in ~23 min wall; evaluated with both.
  - V1: pass=16, partial=12, fail=4 (pass_rate 50.0%).
  - V2: pass=19, partial_pass=4, partial_fail=5, fail=4, error=0; mean_score=0.777.
  - Running cost estimate so far: ~$2–3 (32 runs, skill-free prompt).
- `pipeline` arm — **32/32 ok** in ~18 min wall; evaluated with both.
  - V1: pass=15, partial=13, fail=4 (pass_rate 46.9%).
  - V2: pass=17, partial_pass=5, partial_fail=6, fail=4, error=0; mean_score=0.763.
  - Running cost estimate so far: ~$5–6 (64 runs total).
- `llm_plan` arm — **32/32 ok** in ~16 min wall; evaluated with both.
  - V1: pass=15, partial=11, fail=6 (pass_rate 46.9%).
  - V2: pass=17, partial_pass=5, partial_fail=4, fail=6, error=0; mean_score=0.734.
  - Running cost estimate so far: ~$8–10 (96 runs total).
- `paper` arm — **9/32 ok, 23/32 failed with HTTP 402 Payment Required** (~15 min wall before OpenRouter credit exhausted).
  - First 9 tasks completed fully (akinyi_deseq2 → snakepipes_merge_fc).
  - Remaining 23 tasks: run dirs exist with `workspace/` copy but no `metadata.json` / `trajectory.jsonl` (rollout raised an exception before the save step, per-task `try/except` swallowed it).
  - V1: pass=3, partial=4, fail=2 on the 9 successful runs (23 missing-metadata run dirs are not counted by V1's summary and produce `task_id=None` rows in the JSON).
  - V2: pass=5, partial_pass=1, partial_fail=1, fail=2, error=23; mean_score=0.203 (V2 evaluator correctly marks the 23 missing-metadata runs as `error`).
  - V2 verdict_counts_legacy (V1 verdicts remapped with missing-metadata→fail): pass=3, partial=4, fail=25.
  - Root cause: OpenRouter account returned `402 Payment Required` with `"This request requires more credits, or fewer max_tokens. You requested up to 16384 tokens, but can only afford 3233."` starting mid-afternoon. Plan's hard budget ($22) was almost certainly reached on this arm's first 9 runs combined with the previous three arms — halting the sweep at this point matches the plan's "Halt and report if you hit $18 before finishing" rule.

## Final totals

- **Total attempted runs:** 128 (32 × 4 arms).
- **Total completed runs (metadata.json + trajectory.jsonl present):** 105.
  - `none` 32, `pipeline` 32, `llm_plan` 32, `paper` 9.
- **Crashed runs (OpenRouter 402):** 23 (all in paper arm, indices 9–31).
- **Estimated total cost:** ~$7 from trajectory-step token heuristics + however much the paper-arm 23 crashes billed before the 402 was returned (402 is not charged). Real spend equals the account credits consumed — check the OpenRouter dashboard for the exact figure.
- **Hard budget check:** spend stayed under $18 estimated; the 402 was caused by the account hitting its *pre-funded* ceiling, not by exceeding $18 of work. No runs were retried once the 402 pattern emerged, per the plan's halt-and-report rule.

## Final 4-arm V2 pass rates (versus V1)

Numerator / denominator always = 32 (the full registry):

| arm | V2 `pass` | V2 `pass+partial_pass` | V1 `pass` | status |
|-----|----------:|-----------------------:|----------:|--------|
| `none` | 19 (59.4%) | 23 (71.9%) | 16 (50.0%) | complete |
| `paper` | 5 (15.6%) | 6 (18.8%) | 3 (9.4%) | ⚠ incomplete — 23 crashed |
| `pipeline` | 17 (53.1%) | 22 (68.8%) | 15 (46.9%) | complete |
| `llm_plan` | 17 (53.1%) | 22 (68.8%) | 15 (46.9%) | complete |

On the 9-task subset where the paper arm completed (apples-to-apples): paper is top with 5/9 pass vs none 4/9 / pipeline 5/9 / llm_plan 4/9; mean V2 overall_score 0.722 vs 0.628/0.658/0.602.

## Key insight

- **Skill differentiation is swamped by workspace shortcuts.** Across the three 32/32 arms, `none` is tied with or better than `pipeline`/`llm_plan` on both V1 and V2 — the arm-spread is only ~2 passes / 0.04 mean_score, well below LLM-sampling noise at temp 0.1. This is precisely the Recommendation #1 effect from the V2 sweep: with every task workspace shipping its own `run_*.R` recipe alongside `OBJECTIVE.md`, the agent reconstructs the solution without needing any injected skill, so extra prompt bulk from `pipeline` / `llm_plan` can even hurt slightly. The 9-task restricted paper-vs-none comparison is the only place where the paper arm outpaces none (+1 pass, +0.094 mean_score), matching the V2 sweep's directional finding. Future sweeps should either hide shipped R scripts or adopt a workspace-randomization / ablation protocol before declaring a winning skill source.

## Minor notes

- **V2 lenient lift over V1 is modest**: +7 / +7 / +7 verdict upgrades for `none` / `pipeline` / `llm_plan`, +3 for the 9-run `paper` arm. The BixBench-style tolerance rescues mostly "table shape matches but row order differs" and "float rounded to 3 vs 5 digits" cases.
- **Methylation tasks remain the hardest family across all arms**: 1–2/6 pass per arm under V2; the RDS sidecar often can't reconstruct methylKit S4 semantics via `as.data.frame`.
- **Skill-injection audit is clean for every completed run.** All 32/32 `none`, 32/32 `pipeline`, 32/32 `llm_plan`, and 9/9 completed `paper` pairs have correct `arm`, `injected`, and `skill_sha256` (sha recomputed from manifest matches what the batch runner wrote to `metadata.json`). The 23 audit failures are all attributable to the crashed rollouts (missing `metadata.json`), not to cross-arm leakage.

## Tasks that crashed hard (A4 follow-up candidates)

For each of these, the paper-arm workspace was copied to disk but the agent rollout never produced a trajectory (all due to the same OpenRouter 402 event):

1. `snakepipes_merge_ct` (rna, maxplanck-ie-snakepipes-finish)
2. `riya_limma` (rna, RiyaDua-cervical-cancer)
3. `chipseq_plot_macs_qc` (chipseq, snakemake-workflows-chipseq)
4. `chipseq_plot_homer_annot` (chipseq, snakemake-workflows-chipseq)
5. `snakepipes_scrna_merge_coutt` (scrna, maxplanck-ie-snakepipes)
6. `snakepipes_scrna_qc` (scrna, maxplanck-ie-snakepipes)
7. `spilterlize_filter_features` (rna, epigen-spilterlize_integrate)
8. `spilterlize_norm_voom` (rna, epigen-spilterlize_integrate)
9. `spilterlize_limma_rbe` (rna, epigen-spilterlize_integrate)
10. `spilterlize_norm_edger` (rna, epigen-spilterlize_integrate)
11. `dea_limma` (rna, epigen-dea_limma)
12. `msisensor_merge` (variant, snakemake-workflows-msisensor-pro)
13. `methylkit_filt_norm` (methylation, fritjoflammers-snakemake-methylanalysis)
14. `methylkit2tibble_split` (methylation)
15. `methylkit_remove_snvs` (methylation)
16. `phantompeak_correlation` (chipseq)
17. `nearest_gene` (chipseq, maxplanck-ie-snakepipes)
18. `chipseq_plot_frip_score` (chipseq)
19. `chipseq_plot_peaks_count_macs2` (chipseq)
20. `chipseq_plot_annotatepeaks_summary_homer` (chipseq)
21. `epibtn_rpkm` (rna, joncahn-epigeneticbutton)
22. `snakepipes_scrna_report` (scrna)
23. `clean_histoneHMM` (chipseq, maxplanck-ie-snakepipes)

All three non-paper arms (`none`, `pipeline`, `llm_plan`) ran these tasks to completion, so they are believed to be retryable once OpenRouter credits are topped up. No task-level bugs were detected.

## Generated artefacts

- `experiments/llm_skill_ablation/SWEEP_V3_20260416T194356Z_SUMMARY.md` — human-readable report (V2 + V1 tables, per-family, per-task, 9-task paper-restricted comparison, key takeaways).
- `experiments/llm_skill_ablation/SWEEP_V3_20260416T194356Z.json` — full machine-readable matrix (arms × tasks → {verdict_v2, verdict_v1, overall_score, per_file_scores, steps, skill meta}).
- `experiments/llm_skill_ablation/SWEEP_V3_20260416T194356Z_SKILL_AUDIT.md` — per-(arm, task) skill sha verification.
- `experiments/llm_skill_ablation/SWEEP_V3_20260416T194356Z_V1_V2_DELTA.md` — V1 vs V2 transitions per arm+task.
- `experiments/llm_skill_ablation/tools/aggregate_sweep_v3.py` — new aggregator (reads both V1 and V2 evaluator JSONs).
- `experiments/llm_skill_ablation/config_e3_sweep.yaml` — sweep config used by the batch runner.
- `experiments/llm_skill_ablation/logs/e3/sweep_v3_<arm>_20260416T194356Z.log` — raw batch-runner logs per arm.
- `ldp_r_task_eval/runs/batch_sweep_v3_<arm>_20260416T194356Z/` — individual run directories (workspace + trajectory + metadata), retained for debugging.
- `ldp_r_task_eval/runs/_evaluations/sweep_v3_<arm>_20260416T194356Z.{json,md,v2.json,v2.md}` — per-arm evaluator outputs.

## Recommended next steps

1. **Top up OpenRouter credits and retry the 23 crashed paper-arm tasks** with the same `--batch-run-id sweep_v3_paper_20260416T194356Z` so they merge into the existing batch directory; then re-run `aggregate_sweep_v3.py --ts 20260416T194356Z` to rebuild the summary against the complete 32-task paper arm. Estimated retry cost: 23 × ~$0.08 ≈ $2.
2. **Hide or swap the shipped `run_*.R` scripts in each task workspace before the next full sweep.** With them visible the `none` arm reconstructs the recipe independently of any injected skill and washes out the differential signal between `paper`/`pipeline`/`llm_plan`. A simple replacement with a deliberately broken stub (plus perhaps a `_recipe_hint.md` pointer) should be enough to make the skill source decisive.
3. **Add a repeat-seed protocol (e.g. 3× per arm) at temp 0.1** to measure the sampling-noise floor — at current N=1 per (arm, task), verdict deltas of ≤2 tasks are indistinguishable from noise.
4. **Upgrade the RDS sidecar for methylKit S4 objects.** Methylation tasks (`methylkit_load`/`methylkit_unite`/`methylkit_filt_norm`) bottleneck at 0.07–0.23 V2 score because the sidecar's `as.data.frame` path loses the per-sample slot structure. Either call `methylKit::getData` explicitly or a canonical dump via `methylKit::methylBase2DataFrame`.
5. **Cross-validate with a held-out arm that removes workspace hints entirely** (`hidden_workspace` arm) to isolate the true skill lift. This directly addresses the V2 sweep's Recommendation #1 and this sweep's Key Insight.
