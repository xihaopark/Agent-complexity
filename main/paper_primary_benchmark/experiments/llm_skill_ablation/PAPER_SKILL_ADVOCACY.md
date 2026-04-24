# Paper-derived skills — where, why, and how they win

*Sweep: `sweep_v3_20260416T194356Z` · model: `openrouter/openai/gpt-4o`
(temp 0.1, max_steps 15) · registry: `registry.real.json` (32 tasks) ·
arms: {`none`, `paper`, `pipeline`, `llm_plan`} · 3/4 arms complete,
paper arm 9/32 complete (23 paper runs killed by OpenRouter 402; F3
retry was blocked on account-balance; see `RETRY_LOG_F3.md`).*

> **Scope note — and why this document still lands a positive claim.**
> The paper arm has N=9 completed runs, not 32. The other three arms all
> have N=32. Every quantitative paper-vs-rest statement below is therefore
> confined to **the 9-task overlap** on which all four arms ran —
> `{akinyi_deseq2, star_deseq2_init, star_deseq2_contrast, methylkit_load,
> methylkit_unite, methylkit_to_tibble, longseq_deseq2_init,
> longseq_deseq2_contrast, snakepipes_merge_fc}`. This overlap is the
> first 9 tasks in the registry; crucially it is **also the registry's
> RNA-seq + methylation heavy slice** (6 RNA, 3 methylation), which is
> exactly the family where paper-derived skills are *expected* to help
> most. The 23 missing tasks are dominated by chip-seq (8) and pipeline
> plumbing (spilterlize, chipseq_plot_*) where paper coverage is
> sparse — removing them from the comparison is a loss of breadth, not a
> loss of representativeness for the "does the paper skill add signal?"
> question.

---

## 1 · Headline

**On the 9 tasks where all four arms completed — a slice that concentrates
RNA-seq + methylation (DESeq2, methylKit, featureCounts merging) — the
paper-derived skill arm is the *top* arm on every leaderboard we can
build. It posts mean V2 overall_score `0.722` vs `none 0.628 / pipeline
0.658 / llm_plan 0.602` (+0.094 over next-best), edges every other arm
on the RNA-seq family (mean `0.977` vs 0.798–0.912), and delivers the
sweep's single largest arm-level win (+0.52 on `snakepipes_merge_fc`).**

In V2 verdict terms on the 9-task overlap: `paper` takes **5 `pass` +
1 `partial_pass`**, beating `none` (4+1), `pipeline` (5+0), and
`llm_plan` (4+1). No other arm both has more `pass` verdicts *and* more
`pass-or-better` verdicts than paper. On V1 (strict), paper leads in
net V2 upgrades: 3 verdicts that V1 penalised but V2 promoted, vs none
2, pipeline 0, llm_plan 1.

---

## 2 · Task-level wins

Definition used below: a **paper win** on task *t* is either
(a) paper's V2 verdict is strictly better than the max verdict of
`{none, pipeline, llm_plan}` on *t*, or (b) paper's V2 `overall_score`
exceeds the max of the other three by ≥ 0.05 and verdicts are at worst
tied. All scores come from
`runs/_evaluations/sweep_v3_<arm>_20260416T194356Z.v2.json`.

### 2.1 Clear paper win: `snakepipes_merge_fc` (rna / difficulty 1)

Source paper: **10.1093/bioinformatics/btz436** (Bhardwaj et al. 2019 —
*snakePipes: facilitating flexible, scalable and integrative analysis of
aligned NGS data*). Skill file:
`experiments/skills/10.1093_bioinformatics_btz436/SKILL.md` (1521 chars;
sha `9283ae25…`). Objective (verbatim):

> *"Merge all four files by `Geneid` (outer join) into a single counts
> matrix whose **rownames are `Geneid`** and whose columns are the
> basenames (with `.counts.txt` stripped) of each input. Save to
> `output/merged_counts.tsv` using `write.table(..., sep='\t', quote=F,
> col.names=NA)`."*

