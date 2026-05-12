# skills_llm_plan — Subagent C2 status

## What this arm is

Pre-rollout "plan-as-skill" generator. For each R-task, one OpenRouter call
turns ONLY the task's own surface-level context (OBJECTIVE.md + input
listing + small-text previews + a safe subset of `meta.json`) into a
SKILL.md in the same 4-section layout used by paper- and pipeline-skills:

- `## Method`
- `## Parameters`
- `## Commands / Code Snippets`
- `## Notes for R-analysis agent`

The generator is walled off from the source pipeline, the method paper, the
registry fields that point to `r_script_src`, and anything under
`tasks/real_ground_truth/`. Compared to the other arms:

| arm              | context fed to the SKILL-maker                                      |
|------------------|---------------------------------------------------------------------|
| `no_skill`       | none                                                                |
| `llm_plan_skill` | OBJECTIVE.md + input filenames + small-text previews (this arm)     |
| `paper_skill`    | method paper PDF (vision adapter)                                   |
| `pipeline_skill` | pipeline source tree (.R/.Rmd/Snakefile/config/README)              |

## Tool path

```
main/paper_primary_benchmark/experiments/skills_llm_plan/tools/generate_llm_plan_skill.py
```

### CLI

Single-task:

```bash
python3 main/paper_primary_benchmark/experiments/skills_llm_plan/tools/generate_llm_plan_skill.py \
  --task-dir main/paper_primary_benchmark/ldp_r_task_eval/tasks/real/<task_id> \
  --task-id <task_id> \
  --out-dir main/paper_primary_benchmark/experiments/skills_llm_plan/<task_id>
```

Batch over a registry (Phase 2, NOT run here):

```bash
python3 main/paper_primary_benchmark/experiments/skills_llm_plan/tools/generate_llm_plan_skill.py \
  --registry main/paper_primary_benchmark/ldp_r_task_eval/r_tasks/registry.real.json \
  --out-root main/paper_primary_benchmark/experiments/skills_llm_plan
```

Flags:

- `--model` (default `openrouter/openai/gpt-4o`)
- `--temperature` (default `0.1`)
- `--force` to overwrite an existing `SKILL.md` / `run_manifest.json`
- `--only task_a,task_b` to restrict batch mode
- `--api-key` (otherwise `$OPENROUTER_API_KEY` then `openrouterkey.txt`)

### Outputs per task

- `<out-dir>/SKILL.md` — YAML front matter (`source_type: llm_plan`,
  `task_id`, `generated_at`, `model`, `inputs_previewed`) followed by the
  four-section body.
- `<out-dir>/run_manifest.json` — `prompt_tokens`, `completion_tokens`,
  `runtime_seconds`, `model`, `inputs_listed`, `inputs_previewed`.

### Batch manifest

In batch mode (or single-task mode if `--out-root` is also passed) the tool
maintains `experiments/skills_llm_plan/manifest.json` with the same shape as
the paper-skill manifest, keyed by `task_id`:

```json
{
  "version": 1,
  "generated_at": "...",
  "by_task_id": {
    "<task_id>": {
      "skill_md_path": "experiments/skills_llm_plan/<task_id>/SKILL.md",
      "skill_md_inline": "<first 4000 chars, front matter stripped>",
      "model": "openrouter/openai/gpt-4o",
      "prompt_tokens": N,
      "completion_tokens": N
    }
  }
}
```

## Input-surfacing rules (what the LLM actually sees)

- Reads `OBJECTIVE.md` verbatim.
- Reads a safe subset of `meta.json` (task_id / kind / family / description /
  success_glob / reference_output_files). Fields that would leak the source
  pipeline (`r_script_src`, `ground_truth_dir`, `workflow_id`, `pipeline_*`)
  are intentionally dropped before prompting.
- Walks `input/` recursively. For each file records `path + size_bytes`.
- For text files with extensions `.txt/.tsv/.csv/.json/.yml/.yaml/.md` that
  are ≤ 8 KB, includes a head preview capped at 40 lines / 2000 chars.
