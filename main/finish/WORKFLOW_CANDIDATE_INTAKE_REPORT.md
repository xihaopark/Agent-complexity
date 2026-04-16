# Workflow Candidate Intake Report

更新日期: 2026-04-10

目的:
- 对本地 `workflow_candidates/` 中已拉取的候选仓库做结构扫描。
- 识别哪些仓库最接近当前 `finish` benchmark 的接入模式。
- 当前不做难度分级，不判断是否有分支，只看“是否像一个可拆步、多步骤 workflow”。

本地候选目录:
- `finish/workflow_candidates/`

扫描输出:
- `finish/workflow_candidates/_scan_summary.json`

## 扫描指标

每个仓库按以下结构特征打分:
- 是否存在 `Snakefile` 或 `workflow/Snakefile`
- 是否存在 `workflow/` 目录
- 是否存在 `workflow/rules/` 或 `rules/`
- 是否存在 `scripts/`
- 是否存在 `config/` 或类似配置目录
- 是否存在样本表 / 输入表，如 `samples.tsv`、`samples.csv`、`units.tsv`
- 是否有足够数量的 `*.smk`
- 是否包含较明显的 R 脚本资产

## 总体结果

- 候选总数: 53
- 已拉取到本地目录的仓库源: 47
- 完成结构扫描的本地目录: 47

## 第一梯队: 最像当前 `finish` 接入模式

这些仓库最接近你们现有的 `finish` 结构，优先考虑转接:

| 仓库 | 结构特征 | 备注 |
|---|---|---|
| `snakemake-workflows__rna-seq-kallisto-sleuth` | `workflow/Snakefile` + `workflow/rules/` + `config/` + samplesheet + 大量 `*.smk` + 大量 R 脚本 | 与现有 benchmark 高度同构 |
| `snakemake-workflows__chipseq` | `workflow/Snakefile` + `workflow/rules/` + `config/` + samplesheet | 很适合拆 retained steps |
| `snakemake-workflows__rna-longseq-de-isoform` | 结构完整，规则数多，含 R 分析部分 | 可作为长读长方向扩展 |
| `snakemake-workflows__rna-seq-star-deseq2` | 结构完整，已是现有同类参照 | 可复用现有 finish 改造逻辑 |
| `epigen__scrnaseq_processing_seurat` | `workflow/Snakefile` + `workflow/rules/` + 多个 R 脚本 | 很适合单细胞方向扩展 |
| `epigen__dea_seurat` | `workflow/` + `rules/` + Seurat DEA | 适合作为下游分析 workflow |
| `epigen__dea_limma` | `workflow/` + `rules/` + limma | 适合作为表达/可及性/binding downstream 分析 |
| `epigen__mixscape_seurat` | `workflow/` + `rules/` + R / Seurat | 单细胞扰动方向候选 |
| `epigen__rnaseq_pipeline` | 结构完整，接近标准 Snakemake 项目 | bulk RNA-seq 候选 |
| `epigen__atacseq_pipeline` | 结构完整，ATAC-seq 主线明确 | 多步骤且有清晰模块 |

## 第二梯队: 结构也强，但 R 核心或接入方式略有差异

| 仓库 | 结构特征 | 备注 |
|---|---|---|
| `epigen__unsupervised_analysis` | 结构完整，偏通用分析 | 可作为下游模块型 workflow |
| `epigen__spilterlize_integrate` | 结构完整，偏 preprocessing / integration | 适合做中间流程任务 |
| `epigen__enrichment_analysis` | 结构完整，偏 enrichment | 更像分析后段 workflow |
| `snakemake-workflows__star-arriba-fusion-calling` | 结构完整，RNAseq + fusion | 可作为 RNAseq 变体 |
| `snakemake-workflows__single-cell-drop-seq` | 多 `*.smk`、R 脚本多，但目录布局不完全标准 | 仍然值得保留 |
| `chandanbfx__scRNA-seq-Seurat-Workflow` | 有 Snakemake 与多步 Seurat 分析 | 目录布局比官方仓库松散 |
| `mckellardw__slide_snake` | 很多 `*.smk`，空间转录组方向 | 结构复杂但不完全贴合标准模板 |
| `gustaveroussy__sopa` | 有 workflow 结构，但配置方式较特殊 | 空间组学方向候选 |
| `jfnavarro__st_pipeline` | 空间转录组 pipeline | 需要进一步确认入口方式 |
| `fritjoflammers__snakemake-methylanalysis` | 规则与 R 脚本都比较多 | 甲基化方向候选 |

## 第三梯队: 已拉取，但当前不建议优先接入

这些仓库虽然是候选，但从当前扫描结果看，不是优先改造成 `finish` 的目标:

| 仓库 | 原因 |
|---|---|
| `RiyaDua__cervical-cancer-snakemake-workflow` | 更像小型项目化 workflow，结构较轻 |
| `Akinyi-Onyango__rna_seq_pipeline` | 结构过轻，规则拆分不足 |
| `dwheelerau__snakemake-rnaseq-counts` | 更偏单用途 pipeline |
| `saidmlonji__rnaseq_pipeline` | R/Bash pipeline，但不太像标准 Snakemake 多规则仓库 |
| `gammon-bio__rnaseq_pipeline` | 结构较轻 |
| `mohammedemamkhattabunipd__ATACseq` | 更像 R 分析项目，不像 Snakemake workflow 仓库 |
| `snakemake-workflows__oncology` | 当前仓库内容很少，未成形 |

## systemPipeRdata 的特殊情况

`tgirke__systemPipeRdata` 已拉到本地，但它不是 Snakemake 风格仓库，而是一个 workflow template 源仓库。

它的价值在于:
- 提供多个 R workflow template
- 适合后续手动提炼成你们自己的 `finish` 风格多步骤任务

它和 Snakemake 官方 workflow 不同:
- 不适合作为“直接照搬进 `finish`”的第一优先级
- 更适合作为后续补充 R-native workflow family 的来源

## 当前建议的接入顺序

如果下一步要开始真正做 `finish` 化改造，我建议先从下面这一批开始:

1. `snakemake-workflows__chipseq`
2. `snakemake-workflows__rna-longseq-de-isoform`
3. `epigen__scrnaseq_processing_seurat`
4. `epigen__dea_seurat`
5. `epigen__dea_limma`
6. `epigen__rnaseq_pipeline`
7. `epigen__atacseq_pipeline`
8. `epigen__mixscape_seurat`
9. `fritjoflammers__snakemake-methylanalysis`
10. `mckellardw__slide_snake`

说明:
- `star` 和 `kallisto` 你们已经有了对应 finish 化版本，因此上面优先列的是新增价值更高的方向。
- 第一批最好优先选择与现有结构最同构、且分析族差异足够大的仓库。

## 下一步建议

- 对第一梯队和第二梯队做更细致的入口确认:
- 识别主 `Snakefile`
- 识别配置文件
- 识别最自然的 retained steps
- 识别最小可运行测试数据

- 然后直接产出一份:
- `WORKFLOW_FINISH_CONVERSION_PLAN.md`

内容包括:
- 仓库名
- 建议保留步骤
- 初始接入优先级
- 转为 `finish` 所需的最小改造量
