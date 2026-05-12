# Sample of 50 tasks (5 agents × 10)

From **145** pipeline-stage stubs, **50** were drawn with **family-proportional** quotas (largest-remainder on `manifest.json` families). Each workspace is a **self-contained micro task** (sum integers in `input/values.txt` → write `output/result.txt`), so experiments do not require Snakemake or large omics files.

## Files

| File | Purpose |
|------|---------|
| `manifest.json` | Seed, per-family quotas, **5 batches** of 10 `task_id`s (`agent_01` … `agent_05`) |
| [`../r_tasks/registry.sample_50.json`](../r_tasks/registry.sample_50.json) | Batch runner registry: **only** these 50 tasks (all `ready`) |

**Source of truth:** after `--write-registry`, the same 50 rows also appear in the main [`registry.json`](../r_tasks/registry.json) with `status: ready`. Prefer **`registry.sample_50.json`** for 50-only batch runs; use the main file when you need pilot + full matrix.

## Regenerate (deterministic with same `--seed`)

```bash
python3 main/paper_primary_benchmark/ldp_r_task_eval/tools/sample_and_prepare_eval_50.py --write-registry
```

`--write-registry` updates the **main** [`registry.json`](../r_tasks/registry.json) for those 50 rows (`status: ready`, `agent_batch`, `evaluation_ready`).

**Do not** run [`generate_r_task_stubs.py --force`](../../tools/generate_r_task_stubs.py) on these directories afterward—it overwrites `OBJECTIVE.md` / `meta.json` and breaks the prepared micro-eval. Regenerate stubs only on a clean tree, or re-run this script after.

## Run batch smoke (50 scripted successes)

Scripted smoke writes `output/result.txt` using the same rules as `rollout.expected_result_text_for_smoke` (prefer `evaluation/reference_sum.txt`, else sum `input/values.txt`), so **batch `--smoke` matches the micro-task answer**—unlike a fixed constant.

**Reward note:** `submit_done` in the env still only checks that the artifact **exists**; for LLM runs, compare agent output to `evaluation/reference_sum.txt` offline if you need correctness metrics.

Uses only the 50-task registry (not pilot, not the other 95 stubs):

```bash
python3 main/paper_primary_benchmark/ldp_r_task_eval/batch_runner.py \
  --registry main/paper_primary_benchmark/ldp_r_task_eval/r_tasks/registry.sample_50.json \
  --smoke
```

## Validate

```bash
python3 main/paper_primary_benchmark/ldp_r_task_eval/tools/validate_r_task_registry.py \
  --registry main/paper_primary_benchmark/ldp_r_task_eval/r_tasks/registry.sample_50.json \
  --kind sample50
```

## Agent assignment

Use `manifest.json` → `batches[].task_ids` for **agent_01** … **agent_05** (10 tasks each). Same mapping is in each task’s `meta.json` as `agent_batch`.
