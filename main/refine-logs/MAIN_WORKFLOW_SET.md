# Main Workflow Set (v2)

更新日期: 2026-04-14

## 选择目标

- 作为论文主实验集的第一版核心 workflow 集
- 用于：
  - 多 agent baseline benchmark
  - failure taxonomy 分析
  - targeted adjustment 前后同集复跑
- 总量控制在约 30 个，兼顾代表性、家族覆盖与正式 benchmark 的统计稳定性

## 选择原则

- 优先从 `finish/BENCHMARK_RELEASE_CANDIDATES.json` 的 `release_core` 中选取
- 只选 `status=passed` 的 workflow
- 尽量覆盖主要 bio workflow 家族：
  - `rna`
  - `single-cell`
  - `epigenomics`
  - `variant`
  - `spatial`
  - `other`
- 同时覆盖 small / medium 难度梯度
- 避免主实验集过多包含：
  - 2-4 step 的过小 sanity workflows
  - >40 step 的大型 workflow
  - 当前明显被 infra/resource failure 主导的 workflow

## 推荐主实验集（30）

| Workflow | Steps | Family | 类型 | 入选理由 |
|---|---:|---|---|---|
| `rna-seq-kallisto-sleuth-finish` | 22 | rna | auto | RNA 家族稳定代表，已有正式实验基础 |
| `star-arriba-fusion-calling-finish` | 8 | rna | auto | RNA 分支任务，与常规 differential expression 不同 |
| `tgirke-systempiperdata-rnaseq-finish` | 21 | rna | manual-special | manual-special RNA 代表，步骤更完整 |
| `rna-seq-star-deseq2-finish` | 25 | rna | auto | RNA 主干 benchmark，已有对比结果基础 |
| `epigen-dea_seurat-finish` | 10 | single-cell | auto | single-cell 轻量分析型 workflow |
| `epigen-scrnaseq_processing_seurat-finish` | 15 | single-cell | auto | single-cell 处理中等复杂度代表 |
| `cite-seq-alevin-fry-seurat-finish` | 18 | single-cell | auto | 多模态/更复杂 single-cell 场景 |
| `single-cell-rna-seq-finish` | 22 | single-cell | auto | single-cell 中型 workflow 主代表 |
| `epigen-fetch_ngs-finish` | 7 | epigenomics | auto | epigenomics 轻量入口型 workflow |
| `epigen-dea_limma-finish` | 12 | epigenomics | auto | 统计分析型 epigenomics workflow |
| `epigen-enrichment_analysis-finish` | 16 | epigenomics | auto | 功能富集分析，和 mapping 类任务不同 |
| `tgirke-systempiperdata-chipseq-finish` | 21 | epigenomics | manual-special | ChIP-seq manual-special 代表 |
| `fritjoflammers-snakemake-methylanalysis-finish` | 22 | epigenomics | auto | methylation 方向代表，补足家族多样性 |
| `microsatellite-instability-detection-with-msisensor-pro-finish` | 10 | variant | auto | variant 轻量代表 |
| `dna-seq-short-read-circle-map-finish` | 21 | variant | auto | variant 中型代表 |
| `tgirke-systempiperdata-varseq-finish` | 35 | variant | manual-special | variant 家族高复杂度代表 |
| `gustaveroussy-sopa-finish` | 20 | spatial | auto | 当前最适合作为 spatial 主代表，规模适中 |
| `lwang-genomics-ngs_pipeline_sn-rna_seq-finish` | 9 | other | manual-special | 作为 other/manual-special 的轻量代表 |
| `tgirke-systempiperdata-riboseq-finish` | 32 | other | manual-special | riboseq 类型独特，补足非标准 RNA 任务 |
| `cyrcular-calling-finish` | 34 | other | auto | 较难的 other 家族代表，提供 stress case |
| `epigen-300bcg-atacseq_pipeline-finish` | 10 | epigenomics | manual-special | ATAC 方向补充，增强 epigenomics 覆盖 |
| `lwang-genomics-ngs_pipeline_sn-chip_seq-finish` | 8 | epigenomics | manual-special | 轻量 manual-special ChIP workflow |
| `cellranger-multi-finish` | 14 | single-cell | auto | single-cell 中等规模补充，增加 pipeline 多样性 |
| `tgirke-systempiperdata-spscrna-finish` | 18 | single-cell | manual-special | single-cell manual-special 代表 |
| `epigen-atacseq_pipeline-finish` | 26 | epigenomics | auto | epigenomics 中型 benchmark 代表 |
| `epigen-rnaseq_pipeline-finish` | 26 | epigenomics | auto | 家族内跨任务类型补充 |
| `akinyi-onyango-rna_seq_pipeline-finish` | 8 | other | auto | other 家族轻量 auto 代表 |
| `maxplanck-ie-snakepipes-finish` | 39 | other | auto | 较大但仍可控的 other workflow，提供高复杂度样本 |
| `epigen-spilterlize_integrate-finish` | 14 | epigenomics | auto | 数据整合型任务，补足分析侧流程 |
| `read-alignment-pangenome-finish` | 38 | other | auto | 复杂 alignment / pangenome 场景补充 |