- For binaries (`.bam/.fastq.gz/.rds/.h5/.png/.pdf`) and text files > 8 KB,
  filename + size only. No content.
- Nothing outside `task-dir` is opened.

## Smoke test — `akinyi_deseq2`

Command run:

```bash
python3 main/paper_primary_benchmark/experiments/skills_llm_plan/tools/generate_llm_plan_skill.py \
  --task-dir main/paper_primary_benchmark/ldp_r_task_eval/tasks/real/akinyi_deseq2 \
  --task-id akinyi_deseq2 \
  --out-dir main/paper_primary_benchmark/experiments/skills_llm_plan/akinyi_deseq2
```

Result:

| metric              | value                              |
|---------------------|------------------------------------|
| model               | `openrouter/openai/gpt-4o`         |
| temperature         | 0.1                                |
| prompt_tokens       | 942                                |
| completion_tokens   | 620                                |
| total_tokens        | 1562                               |
| runtime_seconds     | 5.66                               |
| SKILL.md size       | 2790 bytes                         |
| inputs_listed       | `featureCounts_output.txt` (36300 B) |
| inputs_previewed    | none (the only input file is > 8 KB) |

### Structural verification

Confirmed the generated `SKILL.md` contains exactly the four required
second-level headings, in order:

- `## Method`
- `## Parameters`
- `## Commands / Code Snippets`
- `## Notes for R-analysis agent`

### Leak check

Grepped the generated `SKILL.md` for strings that would indicate the LLM
had seen anything outside the task directory:
`ground.truth`, `real_ground_truth`, `akinyi-onyango`, `workflow_candidates`,
`r_script_src`, `Akinyi-Onyango`, `snakemake`. **No matches.** The plan is
grounded entirely in OBJECTIVE.md.

### Quality note

The LLM correctly inferred **DESeq2** as the method — this is a legitimate
inference from the objective text itself, which explicitly says "Run DESeq2
differential expression (condition ~ group)". The plan:

- Uses the sample labels from the objective (`sample_0..sample_5`,
  `condition_A`, `condition_B`) and the stated ±2 log2FC thresholds; it
  does NOT fabricate extra column names.
- Emits a coherent R snippet (`DESeqDataSetFromMatrix`, NA filter,
  `write.table(..., col.names=TRUE, row.names=TRUE, quote=FALSE)`) that
  matches the deliverable contract in OBJECTIVE.md.
- Keeps the `input/` / `output/` paths verbatim from the objective.

Caveat: the input count matrix is >8 KB so the LLM did not see its column
header. The snippet's `counts[, 7:12]` column selection is inferred from
the objective's prose description ("columns: Geneid, Chr, Start, End,
Strand, Length, followed by 6 sample columns"). If an objective ever fails
to state the column layout, the tool will not know it, and the plan will
be weaker — that's consistent with this arm's design (no pipeline/paper
context).

## Recommendation for Phase-2 batch invocation

- Stick with `openrouter/openai/gpt-4o` at `temperature=0.1` for parity
  with the paper-skill vision adapter.
- Per-task cost on `akinyi_deseq2`: ~1.6 K total tokens, ~6 s wall time.
  Budget for the curated 4-8 task registry is ~10-15 K tokens / ~1 minute
  total — trivial.
- Run the batch only after Subagent A's task curation stabilizes; if a
  task's OBJECTIVE.md changes, re-run with `--force` for that task only
  (`--only <task_id>` combined with `--force`).
- Idempotent by default: reruns without `--force` are no-ops once a
  `SKILL.md` exists.
- The batch path rewrites `manifest.json` each invocation; per-task entries
  are keyed by `task_id` so partial runs accumulate cleanly.

## Constraints honored

- Network only to OpenRouter (`openai/gpt-4o`).
- No full batch run performed in Phase 1 (only the `akinyi_deseq2` smoke).
- No reads outside each task's own directory.
- No writes outside `experiments/skills_llm_plan/`.
- `ldp_r_task_eval`, `batch_runner`, `experiments/skills/`, and
  `experiments/skills_pipeline/` untouched.
