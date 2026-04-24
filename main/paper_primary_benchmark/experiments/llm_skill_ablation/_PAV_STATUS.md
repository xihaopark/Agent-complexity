# Plan-Act-Verify (PAV) arm — Subagent C status

Owner: Subagent C. Workstream C of `COORDINATION_PLAN.md`.

## 1. Tool additions to `RTaskEvalEnv`

File: `main/paper_primary_benchmark/ldp_r_task_eval/r_task_env.py`

Added two synchronous tools (auto-picked up by the ldp SimpleAgent via the
aviary `Environment` contract). Existing 6 tools unchanged; total is now 8.

1. **`write_plan(plan: str) -> str`**
   - Persists a markdown plan to `workspace/.plan.md`, overwriting on rewrite.
   - Returns `Wrote plan (<N> chars) to .plan.md`.

2. **`check_progress(note: str) -> str`**
   - Appends `<UTC ISO timestamp> <note>` to `workspace/.progress.log`.
   - Returns a JSON string with:
     - `output_files`: `[{name, size_bytes}, ...]` from `workspace/output/`.
     - `success_artifact_glob` + `success_artifact_present` flag.
     - `plan_excerpt` (first 1000 chars of `.plan.md`).
     - `note_count` (running total of progress entries).

Both preserve Google-style `Args:` docstrings so `aviary.Tool.from_function`
can derive the schema. Registered via `Tool.from_function(self.write_plan)`
and `Tool.from_function(self.check_progress)` in `RTaskEvalEnv.__init__`.

## 2. New config

Path: `main/paper_primary_benchmark/experiments/llm_skill_ablation/config_llm_plan_act_verify.yaml`

- Model: `openrouter/openai/gpt-4o`, `temperature: 0.1`.
- `max_steps: 48` (vs 32 for vanilla arms) to cover plan/verify overhead.
- System prompt length: 1125 chars (≤1200 budget).
- System prompt explicitly pins:
  - First observation → `list_workdir` + `read_text_file(OBJECTIVE.md)` and any
    shipped `*.R` / `*.r` (tasks often ship a reference script).
  - `write_plan` with bullet list derived from OBJECTIVE.
  - Post-change `check_progress` after each non-trivial tool call.
  - Pre-submit sequence: `check_progress("outputs produced")` →
    `list_workdir` → `check_progress("final verify")` → `submit_done`.
  - If the final snapshot is incomplete, rewrite the plan and continue.

## 3. Smoke test

Registry: `main/paper_primary_benchmark/ldp_r_task_eval/r_tasks/registry.real.smoke.json`
(single entry, `akinyi_deseq2`, mirrors `registry.real.json`; do not use for
batch eval).

Smoke invocation (repo root):

```bash
python3 -m main.paper_primary_benchmark.ldp_r_task_eval.batch_runner \
  --registry main/paper_primary_benchmark/ldp_r_task_eval/r_tasks/registry.real.smoke.json \
  --config main/paper_primary_benchmark/experiments/llm_skill_ablation/config_llm_plan_act_verify.yaml \
  --batch-run-id pav_smoke_202604161548 \
  --openrouter-key-file openrouterkey.txt
```

### Evaluator result

`python3 main/paper_primary_benchmark/ldp_r_task_eval/tools/evaluate_real_run.py --batch-run-id pav_smoke_202604161548`

| task | verdict | byte-identical | expected | exists |
|------|---------|----------------|----------|--------|
| `akinyi_deseq2` | **pass** | 2 / 2 | 2 | 2 |

Both `deseq2_up.txt` and `deseq2_down.txt` are byte-identical to the ground
truth at
`ldp_r_task_eval/tasks/real_ground_truth/akinyi_deseq2/reference_output/`.

### Loop artifacts observed in run dir

- `workspace/.plan.md`: 713 chars, structured bullet plan with inputs,
  preprocessing, DESeq2 steps, outputs, validation.
- `workspace/.progress.log`: **2 entries**
  ```
  2026-04-16T15:48:48Z outputs produced
  2026-04-16T15:48:50Z final verify
  ```
- `workspace/output/deseq2_up.txt` (2481 bytes) + `deseq2_down.txt`
  (1524 bytes) present.

### Trajectory (6 steps, 10 tool calls)

| step | tools called |
|------|---------------|
| 0 | `list_workdir`, `read_text_file`, `read_text_file` (OBJECTIVE + shipped `deseq2_analysis.R`) |
| 1 | `write_plan` |
| 2 | `run_rscript` (runs the shipped R script) |
| 3 | `check_progress`, `list_workdir` |
| 4 | `check_progress` (final verify) |
| 5 | `submit_done(success=true)` |