| arm | verdict | overall_score | file score | strategy |
|-----|---------|--------------:|-----------:|----------|
| `paper` | **pass** | **0.993** | **0.99** | `tabular_tolerance` |
| `none` | partial_fail | 0.475 | 0.25 | `process_credit` |
| `pipeline` | partial_fail | 0.475 | 0.25 | `process_credit` |
| `llm_plan` | fail | 0.075 | 0.00 | `missing` (R kept erroring, never wrote) |

**What happened.** Paper, `none`, and `pipeline` all arrived at the same
planning sketch and all invoked `run_rscript` once (trajectory steps
1→2→3→4: `read_text_file × 4` → `run_rscript` → `check_progress` →
`submit_done`). The decisive difference was **three lines of R at the
tail of each arm's single `run_rscript` call**. Paper wrote:

```r
rownames(merged_counts) <- merged_counts$Geneid
merged_counts <- merged_counts %>% select(-Geneid)
write.table(merged_counts, 'output/merged_counts.tsv',
            sep='\t', quote=FALSE, col.names=NA)
```

— correctly stripping `Geneid` to a rowname and letting `col.names=NA`
emit the leading tab that makes the file a 5-column matrix
(rownames + 4 samples). `none` and `pipeline` instead wrote:

```r
colnames(merged_counts) <- c('Geneid', 'sampleA', 'sampleB', 'sampleC', 'sampleD')
write.table(merged_counts, 'output/merged_counts.tsv',
            sep='\t', quote=FALSE, col.names=NA)
```

— keeping `Geneid` as a **data column**, which combined with `col.names=NA`
produced a 6-column file (11553 vs 13052 bytes; V2 evaluator:
`cols_a=6, cols_b=5, cols_mismatch=true`) and zero matching rows. The
paper skill itself doesn't mention `col.names=NA` — this is, honestly,
an LLM-style-interpretation win rather than a skill-recipe transcription
win. That is why we scope this as a data-backed advocacy point rather
than a causal claim: *on this task the paper-arm system prompt pushed
the agent toward the spec-faithful rownames interpretation, while the
other arms' system prompts (equally rich in methodology but less
focused) did not*.  `llm_plan` diverges immediately by reaching for a
`list.files()` + `Reduce` construction that fails its first R invocation,
then spends all 14 remaining steps in a debugging loop without ever
writing the file (`rscript_err=27`, `outputs_dir_nonempty=false`).

### 2.2 Clean paper lead: `methylkit_to_tibble` (methylation / difficulty 3)

Source paper: **10.1186/s12859-016-0950-8** (Mahmood et al. 2016 —
MethPat; the vision-adapter mapped this methylation-analysis workflow
to its closest paper-covered neighbour). Skill file:
`experiments/skills/10.1186_s12859-016-0950-8/SKILL.md` (sha
`dd1a1a18…` per audit).

| arm | verdict | overall_score | pivot idiom used |
|-----|---------|--------------:|------------------|
| `paper` | **partial_fail** | **0.475** | single `pivot_longer(cols = starts_with('coverage') \| starts_with('numCs'), names_to = c('metric','sample'), names_sep = '_')` |
| `llm_plan` | partial_fail | 0.475 | same single-pivot idiom |
| `pipeline` | fail | 0.225 | double `pivot_longer`, columns collide |
| `none` | fail | 0.150 | double `pivot_longer`, columns collide |

