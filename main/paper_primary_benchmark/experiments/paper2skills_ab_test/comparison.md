# Paper2Skills comparison — Method 1 (vision adapter) vs Method 2 (template)

## DOIs evaluated

1. `10.1186/s13059-014-0550-8` — Love et al., *DESeq2* (Genome Biology, 2014)
2. `10.1186/s12859-016-0950-8` — Wong et al., *MethPat* (BMC Bioinformatics,
   2016). **Note**: mapped as "systemPipeR" in the workspace's
   `workflow_literature_map.json`, but the PDF content is MethPat. The
   vision adapter catches this; the template does not.

## Raw measurements

| Metric | DESeq2 (template) | DESeq2 (vision) | MethPat (template) | MethPat (vision) |
|---|---|---|---|---|
| Wall clock | ~0.3 s | 16.1 s (render 0.6 s + LLM 15.5 s) | ~0.3 s | 11.3 s (render 0.5 s + LLM 10.8 s) |
| Prompt tokens | 0 (no LLM) | 6,412 | 0 | 5,332 |
| Completion tokens | 0 | 417 | 0 | 284 |
| Total tokens | 0 | 6,829 | 0 | 5,616 |
| API cost estimate\* | $0 | ~$0.02 | $0 | ~$0.02 |
| Output size (SKILL.md) | ~13 kB raw text dump | ~1.5 kB structured | ~13 kB raw text dump | ~1.3 kB structured |

\* Using OpenRouter list prices for `openai/gpt-4o` (~$2.50 /M input,
~$10 /M output). Two papers: ~$0.04 total for the vision run; ~$0.14 per
1M input-token paper if we scaled to all 7 downloaded PDFs and kept
`pages=8`.

Run manifests with exact numbers are in
`vision_out/<doi>/run_manifest.json`.

## Page / section coverage

### Method 2 (template)

- Dumps the first N pages verbatim via `fitz.get_text("text")`, truncated
  to 12,000 characters.
- Captures Methods text **if** the paper's Methods section starts within
  the first ~8 pages (DESeq2: yes; MethPat: partial). No structural
  awareness — title, abstract, figure captions, references, and code
  listings are all mashed together.
- **No filtering, no distillation.** The downstream agent has to read
  10-13 kB of unstructured text and locate what matters.

### Method 1 (vision adapter)

- Renders pages 1-8 as PNG (130 DPI) and asks GPT-4o for exactly four
  sections: `## Method`, `## Parameters`, `## Commands / Code Snippets`,
  `## Notes for R-analysis agent`.
- For DESeq2: correctly names negative-binomial GLM + empirical-Bayes
  shrinkage, lists `DESeqDataSetFromMatrix`/`DESeq`/`results` call
  sequence, and flags rlog + Cook's-distance pitfalls.
- For MethPat: correctly identifies the tool (despite the mis-routed
  DOI) and notes that no R code is visible on the extracted pages
  (`(No code snippets visible on provided pages.)`).
- Output is ~1.5 kB — small enough to paste into a system prompt.

## Executability (what can the R-analysis agent actually do with this?)

- **Template → marginal**. The agent gets the abstract / front matter /
  possibly some methods text. There is no structured `Commands` block,
  no Parameters list, no "use package X". If the agent already knows
  DESeq2, the text doesn't hurt; if it does not, the text is a mild
  prior but still requires the agent to read through narrative prose.
- **Vision adapter → actionable**. The `## Commands / Code Snippets`
  block in the DESeq2 output is a drop-in runnable R snippet
  (`library(DESeq2); dds <- DESeqDataSetFromMatrix(...); DESeq(dds);
  results(dds)`). The `## Notes for R-analysis agent` block is
  explicitly optimised for prompt injection.
- **Neither method** produces runnable Python modules + tests like the
  full `external/Paper2Skills` does. For our ldp R-task benchmark, that
  layer is not needed — we feed SKILL.md into the system prompt, not
  into a code-import path.

## Qualitative side-by-side (DESeq2)

Template SKILL.md (first 20 non-YAML lines):
```
METHOD
Open Access
Moderated estimation of fold change and
dispersion for RNA-seq data with DESeq2
Michael I Love...
[…lots of prose…]
```

