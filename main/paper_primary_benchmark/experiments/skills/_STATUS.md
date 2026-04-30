# _STATUS — Phase D skill generation + per-task injection (Subagent D)

Date: 2026-04-17
Scope: `experiments/skills/`, `experiments/llm_skill_ablation/config_llm_with_skill_v2.yaml`,
`literature/workflow_literature_map.json`, `literature/_DOI_AUDIT.md`,
`ldp_r_task_eval/batch_runner.py`.

## Verdict

All deliverables met. Vision adapter was run on all 7 PDFs (after
repairing two empty downloads). `batch_runner.py` now supports
`--skill-manifest` with per-task `{{SKILL_MD}}` substitution, and the
smoke run of `akinyi_deseq2` under `config_llm_with_skill_v2.yaml`
passes with byte-identical output.

## DOI audit summary

Full detail: `literature/_DOI_AUDIT.md`. Three mislabellings were found
and corrected in `workflow_literature_map.json` (bumped to `version: 2`):

1. **`10.1038/nbt.1612` is V3D imaging**, not the Marioni 2008 RNA-seq
   reproducibility paper. Replaced with `10.1101/gr.079558.108`
   (Marioni 2008) in `lwang-genomics-ngs_pipeline_sn-rna_seq-finish`
   and `epigen-rnaseq_pipeline-finish`. Correct Marioni PDF
   downloaded.
2. **`10.1186/s12859-016-0950-8` is MethPat** (Wong et al. 2016), not
   systemPipeR. Replaced with the correct systemPipeR DOI
   `10.1186/s12859-016-0938-4` in the three `tgirke-systempiperdata-*`
   workflows; the MethPat DOI was reattached to
   `fritjoflammers-snakemake-methylanalysis-finish` where it is
   method-appropriate (so the downloaded PDF is not orphaned).
3. **`10.1186/s13059-019-1670-y` is the alevin paper**, not
   alevin-fry. Tool label corrected to `alevin`; DOI and workflow
   assignment unchanged (close enough semantically).

Two previously 0-byte PDFs (`10.1038_nbt.1612.pdf`,
`10.1038_s41587-023-01793-w.pdf`) have been repaired: the nbt.1612
stub was removed (DOI was wrong anyway), the Marioni paper was pulled
from Genome Research OA, and Minigraph-Cactus was pulled from its
bioRxiv preprint (same manuscript, renamed to the published DOI
filename).

## Skills generated (7 / 7)

All via `paper2skills_ab_test/vision_adapter.py` with `--pages 8
--dpi 130`, model `openrouter/openai/gpt-4o`.

| # | doi_safe | Paper | SKILL.md size | Prompt tok | Completion tok | Runtime (s) |
|---|---|---|---:|---:|---:|---:|
| 1 | `10.1038_ncomms14049` | Zheng et al., *Massively parallel digital transcriptional profiling of single cells* (10x Chromium), Nat. Commun. 2017 | 2106 B | 6407 | 401 | 13.2 |
| 2 | `10.1038_s41587-023-01793-w` | Hickey et al., *Pangenome Graph Construction with Minigraph-Cactus*, Nat. Biotechnol. 2023 (bioRxiv preprint PDF) | 1841 B | 5307 | 310 | 14.9 |
| 3 | `10.1101_gr.079558.108` | Marioni et al., *RNA-seq: An assessment of technical reproducibility and comparison with gene expression arrays*, Genome Res. 2008 | 2070 B | 6408 | 425 | 13.0 |
| 4 | `10.1186_s12859-016-0950-8` | Wong et al., *MethPat*, BMC Bioinf. 2016 | 1672 B | 6412 | 286 | 11.9 |
| 5 | `10.1186_s13059-014-0550-8` | Love, Huber, Anders, *DESeq2*, Genome Biol. 2014 | 2159 B | 6412 | 388 | 14.4 |
| 6 | `10.1186_s13059-016-0881-8` | Conesa et al., *A survey of best practices for RNA-seq data analysis*, Genome Biol. 2016 | 1977 B | 6412 | 333 | 10.7 |
| 7 | `10.1186_s13059-019-1670-y` | Srivastava et al., *Alevin efficiently estimates accurate gene abundances*, Genome Biol. 2019 | 1861 B | 6411 | 330 | 11.1 |

**Total:** 43,769 prompt + 2,473 completion = 46,242 tokens.
Estimated OpenRouter cost at GPT-4o list ($2.50/M input, $10/M output):
**~$0.13**. Well within the $0.20 budget for this phase.