## 家族覆盖统计

| Family | Count |
|---|---:|
| rna | 4 |
| single-cell | 6 |
| epigenomics | 10 |
| variant | 3 |
| spatial | 1 |
| other | 6 |
| Total | 30 |

## Smoke Workflow Set（测试实验，3 个）

在正式跑 30 个之前，先固定 3 个 workflow 做 smoke benchmark，目标是验证：

- 真实框架 agent 是否能稳定启动
- 共享 env / conda cache 是否正常工作
- workflow 结果 JSON / llm trace / metrics 是否稳定落盘
- 当前 infra 是否还存在前期基础问题（env provisioning、权限、缓存、磁盘）

| Workflow | Steps | Family | 选择原因 |
|---|---:|---|---|
| `rna-seq-star-deseq2-finish` | 25 | rna | 已验证可跑，是 RNA 主干 smoke 候选 |
| `epigen-scrnaseq_processing_seurat-finish` | 15 | single-cell | 覆盖 Seurat / single-cell 场景与 R 生态依赖 |
| `dna-seq-varlociraptor-finish` | 18 | variant | 已有稳定成功记录，适合作为 variant smoke 候选 |

## 为什么不是其它候选

### 暂不纳入（过小 / 更适合作 sanity）

- `dwheelerau-snakemake-rnaseq-counts-finish`
- `gersteinlab-astro-finish`
- `riyadua-cervical-cancer-snakemake-workflow-finish`
- `saidmlonji-rnaseq_pipeline-finish`
- `gammon-bio-rnaseq_pipeline-finish`
- `cellranger-count-finish`
- `sumone-compbio-dge-analysis-using-snakemake-r-finish`

原因：
- `dwheelerau-snakemake-rnaseq-counts-finish` 在 smoke 中暴露出 `project_setup` 步骤的 Snakefile 命令生成为 `None` 的协议问题，不宜作为当前主实验集样本；
- 其余 workflow step 数过小，更适合 smoke / sanity，而不是主实验集核心支撑证据。

### 暂不纳入（当前仍未进入主实验集）

- `lwang-genomics-ngs_pipeline_sn-atac_seq-finish`
- `cellranger-count-finish`
- `epigen-mixscape_seurat-finish`
- `epigen-genome_tracks-finish`
- `semenko-serpent-methylation-pipeline-finish`

原因：
- 当前主实验集已覆盖对应家族与难度区间，纳入后边际信息增益相对较低。

### 暂不纳入（更适合扩展阶段）

- `epigen-unsupervised_analysis-finish`

原因：
- 这些 workflow 更适合作为主实验集通过后的第二轮扩展 benchmark / robustness set。

### 暂不纳入（当前不适合作主实验集）

- `snakemake-workflow-template-finish`
- `zarp-finish`

原因：
- 当前更适合作为 failure case / infra sensitivity case，而不是论文主实验集样本。

## 使用建议

- 先跑 Smoke Workflow Set（3 个）
- smoke 结果符合预期后，再跑 30 个主实验集 baseline benchmark（所有 5 agents）
- 然后固定同一 30 个 workflow 做 before / after targeted adjustment 对比
- 若闭环验证成立，再从 `release_large` 中继续扩展

## 备选替换位

如果导师希望更强调某个方向，可优先替换：

- 强化 spatial:
  - 用 `mckellardw-slide_snake-finish` 替换一个 `other` workflow（但成本明显增加）
- 强化 epigenomics:
  - 用 `epigen-atacseq_pipeline-finish` 或 `epigen-rnaseq_pipeline-finish` 替换 `epigen-fetch_ngs-finish`
- 强化 single-cell manual-special:
  - 用 `tgirke-systempiperdata-spscrna-finish` 替换 `epigen-dea_seurat-finish`
