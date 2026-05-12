# Paper-sensitive R-task: deseq2_lrt_interaction

**Design intent:** detect a **treatment × timepoint interaction** in a factorial RNA-seq design. A common failure mode is running **Wald tests on main effects only** and missing the interaction term. DESeq2 supports **likelihood ratio tests (LRT)** between nested models.

**Conceptual source:** `rna-seq-star-deseq2-finish` (two-factor layout with interaction).

## Your goal

You are given:

- `input/counts.tsv` — gene × sample counts; first column `gene_id`.
- `input/coldata.tsv` — includes `sample`, `treatment` (`ctrl`,`trt`), and `time` (`t0`,`t1`).

You must test the **interaction** `treatment:time` (i.e. does the **time effect differ by treatment?`) using **DESeq2 LRT**:

- Full model: `~ treatment * time` (or equivalent parameterization)
- Reduced model: `~ treatment + time` (no interaction)
- Use `DESeq()` then `nbinomLRT()` / `results()` for LRT as appropriate, following DESeq2 documentation

Write:

- `output/interaction_de.csv` with columns **exactly**:  
  `gene_id,baseMean,log2FoldChange,stat,pvalue,padj`  
  for the **interaction** effect (treatment-specific change in the time effect).  
  `log2FoldChange` should be the interaction coefficient as reported by DESeq2 (or NA if not defined — then drop such rows before export).

Use `write.csv(..., row.names=FALSE)`.

## Deliverables

- `output/interaction_de.csv`

Then `submit_done(success=true)`.