Each skill follows the four-section schema (`## Method`,
`## Parameters`, `## Commands / Code Snippets`, `## Notes for R-analysis
agent`) wrapped in the adapter's YAML front matter. DESeq2 and alevin
skills carry runnable R snippets; MethPat / Conesa / Marioni / 10x
Chromium emit `(No code snippets visible on provided pages.)` as
designed.

## Manifest stats (`experiments/skills/manifest.json`)

- Schema `version: 1`.
- `by_workflow_id`: 8 workflows have at least one available skill
  (DESeq2, alevin, MethPat, Minigraph-Cactus, 10x Chromium, Marioni
  attached to two pipeline wrappers, and Conesa RNA-seq best
  practices).
- `by_task_id`: **1** of 12 real tasks has a paper-derived skill →
  `akinyi_deseq2` maps to Conesa 2016 via
  `akinyi-onyango-rna_seq_pipeline-finish`.
- `tasks_without_skill`: **11** —
  `riya_limma`, `snakepipes_merge_fc`, `snakepipes_merge_ct`,
  `chipseq_plot_peak_intersect`, `chipseq_plot_macs_qc`,
  `chipseq_plot_homer_annot`, `snakepipes_scrna_merge_coutt`,
  `snakepipes_scrna_qc`, `epigenbutton_mapping_stats`,
  `epigenbutton_peak_stats`, `smartseqtotal_violin`.

  These tasks' `pipeline_workflow_id` either does not exist in the
  literature map (e.g. `RiyaDua-cervical-cancer-snakemake-workflow`,
  `joncahn-epigeneticbutton`, `snakemake-workflows-chipseq`,
  `gersteinlab-ASTRO`), or their mapped DOIs have no PDF under
  `literature/pdfs/` (SnakePipes `10.1093/bioinformatics/btz436`).

Skill `akinyi_deseq2 ← Conesa 2016` is a *survey* paper, not a direct
DESeq2 derivation. The `akinyi_deseq2` task's underlying R script does
use DESeq2, and the DESeq2 SKILL.md (doi_safe
`10.1186_s13059-014-0550-8`) is a stronger match — but the per-workflow
mapping in `workflow_literature_map.json` points the Akinyi workflow
at the best-practices survey. See recommendations below.

## `batch_runner.py` changes

- New flag `--skill-manifest <path>` (optional; ignored with
  `--smoke`).
- Added helpers `_load_skill_manifest`, `_resolve_task_skill`,
  `_render_sys_prompt`. The latter only rewrites the sys_prompt when
  a manifest is supplied AND the template contains the literal token
  `{{SKILL_MD}}`. Absence of either is a no-op, so old configs keep
  working unchanged.
- When injection occurs the run's `metadata.json` gains a `skill`
  dict: `injected`, `source_doi`, `source_tool`, `skill_md_path`,
  `pipeline_workflow_id`, `skill_sha256`, `skill_char_len`,
  `manifest_version`. When no skill is available but the manifest was
  loaded, `injected: false` plus `reason: no_skill_for_task` is
  recorded so the no-skill arm is still reproducibly identified.
- Per-task INFO log line is emitted for both injection paths.

## Config created

