# Coordination Plan V3 — Scale to ≥30 tasks + BixBench-style lenient evaluator

Supersedes task-count + evaluator scope from V2. Agent architecture, skill
sources, and batch runner CLI stay the same.

## User requirements

1. **Task scale ≥30**, exhausting every paper-covered pipeline. Find more
   papers to cover pipelines that currently have zero paper-skill so we
   can accept their R scripts. Two more curation rounds beyond V2.
2. **Evaluator goes BixBench-style**: grade both *intermediate process*
   and *final result*, with tolerant / normalized comparisons. Stop
   failing tasks just because floats round differently or rows are
   reshuffled.
3. **Normalization work**: unify output schemas where the reference R
   script has incidental format quirks (trailing newline, index column,
   locale decimal, etc.).

## Evaluation redesign (B3)

New evaluator `tools/evaluate_real_run_v2.py`. Back-compat with V1 is
additive — V2 JSON schema carries V1 fields plus V3 scores.

Per-file score ∈ [0, 1]:

- **byte_identical** (1.0) if hashes match.
- **normalized_equal** (1.0) if — after whitespace trim, LF normalization,
  locale-decimal folding, column-agnostic row sort — contents match.
- **tabular_tolerance** (0.5–0.99): for `.tsv/.csv/.txt` load with pandas,
  align columns, compare with `rtol=1e-3, atol=1e-5`; score = matched cell
  fraction (with same schema + >0 rows required for any score).
- **rds_semantic** (0.5–0.99): for `.rds` files, run a small R side-car that
  serialises the object to a canonical TSV (via `as.data.frame` or
  `methylKit::getData`), then fall back to `tabular_tolerance`.
- **process_credit** (0.0–0.25): independent of content, awarded if the
  file exists AND is non-zero size AND parses as the expected type.
- **missing** / **parse_error**: 0.0.

Process signals per task (weighted into overall_score):

- `tool_calls_executed` > 2 (agent did more than list_workdir)
- `rscript_success_count` ≥ 1 (at least one Rscript exited 0)
- `submit_done_called` == true
- `outputs_directory_nonempty` == true

`overall_score = 0.3 * mean(process_signals) + 0.7 * mean(per_file_score)`

Verdicts:

- `pass`        overall ≥ 0.90
- `partial_pass` 0.60 ≤ overall < 0.90
- `partial_fail` 0.30 ≤ overall < 0.60
- `fail`        overall < 0.30
- `error`       trajectory crashed before producing any output

Deliverables:

- `tools/evaluate_real_run_v2.py` with CLI mirroring V1 plus `--per-file-json`
- `tools/evaluators/` helpers (normalizers, RDS sidecar)
- Short `EVALUATION_V2.md` describing the scoring rubric
- Back-compat: `--legacy` flag reproduces V1 verdicts

## Task expansion (A3)

Target **≥30 ready tasks** (currently 6).

Strategies:

1. **Deeper into V2 paper-covered workflows**: `tools/candidate_r_scripts.csv`
   already lists 52 candidates; re-examine those we skipped in A2 because
   of `snakemake@`-only or missing packages, and see whether the A2
   SnakemakeMock adapter can rescue them. Install missing Bioconductor
   packages when the install is clean (< 3 min) and license-compatible.
2. **Recover V1 workflows once paper coverage lands (see C3)**: RiyaDua
   cervical-cancer (limma), snakemake-workflows-chipseq (MACS2/ENCODE),
   snakePipes, epigeneticbutton, ASTRO — any that can be rescued with
   data-only outputs will be added.
3. **Scripts with hardcoded output paths**: add a pre-run `chdir()` or
   directory-symlink trick so they write into the task workspace. Only
   accept if the rewritten script still matches the original logic.
4. **Scripts that emit images alongside data**: reuse the
   `_patch_strip_*` pattern from A2 to strip `ggsave/pdf/png` calls on a
   temporary copy of the source.
5. Drop candidates that require network (`biomaRt` mirror fetches) or
   unavailable R packages (`Seurat`, `scater`, `scran`, `sleuth`, `spp`,
   `Monocle`, `DMRcaller`, `ComplexUpset`, `AnnotationForge`, `topGO`) unless
   a CRAN/Bioc install works quickly.

Coverage targets by family (approximate):

- rna: ≥10 tasks
- methylation: ≥6 tasks
- chipseq/atacseq: ≥5 tasks
- scrna: ≥3 tasks
- other (annotation / QC / merge utilities): balance of remainder

Each task must satisfy: data-only output, snakemake-mockable or commandArgs,
deterministic synthetic inputs, ground truth produced by the actual R
source code (verbatim or `_patch_strip_*`-scrubbed copy).

## Paper coverage expansion (C3)

Today only 8 workflows have downloaded PDFs. Expand by:

1. For each of the 30 `main/finish/workflow_candidates/` workflows that is
   *not* in `workflow_literature_map.json`, find the primary method DOI:
   - Scan the workflow's `README*`, `*.yaml`, `environment*.yaml`, and R
     script headers for citations, tool names, `@citation` blocks.
   - Map tool name → canonical DOI (e.g., `limma` → Ritchie 2015
     `10.1093/nar/gkv007`; `MACS2` → Zhang 2008 `10.1186/gb-2008-9-9-r137`;
     `snakePipes` → Bhardwaj 2019 `10.1093/bioinformatics/btz436`;
     `edgeR` → Robinson 2010 `10.1093/bioinformatics/btp616`; etc.).
2. Try Unpaywall open access for every DOI; fall back to bioRxiv preprint
   where the OA copy is available (same Crossref metadata path we used in
   V2 for Minigraph-Cactus).
3. Update `workflow_literature_map.json` v3 with: `primary_doi`, `tool`,
   a free-text `chosen_because` note for each added mapping.
4. Save downloaded PDFs under `literature/pdfs/<doi_safe>.pdf`.

Expected outcome: ≥15 workflows have downloaded papers, unlocking more
paper-covered tasks for A3 to build on.

## Phase 2 — regenerate skills (D3)

- Re-run the vision adapter on any newly-downloaded PDF → new
  `experiments/skills/<doi_safe>/SKILL.md`.
- Re-run the pipeline-skill generator on any workflow that now has tasks
  but not yet a pipeline-skill.
- Re-run the LLM-plan generator on the updated registry via
  `--registry ... --out-root experiments/skills_llm_plan`.
- Rebuild all three manifests.
- Smoke one task per arm to verify injection.

## Phase 3 — full sweep (E3)

- 4 arms (none / paper / pipeline / llm_plan) × ≥30 tasks = ≥120 runs.
- Use V2 lenient evaluator for verdict + keep V1 verdict column for
  back-compat (compute both).
- Summary: stratified by family, by difficulty, by skill availability.
- Budget ≤ $8 (runs) + ~$0.50 (skill regen).

## Execution order

```
 Phase 1 (parallel):  A3      B3      C3
                       \      |      /
                        \-----+-----/
                              |
 Phase 2 (after C3):          D3      (needs A3's final task list)
                              |
 Phase 3 (after A3+B3+D3):    E3
```

A3 and C3 are coupled logically (new papers unlock new tasks) but can run
in parallel because A3 gates each task on "workflow has at least a
pipeline-skill-able source tree" rather than paper coverage. D3 later
cleans up skill coverage for A3's final task set.
