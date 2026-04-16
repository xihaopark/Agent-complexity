# Benchmark Run Plan

更新日期: 2026-04-10

- 计划工作流数量: 12
- 每个家族上限: 3
- 是否包含 large 集合: False

选择原则:
- 优先选择 `release_core` 中 steps 适中的 workflow。
- 尽量覆盖 `rna` / `single-cell` / `epigenomics` / `variant` / `spatial` / `other` 各家族。
- 每个家族默认不超过 3 个，避免首轮实验过于偏向单一领域。

## 选中 workflow

| Workflow | Steps | Family | 类型 |
|---|---:|---|---|
| `tgirke-systempiperdata-rnaseq-finish` | 21 | rna | manual-special |
| `dwheelerau-snakemake-rnaseq-counts-finish` | 10 | rna | auto |
| `rna-seq-kallisto-sleuth-finish` | 9 | rna | auto |
| `cite-seq-alevin-fry-seurat-finish` | 18 | single-cell | auto |
| `tgirke-systempiperdata-spscrna-finish` | 18 | single-cell | manual-special |
| `epigen-scrnaseq_processing_seurat-finish` | 15 | single-cell | auto |
| `epigen-enrichment_analysis-finish` | 16 | epigenomics | auto |
| `tgirke-systempiperdata-chipseq-finish` | 21 | epigenomics | manual-special |
| `epigen-spilterlize_integrate-finish` | 14 | epigenomics | auto |
| `dna-seq-short-read-circle-map-finish` | 21 | variant | auto |
| `microsatellite-instability-detection-with-msisensor-pro-finish` | 10 | variant | auto |
| `tgirke-systempiperdata-varseq-finish` | 35 | variant | manual-special |
