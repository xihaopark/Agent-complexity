# F3 retry log — paper-arm 23-task rescue

## TL;DR

- **Retry outcome**: **0 / 23 successful**. All retry attempts were refused
  by OpenRouter with HTTP 402 *before* any tokens were consumed. Root cause
  is still a near-zero account balance, not a code or rollout bug.
- **Durable crashes**: 0 (no task ran long enough to fail "durably"; every
  attempt was terminated pre-flight by OpenRouter's per-request affordability
  check).
- **Estimated spend on F3**: **$0.00 agent-side**. The only cost incurred
  was a ~$0.003 ping + a ~$0.0001 validation ping — both well under the $5
  budget.
- **4 × 32 matrix status**: unchanged from E3. The SWEEP_V3 artefacts are
  still authoritative for the 9-task paper overlap; the paper arm's 23
  `error` rows from E3 remain and were not overwritten.

## OpenRouter status at F3 start

Key file `openrouterkey.txt` (sk-or-v1-4c1…). GET `/api/v1/credits` returns:

```json
{"data": {"total_credits": 2700, "total_usage": 2700.130873749}}
```

→ effective balance **≈ negative $0.13** (or zero with a small cached
positive buffer; OpenRouter's own pre-flight check gives the ground truth).

A small ping (`max_tokens=4`) succeeds (HTTP 200, cost ≈ $0.00004). A
1000-token generation succeeds (cost $0.0029, balance implied ≈ $0.014 at
time of test). **Any agent call that reserves the model's default
`max_tokens=16384` is rejected** with:

```
"This request requires more credits, or fewer max_tokens.
 You requested up to 16384 tokens, but can only afford 1382."
```

Lowering `max_tokens` to 1024 then fails on the *input* side for the first
retry task (`snakepipes_merge_ct`):

```
"Prompt tokens limit exceeded: 16264 > 5530"
```

The paper-arm prompt (system prompt + tool schemas + SKILL.md + OBJECTIVE
plus sample file pre-reads) is ~16k tokens. The available pre-flight
reservation is ~5.5k. Even after lowering output reserve, the prompt alone
is too big to clear the affordability check.

**Conclusion**: the key's topup is insufficient for even one full agent
rollout on the paper arm. The retry cannot proceed without an additional
OpenRouter credit top-up (minimum ≈ **$3–5** to cover 23 rollouts at
~$0.10/task; safer to add **$10**).

## What was attempted (chronological)

| step | action | outcome |
|------|--------|---------|
| 1 | `GET /credits` — confirm balance | balance ~ 0 (see above) |
| 2 | ping `max_tokens=4` | HTTP 200, cost $0.00004 |
| 3 | ping `max_tokens=1000` | HTTP 200, cost $0.0029 |
| 4 | wrote `tools/retry_paper_arm_f3.py` (new file, does NOT modify `batch_runner.py`). Imports `batch_runner._one_task` and iterates a CLI-provided `--tasks` list in-registry-order so each retried run lands at `runs/batch_sweep_v3_paper_20260416T194356Z/<idx:03d>_<task_id>/`, matching E3's folder layout exactly | tool ok |
| 5 | dry-run subset (2 tasks) with `--dry-run` | plan validates, correct indices |
| 6 | launched retry of all 23 tasks with `config_e3_sweep.yaml` (default `max_tokens`) | **HTTP 402** on task 009 (`snakepipes_merge_ct`) — "can only afford 1382 tokens" |
| 7 | killed retry; created `config_e3_sweep_f3.yaml` with `max_tokens=1024` (no other diff) | config loads cleanly |
| 8 | launched single-task retry on `snakepipes_merge_ct` with the new config | **HTTP 402** — "Prompt tokens limit exceeded: 16264 > 5530". The input prompt itself is too large for the remaining balance. |
| 9 | killed retry; documented blocker in this file | — |

## Artefacts added by F3

- `experiments/llm_skill_ablation/tools/retry_paper_arm_f3.py` — subset
  retry wrapper. Reusable for any future arm / task list. Will work once
  credits are topped up.
- `experiments/llm_skill_ablation/config_e3_sweep_f3.yaml` — E3 config with
  `max_tokens=1024` added. Usable if the account is topped up to a level
  that covers the output reservation but not the default 16 k. (Currently
  insufficient: the input-token check is also binding.)
- `experiments/llm_skill_ablation/logs/e3_f3/retry_f3_<ts>.log` — captured
  LiteLLM 402 traces for posterity.

## Tasks still owed (23 paper-arm rollouts)

Same list E3 recorded. Indices are the registry ordinal (used by the
retry wrapper to recreate the correct folder name).

| idx | task_id | family | workflow | paper_skill |
|----:|---------|--------|----------|:-----------:|
| 9 | `snakepipes_merge_ct` | rna | `maxplanck-ie-snakepipes-finish` | Y |
| 10 | `riya_limma` | rna | `RiyaDua-cervical-cancer-snakemake-workflow` | — |
| 11 | `chipseq_plot_macs_qc` | chipseq | `snakemake-workflows-chipseq-finish` | — |
| 12 | `chipseq_plot_homer_annot` | chipseq | `snakemake-workflows-chipseq-finish` | — |
| 13 | `snakepipes_scrna_merge_coutt` | scrna | `maxplanck-ie-snakepipes-finish` | Y |
| 14 | `snakepipes_scrna_qc` | scrna | `maxplanck-ie-snakepipes-finish` | Y |
| 15 | `spilterlize_filter_features` | rna | `epigen-spilterlize_integrate-finish` | — |
| 16 | `spilterlize_norm_voom` | rna | `epigen-spilterlize_integrate-finish` | — |
| 17 | `spilterlize_limma_rbe` | rna | `epigen-spilterlize_integrate-finish` | — |
| 18 | `spilterlize_norm_edger` | rna | `epigen-spilterlize_integrate-finish` | — |
| 19 | `dea_limma` | rna | `epigen-dea_limma-finish` | Y |
| 20 | `msisensor_merge` | variant | `snakemake-workflows-msisensor-pro-finish` | Y |
| 21 | `methylkit_filt_norm` | methylation | `fritjoflammers-snakemake-methylanalysis-finish` | Y |
| 22 | `methylkit2tibble_split` | methylation | `fritjoflammers-snakemake-methylanalysis-finish` | Y |
| 23 | `methylkit_remove_snvs` | methylation | `fritjoflammers-snakemake-methylanalysis-finish` | Y |
| 24 | `phantompeak_correlation` | chipseq | `snakemake-workflows-chipseq-finish` | — |
| 25 | `nearest_gene` | chipseq | `maxplanck-ie-snakepipes-finish` | Y |
| 26 | `chipseq_plot_frip_score` | chipseq | `snakemake-workflows-chipseq-finish` | — |
| 27 | `chipseq_plot_peaks_count_macs2` | chipseq | `snakemake-workflows-chipseq-finish` | — |
| 28 | `chipseq_plot_annotatepeaks_summary_homer` | chipseq | `snakemake-workflows-chipseq-finish` | — |
| 29 | `epibtn_rpkm` | rna | `joncahn-epigeneticbutton-finish` | — |
| 30 | `snakepipes_scrna_report` | scrna | `maxplanck-ie-snakepipes-finish` | Y |
| 31 | `clean_histoneHMM` | chipseq | `maxplanck-ie-snakepipes-finish` | Y |

Paper-skill injected: **10 / 23** (per `SKILL_COVERAGE_V3.md`).
Fallback (no paper skill → sentinel, prompt identical to `none`): **13 / 23**.

## How to finish the retry once credits are available

```bash
cd /Users/park/code/Paper2Skills-main/main
python3 -m paper_primary_benchmark.experiments.llm_skill_ablation.tools.retry_paper_arm_f3 \
  --tasks snakepipes_merge_ct,riya_limma,chipseq_plot_macs_qc,chipseq_plot_homer_annot,snakepipes_scrna_merge_coutt,snakepipes_scrna_qc,spilterlize_filter_features,spilterlize_norm_voom,spilterlize_limma_rbe,spilterlize_norm_edger,dea_limma,msisensor_merge,methylkit_filt_norm,methylkit2tibble_split,methylkit_remove_snvs,phantompeak_correlation,nearest_gene,chipseq_plot_frip_score,chipseq_plot_peaks_count_macs2,chipseq_plot_annotatepeaks_summary_homer,epibtn_rpkm,snakepipes_scrna_report,clean_histoneHMM \
  --batch-run-id sweep_v3_paper_20260416T194356Z \
  --skill-source paper \
  --config paper_primary_benchmark/experiments/llm_skill_ablation/config_e3_sweep.yaml \
  --openrouter-key-file ../openrouterkey.txt
```

Then re-evaluate + re-aggregate:

```bash
python3 -m paper_primary_benchmark.ldp_r_task_eval.tools.evaluate_real_run \
  --runs-dir paper_primary_benchmark/ldp_r_task_eval/runs/batch_sweep_v3_paper_20260416T194356Z \
  --registry paper_primary_benchmark/ldp_r_task_eval/r_tasks/registry.real.json \
  --out paper_primary_benchmark/ldp_r_task_eval/runs/_evaluations/sweep_v3_paper_20260416T194356Z.json

python3 -m paper_primary_benchmark.ldp_r_task_eval.tools.evaluate_real_run_v2 \
  --runs-dir paper_primary_benchmark/ldp_r_task_eval/runs/batch_sweep_v3_paper_20260416T194356Z \
  --registry paper_primary_benchmark/ldp_r_task_eval/r_tasks/registry.real.json \
  --out paper_primary_benchmark/ldp_r_task_eval/runs/_evaluations/sweep_v3_paper_20260416T194356Z.v2.json

python3 paper_primary_benchmark/experiments/llm_skill_ablation/tools/aggregate_sweep_v3.py \
  --ts 20260416T194356Z
```

The aggregator overwrites `SWEEP_V3_20260416T194356Z.{json,md}` +
`_SKILL_AUDIT.md` + `_V1_V2_DELTA.md` in place — no code change required.

## Reconciliation with E3's remaining artefacts

- `SWEEP_V3_20260416T194356Z.json`, `..._SUMMARY.md`, `..._SKILL_AUDIT.md`,
  `..._V1_V2_DELTA.md` are **NOT overwritten** in this turn. F3 could not
  produce new data, so the files still correctly reflect the state
  {none 32/32, pipeline 32/32, llm_plan 32/32, paper 9/32 + 23 error}.
- `PAPER_SKILL_ADVOCACY.md` and `PAPER_SKILL_TASK_WINS.json` are based
  exclusively on the 9-task paper overlap — this is the only apples-to-
  apples slice available until the retry completes. All claims are scoped
  accordingly.