The agent clearly planned (see plan excerpt below), acted (read + ran R
script), then verified (two progress entries, one list_workdir between them)
before submitting.

Plan excerpt (first 400 chars of `.plan.md`):

```
- **Input**: `input/featureCounts_output.txt` with columns: Geneid, Chr, Start, End, Strand, Length, sample_0..sample_5.
- **Preprocessing**: Remove rows starting with `ERCC-`.
- **Data Preparation**:
  - Extract count data from columns 6 to 11.
  - Create `colData` with conditions A (first 3 samples) and B (last 3 samples).
- **DESeq2 Analysis**:
  - Create DESeq2 dataset with `DESeqDataSetFromMa
```

### Token usage

Not captured by `ldp.Trajectory` (the `ToolRequestMessage.info` payload is
empty). LiteLLM stderr shows 6 `openrouter/openai/gpt-4o` completion calls;
for accurate token accounting the coordinator should enable
LiteLLM success callbacks, or parse `litellm`'s stderr cost log, at run time.

## 4. Iteration history

The prompt was iterated four times over the same task to reach pass-with-2-
progress-entries:

| batch id | verdict | `.progress.log` lines | notes |
|----------|---------|-----------------------|-------|
| pav_smoke_202604161542 | partial | 1 | Agent wrote its own R script; dropped Geneid rownames → output not byte-identical. Prompt didn't tell agent to reuse the shipped reference R script. |
| pav_smoke_202604161544 | pass | 1 | Added "read and reuse shipped *.R" hint. Byte-identical, but only one check_progress call. |
| pav_smoke_202604161545 | pass | 1 | Tried softer "final verify" instruction; agent still batched list_workdir+check_progress in the same step. |
| pav_smoke_202604161547 | pass | 1 | Explicit "at least twice" still not enough. |
| pav_smoke_202604161548 | **pass** | **2** | Made the final 4-step micro-sequence explicit (post-run check_progress, list_workdir, final-verify check_progress, submit_done). |

The final `pav_smoke_202604161548` batch is the one the coordinator should
cite.

## 5. Recommendations for coordinator

1. **Use `max_steps: 48` for this arm.** 32 is tight once planning and
   double-verify are added; 48 leaves headroom for error-recovery iterations
   on harder tasks.
2. **Do not reuse smoke registry `registry.real.smoke.json` for the real
   sweep.** It intentionally contains only `akinyi_deseq2`. The coordinator
   should keep using `registry.real.json` (or the expanded variant from
   workstream A) for full evaluation; the smoke registry is purely a unit-
   test fixture.
3. **Token accounting.** If per-run cost matters for the ablation, add a
   LiteLLM `success_callback` in `llm_env.py` or wrap `LLMCallOp` to log
   token counts into `metadata.json`. The trajectory format does not carry
   them today.
4. **The shipped reference R script in each real task workspace is a
   strong prior.** The PAV prompt specifically tells the agent to read and
   reuse `*.R` / `*.r` files when they match OBJECTIVE. The no-skill and
   with-skill arms do not currently include that hint. For a clean
   comparison, decide whether the ablation is "PAV vs vanilla" (fine) or
   "PAV prompt engineering benefits vs vanilla" (in which case the vanilla
   arms should get the same "reuse shipped scripts" hint).
5. **Two new tools, 8 total.** Vanilla arms' prompts still enumerate the
   old 6 tools. They will still work (extra tools are just unused), but if
   the coordinator wants the vanilla arms to ignore the new tools cleanly,
   no change is needed — SimpleAgent will simply not invoke them unless
   mentioned.

## 6. Files touched by subagent C

- **Modified**
  - `main/paper_primary_benchmark/ldp_r_task_eval/r_task_env.py`
- **Added**
  - `main/paper_primary_benchmark/experiments/llm_skill_ablation/config_llm_plan_act_verify.yaml`
  - `main/paper_primary_benchmark/ldp_r_task_eval/r_tasks/registry.real.smoke.json`
  - `main/paper_primary_benchmark/experiments/llm_skill_ablation/_PAV_STATUS.md` (this file)

Not touched: `registry.real.json`, `build_real_r_tasks.py`,
`evaluate_real_run.py`, any file under `tasks/real/` or
`tasks/real_ground_truth/`, any file under `external/Paper2Skills/`.