Vision-adapter SKILL.md:
```
## Method
DESeq2 is a statistical method for differential analysis of count data […]
It employs a generalized linear model (GLM) with a negative binomial
distribution […] empirical Bayes shrinkage […] MAP estimates.

## Parameters
- Normalization factors (s_ij) — adjusts for differences in sequencing depth…
- Dispersion parameter (α_i) — models within-group variability…
- Shrinkage degree (d_i) — controls the amount of shrinkage…
- Logarithmic fold change (LFC) threshold — hypothesis testing…

## Commands / Code Snippets
```r
library(DESeq2)
dds <- DESeqDataSetFromMatrix(countData = count_matrix,
                              colData = col_data, design = ~ condition)
dds <- DESeq(dds)
res <- results(dds)
```

## Notes for R-analysis agent
- Use the DESeq2 package in R…
- Handle outliers using Cook's distance…
- Consider rlog transformation for variance stabilisation…
```

## Failure modes observed

- **Template** silently propagates wrong DOI labels. `10.1186/s12859-016-0950-8`
  is labelled "systemPipeR" in `workflow_literature_map.json` but the PDF is
  MethPat — template output faithfully contains MethPat text under the
  systemPipeR-labelled directory, which would poison a with-skill prompt.
- **Vision** detected the title from page 1 and correctly described
  MethPat, so the agent would at least see *self-consistent* skill
  content even if the mapping is wrong. (Separate action item for the
  coordinator: audit `workflow_literature_map.json`.)
- **Vision** can hallucinate when code is not visible; we mitigated
  this in the system prompt (`If none are visible on the provided
  pages, write "(No code snippets visible on provided pages.)"`),
  and the MethPat run obeyed that instruction correctly.

## Verdict

**Use the vision adapter (Method 1) for the with-skill arm.** Reasons:

1. Produces structured SKILL.md sections that are prompt-injectable.
2. Includes an actionable R code snippet for DESeq2-class papers — the
   agent no longer has to guess the canonical call sequence.
3. Price (~$0.02 / paper, ~$0.14 for all 7 PDFs at `pages=8, dpi=130`)
   and latency (~11-16 s / paper) are negligible against a single
   `ldp` R-task run.
4. Resilient to mis-routed DOIs — the LLM describes what the PDF
   actually is, not what the mapping claims it is.
5. The full LangGraph `external/Paper2Skills` adds value for building
   a Python skill library (modules + tests + git branch) that we do
   not need for prompt-injected SKILL.md. If the project later wants
   a real skill library, switch to the full tool then.

The template method (Method 2) is fine as a fallback for papers where
no API key is available, or to pre-warm the `workflow_literature_map`
with metadata.

## Concrete plug-in for the coordinator (Phase D)

### A. Skill generation loop

For each of the 7 downloaded PDFs, run:

```bash
python3 main/paper_primary_benchmark/experiments/paper2skills_ab_test/vision_adapter.py \
  --pdf main/paper_primary_benchmark/literature/pdfs/<doi-safe>.pdf \
  --out-dir main/paper_primary_benchmark/experiments/skills/<doi-safe> \
  --pages 8 --dpi 130
```

### B. System-prompt snippet for `config_llm_with_skill.yaml`

Replace the current free-form "consult the workflow_literature_map"
paragraph with a deterministic "paste-the-skill-file" block. Drop this
into `experiments/llm_skill_ablation/config_llm_with_skill.yaml` (the
coordinator can template-render the `{{SKILL_MD}}` marker per task from
`workflow_literature_map.json` → `experiments/skills/<doi>/SKILL.md`):

```yaml
agent:
  sys_prompt: |
    You solve R-centric analysis tasks in a sandbox workspace. Use only
    the provided tools: run_shell, read_text_file, write_text_file,
    run_rscript, list_workdir, submit_done. Prefer R for numeric /
    statistical work. Do not assume Snakemake or external clusters.

    # Paper-derived skill (auto-generated from the method paper via
    # paper2skills_ab_test/vision_adapter.py). Trust the commands here
    # over your own memory when they disagree; fall back to your own
    # knowledge if the skill says a section is missing.

    {{SKILL_MD}}

    When the objective is satisfied, call submit_done(success=true).
```

If a task has no paper (no workflow_literature_map hit) or the paper is
not in `literature/pdfs/`, render the block as a single line
`(No paper-derived skill is available for this task.)` so the prompt
stays stable-shaped across tasks.
