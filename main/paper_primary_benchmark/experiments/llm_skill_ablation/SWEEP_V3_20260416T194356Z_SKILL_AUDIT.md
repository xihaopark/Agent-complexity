# Skill injection audit V3 — TS `20260416T194356Z`

Per-run audit: for each (arm, task_id) we confirm:

1. `metadata.json::skill.arm` equals the CLI arm.
2. `skill.injected` matches expectation (`false` for `none` and paper-fallback, `true` otherwise).
3. `skill.skill_sha256` equals the sha256 of the inline skill text recomputed from the manifest (re-running the same resolution rule as the batch runner).

| arm | task | workflow | arm_match | injected_expected | sha_match | got sha8 | expected sha8 | char_len | tag |
|-----|------|----------|:---------:|:-----------------:|:---------:|----------|---------------|---------:|-----|
| `none` | `akinyi_deseq2` | `akinyi-onyango-rna_seq_pipeline-finish` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `star_deseq2_init` | `rna-seq-star-deseq2-finish` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `star_deseq2_contrast` | `rna-seq-star-deseq2-finish` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `methylkit_load` | `fritjoflammers-snakemake-methylanalysis-finish` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `methylkit_unite` | `fritjoflammers-snakemake-methylanalysis-finish` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `methylkit_to_tibble` | `fritjoflammers-snakemake-methylanalysis-finish` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `longseq_deseq2_init` | `snakemake-workflows-rna-longseq-de-isoform` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `longseq_deseq2_contrast` | `snakemake-workflows-rna-longseq-de-isoform` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `snakepipes_merge_fc` | `maxplanck-ie-snakepipes-finish` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `snakepipes_merge_ct` | `maxplanck-ie-snakepipes-finish` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `riya_limma` | `RiyaDua-cervical-cancer-snakemake-workflow` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `chipseq_plot_macs_qc` | `snakemake-workflows-chipseq-finish` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `chipseq_plot_homer_annot` | `snakemake-workflows-chipseq-finish` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `snakepipes_scrna_merge_coutt` | `maxplanck-ie-snakepipes-finish` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `snakepipes_scrna_qc` | `maxplanck-ie-snakepipes-finish` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `spilterlize_filter_features` | `epigen-spilterlize_integrate-finish` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `spilterlize_norm_voom` | `epigen-spilterlize_integrate-finish` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `spilterlize_limma_rbe` | `epigen-spilterlize_integrate-finish` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `spilterlize_norm_edger` | `epigen-spilterlize_integrate-finish` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `dea_limma` | `epigen-dea_limma-finish` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `msisensor_merge` | `snakemake-workflows-msisensor-pro-finish` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `methylkit_filt_norm` | `fritjoflammers-snakemake-methylanalysis-finish` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `methylkit2tibble_split` | `fritjoflammers-snakemake-methylanalysis-finish` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `methylkit_remove_snvs` | `fritjoflammers-snakemake-methylanalysis-finish` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `phantompeak_correlation` | `snakemake-workflows-chipseq-finish` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `nearest_gene` | `maxplanck-ie-snakepipes-finish` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `chipseq_plot_frip_score` | `snakemake-workflows-chipseq-finish` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `chipseq_plot_peaks_count_macs2` | `snakemake-workflows-chipseq-finish` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `chipseq_plot_annotatepeaks_summary_homer` | `snakemake-workflows-chipseq-finish` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `epibtn_rpkm` | `joncahn-epigeneticbutton-finish` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `snakepipes_scrna_report` | `maxplanck-ie-snakepipes-finish` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `none` | `clean_histoneHMM` | `maxplanck-ie-snakepipes-finish` | ✓ | ✓ | ✓ | — | — | — | sentinel |
| `paper` | `akinyi_deseq2` | `akinyi-onyango-rna_seq_pipeline-finish` | ✓ | ✓ | ✓ | `67a57f25` | `67a57f25` | 1700 | expected_injection (by_task_id) |
| `paper` | `star_deseq2_init` | `rna-seq-star-deseq2-finish` | ✓ | ✓ | ✓ | `4aaf2fb8` | `4aaf2fb8` | 1881 | expected_injection (by_task_id) |
| `paper` | `star_deseq2_contrast` | `rna-seq-star-deseq2-finish` | ✓ | ✓ | ✓ | `4aaf2fb8` | `4aaf2fb8` | 1881 | expected_injection (by_task_id) |
| `paper` | `methylkit_load` | `fritjoflammers-snakemake-methylanalysis-finish` | ✓ | ✓ | ✓ | `7a926c67` | `7a926c67` | 1395 | expected_injection (by_task_id) |
| `paper` | `methylkit_unite` | `fritjoflammers-snakemake-methylanalysis-finish` | ✓ | ✓ | ✓ | `7a926c67` | `7a926c67` | 1395 | expected_injection (by_task_id) |
| `paper` | `methylkit_to_tibble` | `fritjoflammers-snakemake-methylanalysis-finish` | ✓ | ✓ | ✓ | `7a926c67` | `7a926c67` | 1395 | expected_injection (by_task_id) |
| `paper` | `longseq_deseq2_init` | `snakemake-workflows-rna-longseq-de-isoform` | ✓ | ✓ | ✓ | — | — | — | expected_fallback (no_paper_for_workflow) |
| `paper` | `longseq_deseq2_contrast` | `snakemake-workflows-rna-longseq-de-isoform` | ✓ | ✓ | ✓ | — | — | — | expected_fallback (no_paper_for_workflow) |
| `paper` | `snakepipes_merge_fc` | `maxplanck-ie-snakepipes-finish` | ✓ | ✓ | ✓ | `9283ae25` | `9283ae25` | 1521 | expected_injection (by_task_id) |
| `paper` | `snakepipes_merge_ct` | `maxplanck-ie-snakepipes-finish` | ✗ | ✗ | ✗ | — | `9283ae25` | — | expected_injection (by_task_id) |
| `paper` | `riya_limma` | `RiyaDua-cervical-cancer-snakemake-workflow` | ✗ | ✗ | ✓ | — | — | — | expected_fallback (no_paper_for_workflow) |
| `paper` | `chipseq_plot_macs_qc` | `snakemake-workflows-chipseq-finish` | ✗ | ✗ | ✓ | — | — | — | expected_fallback (no_paper_for_workflow) |
| `paper` | `chipseq_plot_homer_annot` | `snakemake-workflows-chipseq-finish` | ✗ | ✗ | ✓ | — | — | — | expected_fallback (no_paper_for_workflow) |
| `paper` | `snakepipes_scrna_merge_coutt` | `maxplanck-ie-snakepipes-finish` | ✗ | ✗ | ✗ | — | `9283ae25` | — | expected_injection (by_task_id) |
| `paper` | `snakepipes_scrna_qc` | `maxplanck-ie-snakepipes-finish` | ✗ | ✗ | ✗ | — | `9283ae25` | — | expected_injection (by_task_id) |
| `paper` | `spilterlize_filter_features` | `epigen-spilterlize_integrate-finish` | ✗ | ✗ | ✓ | — | — | — | expected_fallback (no_paper_for_workflow) |
| `paper` | `spilterlize_norm_voom` | `epigen-spilterlize_integrate-finish` | ✗ | ✗ | ✓ | — | — | — | expected_fallback (no_paper_for_workflow) |
| `paper` | `spilterlize_limma_rbe` | `epigen-spilterlize_integrate-finish` | ✗ | ✗ | ✓ | — | — | — | expected_fallback (no_paper_for_workflow) |
| `paper` | `spilterlize_norm_edger` | `epigen-spilterlize_integrate-finish` | ✗ | ✗ | ✓ | — | — | — | expected_fallback (no_paper_for_workflow) |
| `paper` | `dea_limma` | `epigen-dea_limma-finish` | ✗ | ✗ | ✗ | — | `7787402b` | — | expected_injection (by_task_id) |
| `paper` | `msisensor_merge` | `snakemake-workflows-msisensor-pro-finish` | ✗ | ✗ | ✗ | — | `efabb82f` | — | expected_injection (by_task_id) |
| `paper` | `methylkit_filt_norm` | `fritjoflammers-snakemake-methylanalysis-finish` | ✗ | ✗ | ✗ | — | `7a926c67` | — | expected_injection (by_task_id) |
| `paper` | `methylkit2tibble_split` | `fritjoflammers-snakemake-methylanalysis-finish` | ✗ | ✗ | ✗ | — | `7a926c67` | — | expected_injection (by_task_id) |
| `paper` | `methylkit_remove_snvs` | `fritjoflammers-snakemake-methylanalysis-finish` | ✗ | ✗ | ✗ | — | `7a926c67` | — | expected_injection (by_task_id) |
| `paper` | `phantompeak_correlation` | `snakemake-workflows-chipseq-finish` | ✗ | ✗ | ✓ | — | — | — | expected_fallback (no_paper_for_workflow) |
| `paper` | `nearest_gene` | `maxplanck-ie-snakepipes-finish` | ✗ | ✗ | ✗ | — | `9283ae25` | — | expected_injection (by_task_id) |
| `paper` | `chipseq_plot_frip_score` | `snakemake-workflows-chipseq-finish` | ✗ | ✗ | ✓ | — | — | — | expected_fallback (no_paper_for_workflow) |
| `paper` | `chipseq_plot_peaks_count_macs2` | `snakemake-workflows-chipseq-finish` | ✗ | ✗ | ✓ | — | — | — | expected_fallback (no_paper_for_workflow) |
| `paper` | `chipseq_plot_annotatepeaks_summary_homer` | `snakemake-workflows-chipseq-finish` | ✗ | ✗ | ✓ | — | — | — | expected_fallback (no_paper_for_workflow) |
| `paper` | `epibtn_rpkm` | `joncahn-epigeneticbutton-finish` | ✗ | ✗ | ✓ | — | — | — | expected_fallback (no_paper_for_workflow) |
| `paper` | `snakepipes_scrna_report` | `maxplanck-ie-snakepipes-finish` | ✗ | ✗ | ✗ | — | `9283ae25` | — | expected_injection (by_task_id) |
| `paper` | `clean_histoneHMM` | `maxplanck-ie-snakepipes-finish` | ✗ | ✗ | ✗ | — | `9283ae25` | — | expected_injection (by_task_id) |
| `pipeline` | `akinyi_deseq2` | `akinyi-onyango-rna_seq_pipeline-finish` | ✓ | ✓ | ✓ | `c92cfb05` | `c92cfb05` | 3076 | expected_injection (by_workflow_id) |
| `pipeline` | `star_deseq2_init` | `rna-seq-star-deseq2-finish` | ✓ | ✓ | ✓ | `e9a3bc65` | `e9a3bc65` | 4000 | expected_injection (by_workflow_id) |
| `pipeline` | `star_deseq2_contrast` | `rna-seq-star-deseq2-finish` | ✓ | ✓ | ✓ | `e9a3bc65` | `e9a3bc65` | 4000 | expected_injection (by_workflow_id) |
| `pipeline` | `methylkit_load` | `fritjoflammers-snakemake-methylanalysis-finish` | ✓ | ✓ | ✓ | `5df053f6` | `5df053f6` | 3835 | expected_injection (by_workflow_id) |
| `pipeline` | `methylkit_unite` | `fritjoflammers-snakemake-methylanalysis-finish` | ✓ | ✓ | ✓ | `5df053f6` | `5df053f6` | 3835 | expected_injection (by_workflow_id) |
| `pipeline` | `methylkit_to_tibble` | `fritjoflammers-snakemake-methylanalysis-finish` | ✓ | ✓ | ✓ | `5df053f6` | `5df053f6` | 3835 | expected_injection (by_workflow_id) |
| `pipeline` | `longseq_deseq2_init` | `snakemake-workflows-rna-longseq-de-isoform` | ✓ | ✓ | ✓ | `ed7db6c1` | `ed7db6c1` | 4000 | expected_injection (by_workflow_id) |
| `pipeline` | `longseq_deseq2_contrast` | `snakemake-workflows-rna-longseq-de-isoform` | ✓ | ✓ | ✓ | `ed7db6c1` | `ed7db6c1` | 4000 | expected_injection (by_workflow_id) |
| `pipeline` | `snakepipes_merge_fc` | `maxplanck-ie-snakepipes-finish` | ✓ | ✓ | ✓ | `9ee3a3d5` | `9ee3a3d5` | 3603 | expected_injection (by_workflow_id) |
| `pipeline` | `snakepipes_merge_ct` | `maxplanck-ie-snakepipes-finish` | ✓ | ✓ | ✓ | `9ee3a3d5` | `9ee3a3d5` | 3603 | expected_injection (by_workflow_id) |
| `pipeline` | `riya_limma` | `RiyaDua-cervical-cancer-snakemake-workflow` | ✓ | ✓ | ✓ | `a94e9936` | `a94e9936` | 3342 | expected_injection (by_workflow_id) |
| `pipeline` | `chipseq_plot_macs_qc` | `snakemake-workflows-chipseq-finish` | ✓ | ✓ | ✓ | `a232a8cb` | `a232a8cb` | 4000 | expected_injection (by_workflow_id) |
| `pipeline` | `chipseq_plot_homer_annot` | `snakemake-workflows-chipseq-finish` | ✓ | ✓ | ✓ | `a232a8cb` | `a232a8cb` | 4000 | expected_injection (by_workflow_id) |
| `pipeline` | `snakepipes_scrna_merge_coutt` | `maxplanck-ie-snakepipes-finish` | ✓ | ✓ | ✓ | `9ee3a3d5` | `9ee3a3d5` | 3603 | expected_injection (by_workflow_id) |
| `pipeline` | `snakepipes_scrna_qc` | `maxplanck-ie-snakepipes-finish` | ✓ | ✓ | ✓ | `9ee3a3d5` | `9ee3a3d5` | 3603 | expected_injection (by_workflow_id) |
| `pipeline` | `spilterlize_filter_features` | `epigen-spilterlize_integrate-finish` | ✓ | ✓ | ✓ | `89bb0a4e` | `89bb0a4e` | 4000 | expected_injection (by_workflow_id) |
| `pipeline` | `spilterlize_norm_voom` | `epigen-spilterlize_integrate-finish` | ✓ | ✓ | ✓ | `89bb0a4e` | `89bb0a4e` | 4000 | expected_injection (by_workflow_id) |
| `pipeline` | `spilterlize_limma_rbe` | `epigen-spilterlize_integrate-finish` | ✓ | ✓ | ✓ | `89bb0a4e` | `89bb0a4e` | 4000 | expected_injection (by_workflow_id) |
| `pipeline` | `spilterlize_norm_edger` | `epigen-spilterlize_integrate-finish` | ✓ | ✓ | ✓ | `89bb0a4e` | `89bb0a4e` | 4000 | expected_injection (by_workflow_id) |
| `pipeline` | `dea_limma` | `epigen-dea_limma-finish` | ✓ | ✓ | ✓ | `0479b9f6` | `0479b9f6` | 3421 | expected_injection (by_workflow_id) |
| `pipeline` | `msisensor_merge` | `snakemake-workflows-msisensor-pro-finish` | ✓ | ✓ | ✓ | `ace95648` | `ace95648` | 2598 | expected_injection (by_workflow_id) |
| `pipeline` | `methylkit_filt_norm` | `fritjoflammers-snakemake-methylanalysis-finish` | ✓ | ✓ | ✓ | `5df053f6` | `5df053f6` | 3835 | expected_injection (by_workflow_id) |
| `pipeline` | `methylkit2tibble_split` | `fritjoflammers-snakemake-methylanalysis-finish` | ✓ | ✓ | ✓ | `5df053f6` | `5df053f6` | 3835 | expected_injection (by_workflow_id) |
| `pipeline` | `methylkit_remove_snvs` | `fritjoflammers-snakemake-methylanalysis-finish` | ✓ | ✓ | ✓ | `5df053f6` | `5df053f6` | 3835 | expected_injection (by_workflow_id) |
| `pipeline` | `phantompeak_correlation` | `snakemake-workflows-chipseq-finish` | ✓ | ✓ | ✓ | `a232a8cb` | `a232a8cb` | 4000 | expected_injection (by_workflow_id) |
| `pipeline` | `nearest_gene` | `maxplanck-ie-snakepipes-finish` | ✓ | ✓ | ✓ | `9ee3a3d5` | `9ee3a3d5` | 3603 | expected_injection (by_workflow_id) |
| `pipeline` | `chipseq_plot_frip_score` | `snakemake-workflows-chipseq-finish` | ✓ | ✓ | ✓ | `a232a8cb` | `a232a8cb` | 4000 | expected_injection (by_workflow_id) |
| `pipeline` | `chipseq_plot_peaks_count_macs2` | `snakemake-workflows-chipseq-finish` | ✓ | ✓ | ✓ | `a232a8cb` | `a232a8cb` | 4000 | expected_injection (by_workflow_id) |
| `pipeline` | `chipseq_plot_annotatepeaks_summary_homer` | `snakemake-workflows-chipseq-finish` | ✓ | ✓ | ✓ | `a232a8cb` | `a232a8cb` | 4000 | expected_injection (by_workflow_id) |
| `pipeline` | `epibtn_rpkm` | `joncahn-epigeneticbutton-finish` | ✓ | ✓ | ✓ | `ed45355a` | `ed45355a` | 4000 | expected_injection (by_workflow_id) |
| `pipeline` | `snakepipes_scrna_report` | `maxplanck-ie-snakepipes-finish` | ✓ | ✓ | ✓ | `9ee3a3d5` | `9ee3a3d5` | 3603 | expected_injection (by_workflow_id) |
| `pipeline` | `clean_histoneHMM` | `maxplanck-ie-snakepipes-finish` | ✓ | ✓ | ✓ | `9ee3a3d5` | `9ee3a3d5` | 3603 | expected_injection (by_workflow_id) |
| `llm_plan` | `akinyi_deseq2` | `akinyi-onyango-rna_seq_pipeline-finish` | ✓ | ✓ | ✓ | `3a889efd` | `3a889efd` | 2418 | expected_injection (by_task_id) |
| `llm_plan` | `star_deseq2_init` | `rna-seq-star-deseq2-finish` | ✓ | ✓ | ✓ | `f169268d` | `f169268d` | 2217 | expected_injection (by_task_id) |
| `llm_plan` | `star_deseq2_contrast` | `rna-seq-star-deseq2-finish` | ✓ | ✓ | ✓ | `06cd791a` | `06cd791a` | 1987 | expected_injection (by_task_id) |
| `llm_plan` | `methylkit_load` | `fritjoflammers-snakemake-methylanalysis-finish` | ✓ | ✓ | ✓ | `db18cc3a` | `db18cc3a` | 1903 | expected_injection (by_task_id) |
| `llm_plan` | `methylkit_unite` | `fritjoflammers-snakemake-methylanalysis-finish` | ✓ | ✓ | ✓ | `dc8aedc7` | `dc8aedc7` | 2708 | expected_injection (by_task_id) |
| `llm_plan` | `methylkit_to_tibble` | `fritjoflammers-snakemake-methylanalysis-finish` | ✓ | ✓ | ✓ | `0da2c673` | `0da2c673` | 2267 | expected_injection (by_task_id) |
| `llm_plan` | `longseq_deseq2_init` | `snakemake-workflows-rna-longseq-de-isoform` | ✓ | ✓ | ✓ | `e2f5ba88` | `e2f5ba88` | 2070 | expected_injection (by_task_id) |
| `llm_plan` | `longseq_deseq2_contrast` | `snakemake-workflows-rna-longseq-de-isoform` | ✓ | ✓ | ✓ | `758e6aa4` | `758e6aa4` | 1710 | expected_injection (by_task_id) |
| `llm_plan` | `snakepipes_merge_fc` | `maxplanck-ie-snakepipes-finish` | ✓ | ✓ | ✓ | `2fcb76d2` | `2fcb76d2` | 1986 | expected_injection (by_task_id) |
| `llm_plan` | `snakepipes_merge_ct` | `maxplanck-ie-snakepipes-finish` | ✓ | ✓ | ✓ | `abdf20ba` | `abdf20ba` | 1972 | expected_injection (by_task_id) |
| `llm_plan` | `riya_limma` | `RiyaDua-cervical-cancer-snakemake-workflow` | ✓ | ✓ | ✓ | `ecb3f14e` | `ecb3f14e` | 2234 | expected_injection (by_task_id) |
| `llm_plan` | `chipseq_plot_macs_qc` | `snakemake-workflows-chipseq-finish` | ✓ | ✓ | ✓ | `e99d62c0` | `e99d62c0` | 3358 | expected_injection (by_task_id) |
| `llm_plan` | `chipseq_plot_homer_annot` | `snakemake-workflows-chipseq-finish` | ✓ | ✓ | ✓ | `39e816cf` | `39e816cf` | 2085 | expected_injection (by_task_id) |
| `llm_plan` | `snakepipes_scrna_merge_coutt` | `maxplanck-ie-snakepipes-finish` | ✓ | ✓ | ✓ | `d8264951` | `d8264951` | 2713 | expected_injection (by_task_id) |
| `llm_plan` | `snakepipes_scrna_qc` | `maxplanck-ie-snakepipes-finish` | ✓ | ✓ | ✓ | `5c816175` | `5c816175` | 2099 | expected_injection (by_task_id) |
| `llm_plan` | `spilterlize_filter_features` | `epigen-spilterlize_integrate-finish` | ✓ | ✓ | ✓ | `b1ed4c3f` | `b1ed4c3f` | 1668 | expected_injection (by_task_id) |
| `llm_plan` | `spilterlize_norm_voom` | `epigen-spilterlize_integrate-finish` | ✓ | ✓ | ✓ | `46cc6c82` | `46cc6c82` | 2061 | expected_injection (by_task_id) |
| `llm_plan` | `spilterlize_limma_rbe` | `epigen-spilterlize_integrate-finish` | ✓ | ✓ | ✓ | `8a921a28` | `8a921a28` | 1874 | expected_injection (by_task_id) |
| `llm_plan` | `spilterlize_norm_edger` | `epigen-spilterlize_integrate-finish` | ✓ | ✓ | ✓ | `8def7116` | `8def7116` | 1749 | expected_injection (by_task_id) |
| `llm_plan` | `dea_limma` | `epigen-dea_limma-finish` | ✓ | ✓ | ✓ | `8ad05d08` | `8ad05d08` | 2427 | expected_injection (by_task_id) |
| `llm_plan` | `msisensor_merge` | `snakemake-workflows-msisensor-pro-finish` | ✓ | ✓ | ✓ | `d01bde3c` | `d01bde3c` | 1976 | expected_injection (by_task_id) |
| `llm_plan` | `methylkit_filt_norm` | `fritjoflammers-snakemake-methylanalysis-finish` | ✓ | ✓ | ✓ | `aabfaf91` | `aabfaf91` | 2004 | expected_injection (by_task_id) |
| `llm_plan` | `methylkit2tibble_split` | `fritjoflammers-snakemake-methylanalysis-finish` | ✓ | ✓ | ✓ | `acdc6a27` | `acdc6a27` | 2063 | expected_injection (by_task_id) |
| `llm_plan` | `methylkit_remove_snvs` | `fritjoflammers-snakemake-methylanalysis-finish` | ✓ | ✓ | ✓ | `fdbb1940` | `fdbb1940` | 2097 | expected_injection (by_task_id) |
| `llm_plan` | `phantompeak_correlation` | `snakemake-workflows-chipseq-finish` | ✓ | ✓ | ✓ | `fb99c3d8` | `fb99c3d8` | 1593 | expected_injection (by_task_id) |
| `llm_plan` | `nearest_gene` | `maxplanck-ie-snakepipes-finish` | ✓ | ✓ | ✓ | `cad7e324` | `cad7e324` | 2483 | expected_injection (by_task_id) |
| `llm_plan` | `chipseq_plot_frip_score` | `snakemake-workflows-chipseq-finish` | ✓ | ✓ | ✓ | `78917f78` | `78917f78` | 1818 | expected_injection (by_task_id) |
| `llm_plan` | `chipseq_plot_peaks_count_macs2` | `snakemake-workflows-chipseq-finish` | ✓ | ✓ | ✓ | `c811981f` | `c811981f` | 2020 | expected_injection (by_task_id) |
| `llm_plan` | `chipseq_plot_annotatepeaks_summary_homer` | `snakemake-workflows-chipseq-finish` | ✓ | ✓ | ✓ | `71fe612a` | `71fe612a` | 1505 | expected_injection (by_task_id) |
| `llm_plan` | `epibtn_rpkm` | `joncahn-epigeneticbutton-finish` | ✓ | ✓ | ✓ | `05bc4daa` | `05bc4daa` | 2317 | expected_injection (by_task_id) |
| `llm_plan` | `snakepipes_scrna_report` | `maxplanck-ie-snakepipes-finish` | ✓ | ✓ | ✓ | `a474b76c` | `a474b76c` | 2199 | expected_injection (by_task_id) |
| `llm_plan` | `clean_histoneHMM` | `maxplanck-ie-snakepipes-finish` | ✓ | ✓ | ✓ | `17ae3ba1` | `17ae3ba1` | 2032 | expected_injection (by_task_id) |

**Audit result:** 23 row(s) failed; see ✗ marks above.