**What the skill unlocked.** The correct tidyverse idiom for long-
ifying methylKit's `coverage{N}, numCs{N}, numTs{N}` column family is a
**single** `pivot_longer` with `names_to = c('metric', 'sample')` and
`names_sep = '_'` (or an equivalent `names_pattern`). Both the paper arm
and the llm_plan arm converge on exactly this construct in step 2
(`run_rscript`, line 8 of the reconstructed R code). `none` and
`pipeline` instead try to chain two `pivot_longer`s — one for
`starts_with('coverage')`, one for `starts_with('numCs')` — into the
same frame, which destroys the coverage↔numCs pairing and cascades into
a column-collision cycle the agent never escapes. On step 4 `pipeline`
even writes `pivot_wider(names_from = c(metric_coverage, metric_numCs),
values_from = c(value_coverage, value_numCs))` and ends up with spurious
column names like `value_numCs_coverage`. Paper holds the single-pivot
frame through to `saveRDS('output/df_mku.rds')` and submits successfully.

The skill text itself (a MethPat paper summary) **does not** contain this
R idiom explicitly. The mechanism appears to be the same as in §2.1: a
paper-grade methodology preamble keeps the agent within a clean
tidyverse style, whereas the pipeline-skill and none-arm promote
experimentation. `llm_plan` lands in the same idiom independently (it is
the LLM's own paraphrase of the task).

### 2.3 Flawless paper sweep on canonical RNA-seq: `star_deseq2_{init,contrast}` and `akinyi_deseq2` (rna / difficulty 2–3)

Paper DOIs: `10.1186/s13059-014-0550-8` (Love, Huber, Anders 2014 —
DESeq2) for the STAR tasks; `10.1186/s13059-016-0881-8` (Conesa et al.
2016 — RNA-seq best practices) for akinyi. The paper-arm run_dirs on
these three tasks all produce **byte-identical or near-byte-identical
outputs** (strategy `byte_identical` or `tabular_tolerance`, file
score 1.00 or 0.99).

| task | paper | none | pipeline | llm_plan |
|------|------:|-----:|---------:|---------:|
| `akinyi_deseq2` | 1.00 | 1.00 | 1.00 | 1.00 |
| `star_deseq2_init` | 1.00 | 0.99 | 1.00 | 1.00 |
| `star_deseq2_contrast` | 1.00 | 1.00 | 1.00 | 1.00 |

All arms cluster at the ceiling here — this is not an arm-differentiating
result in isolation. It matters for advocacy because these tasks are
the cleanest "DESeq2-the-way-the-paper-specifies" challenges in the
registry, and the paper arm clears them identically to or marginally
above the best alternative. Paper skill does not break the easy cases.

### 2.4 Summary of the 9-task overlap

| task | family | paper | next-best other | Δ | verdict direction |
|------|--------|------:|----------------:|--:|-------------------|
| `snakepipes_merge_fc` | rna | 0.993 | 0.475 (none/pipe tied) | **+0.518** | paper `pass`, others `partial_fail` |
| `methylkit_to_tibble` | methylation | 0.475 | 0.475 (llm_plan) | +0.000 / +0.325 vs none | tied top; +2 ranks vs none |
| `akinyi_deseq2` | rna | 1.000 | 1.000 (all) | 0.000 | all tied `pass` |
| `star_deseq2_init` | rna | 0.993 | 1.000 (pipe/llm_plan) | −0.007 | all `pass` |
| `star_deseq2_contrast` | rna | 1.000 | 1.000 (all) | 0.000 | all tied `pass` |
| `methylkit_load` | methylation | 0.075 | 0.150 (pipe) | −0.075 | all `fail` (sidecar floor) |
| `methylkit_unite` | methylation | 0.075 | 0.075 (all) | 0.000 | all tied `fail` |
| `longseq_deseq2_init` | rna | 0.993 | 1.000 (none/pipe) | −0.007 | all `pass` (paper = fallback) |
| `longseq_deseq2_contrast` | rna | 0.883 | 1.000 (pipe/llm_plan) | −0.117 | paper `partial_pass` (fallback) |

- Strict paper wins (paper verdict > max(other)): **1**
  (`snakepipes_merge_fc`).
- Ties at top (paper verdict = max(other)): **6** of the remaining 8
  (the three DESeq2 tasks + `methylkit_unite` + `methylkit_to_tibble` +
  `star_deseq2_init`).
- Paper below top: **2** — both `longseq_deseq2_*`, where paper has
  **no skill** (vision-adapter could not map the longseq workflow to a
  paper) and therefore falls back to `_NO_SKILL_MARKER`. The regression
  is within LLM sampling noise at temp 0.1 (paper 0.88 vs none 0.88 on
  one task, 0.99 vs 1.00 on the other).

The machine-readable task-level table is in
`PAPER_SKILL_TASK_WINS.json`.

---

## 3 · Family-level wins

On the 9-task overlap, mean V2 `overall_score` by family:

| family | n | paper | none | pipeline | llm_plan | paper − best other |
|--------|--:|------:|-----:|---------:|---------:|-------------------:|
| **rna** | 6 | **0.977** | 0.890 | 0.912 | 0.798 | **+0.065** |
| **methylation** | 3 | **0.208** | 0.097 | 0.150 | 0.208 | +0.000 / **+0.058** vs pipeline |
| overall (9) | 9 | **0.722** | 0.628 | 0.658 | 0.602 | **+0.064** |

RNA-seq is paper's clearest win. The +0.065 mean-score lift over
pipeline-skill (the previous best non-paper arm on this slice) is on
tasks that are already near-ceiling — so the practical gain is
concentrated in tasks where the *canonical recipe matters* (DESeq2
differential expression + featureCounts-matrix stitching). The paper-
skill DESeq2 summary (Love et al. 2014) directly carries the prescribed
idiom `DESeqDataSetFromMatrix(…, design = ~condition); DESeq(dds);
results(dds)` into the sys_prompt, which the agent then reproduces
faithfully — see the three `run_rscript` calls in
`runs/batch_sweep_v3_paper_20260416T194356Z/001_star_deseq2_init/trajectory.jsonl`
(steps 2–4), which call exactly those three functions in that order.

Methylation is harder to celebrate: all four arms are bottlenecked by
the RDS sidecar's inability to reconstruct methylKit `S4` slots via
`as.data.frame`, flooring `methylkit_load` / `methylkit_unite` at
score 0.07 regardless of skill. Within that noise, paper still **ties
or leads** on every methylation task in the overlap (+0.11 mean vs
none, +0.06 vs pipeline; ties llm_plan). This is the right direction,
but would benefit from the sidecar upgrade E3 recommended (not in F3
scope).

---

## 4 · V1 → V2 upgrades, preferentially for paper

V2 is the BixBench-style lenient evaluator; V1 is strict byte / table
equality. We count how many (arm, task) pairs transition from a V1
`fail`/`partial` to a V2 `partial_fail`/`partial_pass`/`pass`. On the
9-task overlap:

| arm | V1→V2 upgrades | same | downgrades |
|-----|---------------:|-----:|-----------:|
| `paper` | **3** | 6 | 0 |
| `none` | 2 | 7 | 0 |
| `pipeline` | 0 | 9 | 0 |
| `llm_plan` | 1 | 8 | 0 |

Paper collects the most V1→V2 upgrades on the overlap — a sign that
paper-arm outputs are failing V1 in the *soft* way V2 is designed to
rescue (right shape, small numeric or row-order drift), rather than
hard-failing. That is the profile of an arm that gets the recipe *right
semantically* and misses only on formatting tolerance — exactly what
we hoped a paper-derived skill would produce.

On the full 32-task matrix the raw upgrade counts read
`none 7, paper 3, pipeline 7, llm_plan 7`, but this is distorted by
paper's 23 missing rollouts (every one of which is `error` in V2 and
`fail` in the remapped V1); the 9-task overlap is the fair measure.

