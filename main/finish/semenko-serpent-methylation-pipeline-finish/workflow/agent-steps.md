# semenko-serpent-methylation-pipeline-finish LLM Execution Spec

## Purpose

- Source repository: `semenko__serpent-methylation-pipeline`
- Source snakefile: `../workflow_candidates/semenko__serpent-methylation-pipeline/workflow/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `get_reference_genome`
2. `mask_reference_fasta`
3. `biscuit_index`
4. `biscuit_qc_index`
5. `bwa_meth_index`
6. `wgbs_tools_index`
7. `md5sum`
8. `seqtk_subsample`
9. `fastp`
10. `bwa_meth`
11. `mark_nonconverted`
12. `samtools_fixmate_sort_markdup`
13. `samtools_index`
14. `samtools_statistics`
15. `biscuit_bed`
16. `biscuit_epiread`
17. `biscuit_qc`
18. `methyldackel_mbias_plots`
19. `fastqc_bam`
20. `goleft_indexcov`
21. `wgbs_tools_pat_beta`
22. `touch_complete_flag`
23. `multiqc`
24. `all`
