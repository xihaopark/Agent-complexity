# Coordination Plan V2 — Paper-first, data-only, 4 skill sources

Supersedes the sweep scope in `COORDINATION_PLAN.md`. The PAV dimension from
v1 is set aside for this round; here we hold the agent architecture constant
(vanilla SimpleAgent) and vary only the SKILL SOURCE.

## User requirements (what changed)

1. **Paper-first task curation.** Only build tasks for pipelines that already
   have a downloaded, validated paper skill (from `experiments/skills/`).
   This eliminates the "11 of 12 tasks have no skill" coverage gap from v1.
2. **Data-only outputs.** No task may have an image/PDF/plot as its
   deliverable. Refactor or drop any image-producing task. Keeping the
   *data that underlies* a plot (the CSV input to ggsave) is fine; the
   ggsave call itself is dropped from the reference.
3. **Four skill-source arms on the same agent.**

   | arm id | skill source | description |
   |---|---|---|
   | `no_skill` | — | Vanilla SimpleAgent, no paper/pipeline/plan context. |
   | `llm_plan_skill` | LLM pre-rollout | Before the agent starts, call LLM once with OBJECTIVE.md + input listing → it writes a SKILL.md-shaped plan. Inject as context. This is "plan-in-skill-template" as a pre-step. |
   | `paper_skill` | method paper | Existing vision-adapter skill from `experiments/skills/<doi>/`. |
   | `pipeline_skill` | pipeline source | NEW: read all `.R/.Rmd/Snakefile/config.yaml/README.md` of the source workflow → LLM distills into a SKILL.md. |

## Paper-covered pipeline inventory

From `experiments/skills/manifest.json::by_workflow_id`:

| workflow_id | paper skill | notes |
|---|---|---|
| `akinyi-onyango-rna_seq_pipeline-finish` | Conesa 2016 survey | already yields `akinyi_deseq2` |
| `rna-seq-star-deseq2-finish` | Love 2014 DESeq2 | scripts use `snakemake@` — needs adapter |
| `cite-seq-alevin-fry-seurat-finish` | Srivastava 2019 alevin | Seurat not installed → skip |
| `fritjoflammers-snakemake-methylanalysis-finish` | Wong 2016 MethPat | inspect for standalone R |
| `lwang-genomics-ngs_pipeline_sn-rna_seq-finish` | Marioni 2008 | inspect for standalone R |
| `cellranger-multi-finish` | Zheng 2017 10x | mostly python/shell; skip if no R task |
| `epigen-rnaseq_pipeline-finish` | Marioni 2008 | `snakemake@` only — needs adapter |
| `read-alignment-pangenome-finish` | Minigraph-Cactus | mostly shell; likely no R task |

Realistic target: 4-8 data-only R tasks, all with paper-skill coverage.

## Execution plan

### Phase 1 (parallel)

**Subagent A — task curation (paper-first, data-only)**
- Audit the current 12 tasks in `registry.real.json`:
  - Keep tasks with pure data outputs (CSV/TSV/txt).
  - Refactor tasks that output BOTH data and images: modify the reference
    R script to drop `ggsave/pdf/png` calls and keep only the tabular
    writes. Update `eval_files` to data-only. Re-build ground truth.
  - Drop tasks whose ONLY deliverable is an image.
- From the 8 paper-covered workflows, add new tasks by:
  - Scanning for standalone R scripts, OR
  - Wrapping `snakemake@`-style scripts with a tiny adapter that fakes
    the `snakemake` object (list with `$input, $output, $params, $threads`).
- Rebuild + verify every surviving task; update `registry.real.json`.
- Deliverable: `tasks/real/_STATUS_V2.md`.

**Subagent B — pipeline-skill generator**
- Write `tools/generate_pipeline_skill.py` that, for a given workflow dir,
  collects all `.R/.Rmd/.py/Snakefile/.smk/config*.yaml/env*.yaml/README*`
  files (cap per-file 8 KB, cap total 80 KB), then calls OpenRouter
  `gpt-4o` to emit a SKILL.md in the same 4-section format as paper-skills.
- Run it on the 8 paper-covered workflows.
- Output under `experiments/skills_pipeline/<workflow_id>/SKILL.md` +
  `run_manifest.json`.
- Produce a `manifest.json` analogous to the paper-skill one but keyed
  by workflow_id.
- Deliverable: `experiments/skills_pipeline/_STATUS.md`.

**Subagent C — LLM-plan-skill generator**
- Write `tools/generate_llm_plan_skill.py` that, given a task directory
  (OBJECTIVE.md + input listing + meta.json), makes ONE pre-rollout
  OpenRouter call asking the LLM to emit a SKILL.md-shaped plan for
  this task (4 sections: Method / Parameters / Commands / Notes).
- Idempotent per-task; caches to
  `experiments/skills_llm_plan/<task_id>/SKILL.md`.
- Also ship a batch mode that runs it across a registry.
- Deliverable: the tool + smoke run on `akinyi_deseq2`.

### Phase 2 (after A + B + C)

**Subagent D — unified skill injection in batch_runner**
- Extend `batch_runner.py` to accept `--skill-source {none|paper|pipeline|llm_plan}`.
- Depending on source, load the appropriate manifest:
  - `paper`: `experiments/skills/manifest.json` (existing, per-task).
  - `pipeline`: `experiments/skills_pipeline/manifest.json` (new, per-workflow;
    resolves task_id → workflow_id via registry).
  - `llm_plan`: `experiments/skills_llm_plan/manifest.json` (new, per-task).
  - `none`: no injection.
- Writes the source into `metadata.json::skill.arm` for traceability.
- Smoke test one task in each source.
- Deliverable: updated `batch_runner.py` + test log.

### Phase 3

**Subagent E — 4-arm sweep + summary**
- Run each of 4 arms on the curated registry (4-8 tasks). Shared timestamp.
- Evaluate via `evaluate_real_run.py`.
- Produce a stratified summary comparing arms.

## Out of scope for this round

- PAV agent architecture (keep for a future run; requires its own decoupled
  ablation).
- Expanding paper PDF downloads (blocked on open-access availability).
- Task repetition for statistical significance.