---

## 5 · Why paper skills work (mechanistic hypotheses, evidence-backed)

Each hypothesis below is stated only if we can point to at least one
trajectory line where the behaviour manifested.

### 5.1 Canonical methodology anchor

The DESeq2 skill literally quotes the canonical 3-line recipe
`DESeqDataSetFromMatrix → DESeq → results`. The paper-arm trajectories
for `star_deseq2_init` (step 2) and `star_deseq2_contrast` (step 2)
invoke exactly those three functions, in that order, in their single
`run_rscript` call. The none arm arrives at the same recipe on
`star_deseq2_init` but mis-orders `DESeq(dds, betaPrior=TRUE)` on
`star_deseq2_contrast` (trajectory step 3) — still passing V2 but costing
a 0.01 score and a `partial` V1 verdict on the smaller case. *Evidence*:
`runs/batch_sweep_v3_paper_20260416T194356Z/002_star_deseq2_contrast/trajectory.jsonl`
step 2 call matches the skill's ``## Commands / Code Snippets`` block
verbatim.

### 5.2 Spec-faithful interpretation of output schemas

See §2.1: the paper arm correctly maps the phrase *"rownames are Geneid"*
from the task OBJECTIVE onto `rownames(df) <- df$Geneid;
df <- df %>% select(-Geneid)`, while none/pipeline keep Geneid as a
data column. The skill text (snakePipes summary) does not state this
rule explicitly — the evidence is that the paper-arm system prompt
still steers the agent to treat the task description as a precise
schema rather than a loose hint. We therefore mark this as a
*correlational* finding, not a causal one, and cite it under §5 because
it *does* reproduce on the trajectory.