`experiments/llm_skill_ablation/config_llm_with_skill_v2.yaml` — same
`max_steps`, `llm_model.name`, and `temperature` as v1; only the
`sys_prompt` differs. It now contains the literal `{{SKILL_MD}}`
placeholder (see Subagent B's `comparison.md` §"Concrete plug-in").

## Smoke test — `akinyi_deseq2`

- Batch id: **`skill_smoke_20260416T160459Z`**
- Command:
  ```bash
  python3 -m paper_primary_benchmark.ldp_r_task_eval.batch_runner \
    --registry paper_primary_benchmark/ldp_r_task_eval/r_tasks/registry.real.akinyi_only.json \
    --config paper_primary_benchmark/experiments/llm_skill_ablation/config_llm_with_skill_v2.yaml \
    --skill-manifest paper_primary_benchmark/experiments/skills/manifest.json \
    --batch-run-id skill_smoke_20260416T160459Z
  ```
- metadata.json recorded
  `skill.injected=true`,
  `source_doi=10.1186/s13059-016-0881-8`,
  `skill_sha256=482a34902260b65139534da51f43a74c04931d3d36e0b78a1497f21931f3bd75`,
  `skill_char_len=1701`, `manifest_version=1`.
- Evaluator verdict: **pass** — both expected files
  (`deseq2_up.txt`, `deseq2_down.txt`) produced, byte-identical with
  reference.

A single-task registry helper file
`ldp_r_task_eval/r_tasks/registry.real.akinyi_only.json` was created
to isolate the smoke run; it is a trivial filter over
`registry.real.json` and is safe to delete or keep for repeat runs.

## Backward compatibility check

Confirmed by unit-level probe (`_render_sys_prompt`) and by the smoke
run itself:

- `--skill-manifest` absent → sys_prompt is passed through unchanged,
  no `skill` block appears in metadata.json.
- `--skill-manifest` present, template has no `{{SKILL_MD}}` → also a
  no-op, but the metadata block is populated so the experiment arm is
  distinguishable in the registry of runs.
- `--skill-manifest` present, template has `{{SKILL_MD}}` → placeholder
  is replaced per task; tasks in `tasks_without_skill` get the literal
  string `"(No paper-derived skill is available for this task.)"`
  so the prompt keeps a stable shape.

## Recommendations for the coordinator

1. **Priority task for the final sweep: `akinyi_deseq2`** — it is the
   only task that currently has a genuine paper hit end-to-end, and
   it is the one we know we can evaluate deterministically (sha256
   match on both output files). Run it on all four arms.

2. **Re-target `akinyi-onyango-rna_seq_pipeline-finish` to DESeq2**.
   The underlying script is a vanilla DESeq2 workflow; swapping its
   *primary* citation from Conesa 2016 (survey) to Love 2014 (DESeq2)
   in `workflow_literature_map.json` would make the injected skill
   much more actionable (it already contains the
   `DESeqDataSetFromMatrix → DESeq → results` call sequence). I did
   not make this change because the map is a literature citation
   registry and the Conesa entry was deliberately chosen by upstream;
   I'm flagging it for your call.

3. **Expand PDF coverage to unlock more tasks**. The fastest wins
   are:
   - `RiyaDua-cervical-cancer-snakemake-workflow` → unlocks
     `riya_limma`; primary method is *limma* (Ritchie et al.,
     Nucleic Acids Res. 2015, `10.1093/nar/gkv007`). The DOI is
     already in the map under `epigen-dea_limma-finish`; we just
     need to (a) add an entry for the RiyaDua workflow and (b)
     download the PDF.
   - `snakemake-workflows-chipseq` → unlocks 3 chipseq plotting
     tasks; the primary citation is either the ENCODE ChIP-seq
     guidelines (`10.1186/gb-2012-13-8-r51`, already in the map) or
     MACS2 (`10.1186/gb-2008-9-9-r137`); neither PDF is downloaded.
   - `maxplanck-ie-snakepipes-finish` → unlocks 4 SnakePipes tasks;
     DOI `10.1093/bioinformatics/btz436` is in the map, PDF missing.

4. **Vision adapter page budget is probably fine at 8**. The longest
   paper in the set is Minigraph-Cactus (54 preprint pages); the
   adapter still extracted a coherent Methods distillation from the
   first 8. For deep-methodology papers where we know the Methods
   section sits further in (e.g. supplemental-heavy Nature methods
   papers), bumping to `--pages 12` would cost ~1.5× input tokens
   (~$0.03 → $0.045 / paper) and is almost certainly worth it. I'd
   recommend `pages=12` for the next re-generation if we expand the
   PDF set; for the current 7 the added pages would hit references
   and figures, not more methods, so staying at 8 is a reasonable
   default.

5. **Consider a per-task DOI override** (future work). The current
   mapping is per-workflow; several workflows have multiple
   citations where the "right" one depends on the sub-script. A
   minimal extension: add `task_overrides: {task_id: doi}` to the
   manifest builder. Not needed for this round since only
   `akinyi_deseq2` is eligible.

## Deliverables index

- `experiments/skills/<7 doi_safe>/SKILL.md` + `run_manifest.json`
- `experiments/skills/manifest.json`
- `experiments/skills/_STATUS.md` (this file)
- `experiments/llm_skill_ablation/config_llm_with_skill_v2.yaml`
- `literature/_DOI_AUDIT.md`
- `literature/workflow_literature_map.json` (→ version 2, with
  `audit_notes`)
- `literature/pdfs/10.1101_gr.079558.108.pdf` (new),
  `literature/pdfs/10.1038_s41587-023-01793-w.pdf` (re-fetched)
- `ldp_r_task_eval/batch_runner.py` (now supports
  `--skill-manifest`)
- `ldp_r_task_eval/r_tasks/registry.real.akinyi_only.json` (one-task
  registry used for the smoke run; safe to keep or delete)
- `ldp_r_task_eval/runs/batch_skill_smoke_20260416T160459Z/` (smoke
  run artifacts — trajectory + metadata + evaluator verdict)
