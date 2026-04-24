# Skill coverage matrix — V3

Generated from manifests at 2026-04-17. Tasks: 32.

- Paper manifest version: 3 | by_workflow_id: 29 | by_task_id: 18
- Pipeline manifest version: 3 | by_workflow_id: 16
- LLM-plan manifest version: 3 | by_task_id: 32

| task_id | workflow_id | has_paper | has_pipeline | has_llm_plan |
|---|---|---|---|---|
| akinyi_deseq2 | akinyi-onyango-rna_seq_pipeline-finish | Y | Y | Y |
| star_deseq2_init | rna-seq-star-deseq2-finish | Y | Y | Y |
| star_deseq2_contrast | rna-seq-star-deseq2-finish | Y | Y | Y |
| methylkit_load | fritjoflammers-snakemake-methylanalysis-finish | Y | Y | Y |
| methylkit_unite | fritjoflammers-snakemake-methylanalysis-finish | Y | Y | Y |
| methylkit_to_tibble | fritjoflammers-snakemake-methylanalysis-finish | Y | Y | Y |
| longseq_deseq2_init | snakemake-workflows-rna-longseq-de-isoform | N | Y | Y |
| longseq_deseq2_contrast | snakemake-workflows-rna-longseq-de-isoform | N | Y | Y |
| snakepipes_merge_fc | maxplanck-ie-snakepipes-finish | Y | Y | Y |
| snakepipes_merge_ct | maxplanck-ie-snakepipes-finish | Y | Y | Y |
| riya_limma | RiyaDua-cervical-cancer-snakemake-workflow | N | Y | Y |
| chipseq_plot_macs_qc | snakemake-workflows-chipseq-finish | N | Y | Y |
| chipseq_plot_homer_annot | snakemake-workflows-chipseq-finish | N | Y | Y |
| snakepipes_scrna_merge_coutt | maxplanck-ie-snakepipes-finish | Y | Y | Y |
| snakepipes_scrna_qc | maxplanck-ie-snakepipes-finish | Y | Y | Y |
| spilterlize_filter_features | epigen-spilterlize_integrate-finish | N | Y | Y |
| spilterlize_norm_voom | epigen-spilterlize_integrate-finish | N | Y | Y |
| spilterlize_limma_rbe | epigen-spilterlize_integrate-finish | N | Y | Y |
| spilterlize_norm_edger | epigen-spilterlize_integrate-finish | N | Y | Y |
| dea_limma | epigen-dea_limma-finish | Y | Y | Y |
| msisensor_merge | snakemake-workflows-msisensor-pro-finish | Y | Y | Y |
| methylkit_filt_norm | fritjoflammers-snakemake-methylanalysis-finish | Y | Y | Y |
| methylkit2tibble_split | fritjoflammers-snakemake-methylanalysis-finish | Y | Y | Y |
| methylkit_remove_snvs | fritjoflammers-snakemake-methylanalysis-finish | Y | Y | Y |
| phantompeak_correlation | snakemake-workflows-chipseq-finish | N | Y | Y |
| nearest_gene | maxplanck-ie-snakepipes-finish | Y | Y | Y |
| chipseq_plot_frip_score | snakemake-workflows-chipseq-finish | N | Y | Y |
| chipseq_plot_peaks_count_macs2 | snakemake-workflows-chipseq-finish | N | Y | Y |
| chipseq_plot_annotatepeaks_summary_homer | snakemake-workflows-chipseq-finish | N | Y | Y |
| epibtn_rpkm | joncahn-epigeneticbutton-finish | N | Y | Y |
| snakepipes_scrna_report | maxplanck-ie-snakepipes-finish | Y | Y | Y |
| clean_histoneHMM | maxplanck-ie-snakepipes-finish | Y | Y | Y |

## Summary
- Tasks with paper skill: 18/32
- Tasks with pipeline skill: 32/32
- Tasks with llm_plan skill: 32/32

## Missing paper coverage (14 tasks)
Expected for workflows whose primary_doi is null or whose PDF C3 could not download (single-cell-rna-seq-finish, epigen-spilterlize_integrate-finish, snakemake-workflows-chipseq-finish, snakemake-workflows-rna-longseq-de-isoform, RiyaDua-cervical-cancer-snakemake-workflow, joncahn-epigeneticbutton-finish).

- longseq_deseq2_init (snakemake-workflows-rna-longseq-de-isoform)
- longseq_deseq2_contrast (snakemake-workflows-rna-longseq-de-isoform)
- riya_limma (RiyaDua-cervical-cancer-snakemake-workflow)
- chipseq_plot_macs_qc (snakemake-workflows-chipseq-finish)
- chipseq_plot_homer_annot (snakemake-workflows-chipseq-finish)
- spilterlize_filter_features (epigen-spilterlize_integrate-finish)
- spilterlize_norm_voom (epigen-spilterlize_integrate-finish)
- spilterlize_limma_rbe (epigen-spilterlize_integrate-finish)
- spilterlize_norm_edger (epigen-spilterlize_integrate-finish)
- phantompeak_correlation (snakemake-workflows-chipseq-finish)
- chipseq_plot_frip_score (snakemake-workflows-chipseq-finish)
- chipseq_plot_peaks_count_macs2 (snakemake-workflows-chipseq-finish)
- chipseq_plot_annotatepeaks_summary_homer (snakemake-workflows-chipseq-finish)
- epibtn_rpkm (joncahn-epigeneticbutton-finish)

## Bug: tasks missing pipeline skill (0)

## Bug: tasks missing llm_plan skill (0)