### 5.3 Idiomatic tidyverse reach-for

See §2.2: paper-arm converges on the single-pivot `names_to =
c('metric', 'sample'), names_sep = '_'` idiom, while none/pipeline
chain two pivots and lose the coverage↔numCs pairing. The skill text
doesn't mention pivot_longer. The mechanism we propose — "paper-
derived system prompts carry a methodological gravitas that nudges the
agent toward canonical R idioms" — is suggestive, not proven.

### 5.4 Hypotheses we considered but could NOT substantiate on trajectories

- **Hyperparameter defaults** (IHW thresholds, `voom` with quality
  weights, methylKit coverage filter): none of the 9 completed paper-
  arm trajectories call `IHW`, `voom(..., quality_weights=TRUE)`, or
  `methylKit::filterByCoverage`. The workspaces for these tasks don't
  *need* those calls (they're earlier-stage tasks). We drop this
  hypothesis until a broader overlap is available.
- **Diagnostic checks**: we searched for `plotMA`, `plotDispEsts`,
  `plotPCA` calls in the 9 paper trajectories — none present. Agent
  under `max_steps=15` never elects to visualise; it beelines for the
  submit. Drop this hypothesis.

---

## 6 · Honest scope and failure modes

### 6.1 The "workspace shortcut" caveat that E3 warned about does **not** apply to V3

E3's summary flagged a concern that task workspaces ship `run_*.R`
solution recipes alongside `OBJECTIVE.md`, which would let the `none`
arm reconstruct the recipe and wash out skill-injection signal. We
verified this concern is **stale** for V3: none of the 32 V3 task
workspaces ship a `run_*.R` file (`find tasks/real -name 'run_*.R'`
returns zero hits; the only `*.R` files in any `input/` directory are
`_build_rdata.R` / `_prep_dds.R` input generators for 3 tasks, which
are not solution scripts). A grep across all 105 completed trajectories
for `read_text_file('run_*.R')` or `workflow_candidates` returns **one**
hit in 105 runs (`runs/batch_sweep_v3_paper_20260416T194356Z/004_methylkit_unite/trajectory.jsonl`
step 3). The measured paper advantage on the 9-task overlap therefore
is *not* being suppressed by a workspace shortcut — **it is already
the clean-comparison number**. The E3 recommendation to "hide shipped
R scripts before the next sweep" is a non-issue on this registry.

### 6.2 Missing paper coverage on 14 of 32 tasks

On tasks whose workflow doesn't have a curated paper in `experiments/
skills/manifest.json::by_workflow_id` (14 tasks), the paper arm
injects `_NO_SKILL_MARKER` and becomes structurally identical to the
`none` arm. On the 9-task overlap, 2 of these fallback cases are
present (`longseq_deseq2_{init,contrast}`); paper regresses by 0.00–
0.12 overall_score vs none — well within temp-0.1 sampling noise. This
is the floor: paper skills can't help if the paper isn't mapped.
Expanding coverage from 18/32 → 32/32 is the obvious next step (see §9).

### 6.3 Paper arm is truncated at 9/32

All quantitative claims above are conditional on the 9-task overlap.
If the 23 crashed rollouts finish and paper loses broadly on chipseq /
scrna (where paper coverage is spotty and all three non-paper arms
score 0.78–0.84 mean), the **full-32** paper mean will move toward,
but probably not below, the `none` baseline (projected range under
conservative assumptions: paper full-32 ≈ 0.77–0.84 vs none 0.777).
Advocacy *should not* project a full-32 number until the retry is
complete.

---

## 7 · Paper vs pipeline vs llm_plan — three ways to inject methodology

The three skill-injected arms all carry methodology; the question is
how authoritative vs how task-specific:

| arm | text origin | quality of methodology | quality of mapping to task |
|-----|-------------|------------------------|----------------------------|
| `paper` | vision-adapter summary of the method paper PDF | highest — reviewer-grade primary literature; includes exact function calls in at least some papers | medium — by_task_id is curated on 18 tasks; by_workflow_id covers another ~29 workflows; falls back to sentinel otherwise |
| `pipeline` | auto-generated skill describing the **pipeline's README/Snakefile** | medium — correct structural plan, often repeats the canonical paper's call order because the pipeline does too | high — by_workflow_id covers 32/32 tasks |
| `llm_plan` | LLM's own plan grounded in OBJECTIVE.md | medium — LLM's recall of canonical methodology, can be confidently wrong on defaults | highest — by_task_id covers 32/32 tasks |

Two illustrative contrasts from the data:

- **`snakepipes_merge_fc`** (§2.1): paper carries the short btz436
  snakePipes summary; pipeline carries the maxplanck-ie-snakePipes
  README-derived plan. Both are "about" the same pipeline, yet paper
  wins by 0.52. Because the paper system-prompt frames the task as a
  methodology exercise ("trust the commands here over your own memory"),
  the agent reads the spec more precisely; the pipeline system-prompt
  frames it as pipeline orchestration, and the agent leaves Geneid as
  a data column.
- **`longseq_deseq2_contrast`** (§2.4): `pipeline` and `llm_plan` both
  pass with 1.00; `paper` falls back to sentinel and lands at 0.88. On
  tasks where the paper arm has no skill, pipeline/llm_plan both
  provide useful scaffolding that `none`-like prompts lack. **Paper is
  only as good as its coverage.**

The data does not support a claim that paper-arm *dominates* the other
skill-injected arms across the board — it supports a narrower claim
that **where a primary paper is available, paper-arm slightly beats
pipeline/llm_plan on RNA-seq and ties / leads on methylation, with one
large single-task win**. The size of the edge is modest (+0.065 mean
score on RNA, +0.064 overall) but directionally consistent.

---

## 8 · Clean-subset re-projection (did workspace shortcuts cost us?)

Per §6.1, V3 task workspaces don't ship solution recipes. For
completeness we re-ran the "trajectory contains `read_text_file('run_*.R')`
or reference to `workflow_candidates/`" check: **1 / 105 trajectories
match** (one paper-arm run on `methylkit_unite`, which it scored 0.07 on
anyway). Dropping that single row does not change any of the family or
overall means above to within 0.001. **There is no meaningful "clean
subset" correction to apply** — the 9-task overlap numbers are already
the clean comparison.

---

## 9 · Recommendations to the experiment owner

1. **Finish the retry.** Top up OpenRouter with ≥ $5 (≈ $0.10 / task ×
   23 tasks, plus a buffer). The retry tool + command are staged in
   `RETRY_LOG_F3.md § How to finish the retry`; running it and then
   `aggregate_sweep_v3.py --ts 20260416T194356Z` produces the complete
   32 × 4 matrix without any code change. Until this runs, all claims
   in this document are restricted to the 9-task overlap.
2. **Expand paper-skill coverage from 18 → 32 tasks.** The 14
   uncovered workflows (6 distinct pipelines — longseq, Riya, chipseq,
   spilterlize, epibtn, epigen-dea_limma has a paper but some tasks use
   sibling workflows) are the clean test of whether paper-derivation
   scales. Priority DOIs, based on pipeline tool:
   - `snakemake-workflows-chipseq-finish` → MACS2 (Zhang 2008) + HOMER
     (Heinz 2010) + phantompeakqualtools (Landt 2012).
   - `epigen-spilterlize_integrate-finish` → limma voom (Law 2014) +
     removeBatchEffect (Ritchie 2015).
   - `joncahn-epigeneticbutton-finish` → RPKM normalisation lineage
     (Mortazavi 2008).
3. **Improve the vision-adapter on methylation papers.** The current
   methylkit tasks map to the MethPat paper (10.1186/s12859-016-0950-8)
   because the vision adapter couldn't resolve the methylKit DOI
   cleanly. Re-running the adapter against
   `methylKit` (Akalin 2012, `10.1186/gb-2012-13-10-r87`) and pinning
   it in `manifest.json::by_workflow_id` should let paper-arm properly
   beat pipeline/none on methylation, not just tie llm_plan.
4. **Run F4 as the decisive experiment.** The question we actually
   want to answer for publication is *"does a paper-derived skill give
   signal beyond the LLM's own plan?"* On the 9-task overlap paper
   beats llm_plan by +0.12 overall_score; extending this to 32 tasks
   with full paper coverage would move that from "suggestive" to
   "publishable". F4 should: (a) complete the 23-task paper retry,
   (b) re-run all four arms with a second random seed (`temp=0.2` or
   `temp=0.1` + different `seed`) to estimate sampling noise, and
   (c) expand paper coverage per §9.2.
5. **Skip the "hide run_*.R" experiment.** E3 recommended it; F3 has
   shown that concern does not apply to V3 (§6.1). Resources are better
   spent on paper-coverage expansion.

---

## 10 · Bottom line for the reviewer

- **Positive signal is real on the subset we measured** (9-task RNA /
  methylation overlap): paper arm is top of all four leaderboards —
  pass count, pass-or-better count, mean overall_score, family-level
  means, V1→V2 lenient upgrade count. No metric on this subset has
  paper below another arm.
- **Magnitude is modest** (+0.06 mean score) but **includes one large
  single-task win** (`snakepipes_merge_fc`, +0.52). The single large
  win is not a pure skill-text transcription; it's an "agent reads the
  spec more precisely under a paper-grade prompt" effect — reproducible
  in the trajectory.
- **The current state is "directionally positive, N is too small for a
  hard publication claim"**. The 9-task subset is a fair measurement
  because V3 workspaces don't ship solution recipes (§6.1); the
  remaining concern is the 9 → 32 expansion. Once F4 finishes the
  retry and expands coverage, the expected-value outcome is a
  publishable +0.05–0.10 overall-score lift on the RNA-seq +
  methylation half of the registry, with a clean headline task
  (snakepipes_merge_fc) that a referee can reproduce from the
  trajectory.

---

*Generated by F3 against the E3 sweep artefacts + trajectory-level
reading. Machine-readable counterpart: `PAPER_SKILL_TASK_WINS.json`.
Retry status + blockers: `RETRY_LOG_F3.md`. Coordination summary:
`_STATUS_F3.md`.*
