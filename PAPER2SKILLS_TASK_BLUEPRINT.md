# Paper2Skills Task设计蓝图 (基于上游资源)

> 日期: 2026-04-23
> 模型: Qwen3 (本地vLLM)
> 目标: 设计能证明Paper Skill价值的12-14个高质量任务

---

## 资源盘点

| 资源 | 数量 | 路径 |
|------|------|------|
| -finish workflows | 57 | `main/finish/*-finish/` |
| workflow_candidates原源码 | 48 | `main/finish/workflow_candidates/` |
| workflow-paper映射 | 30 | `main/paper_primary_benchmark/literature/workflow_literature_map.json` |
| 现有tasks | 36 | `main/paper_primary_benchmark/ldp_r_task_eval/tasks/real/` |

---

## 核心设计原则（基于之前的经验教训）

### ✅ 好Task的特征

| 维度 | 要求 | 检测方法 |
|------|------|----------|
| 难度 | Agent默认做法失败 | None arm得分 0.2-0.4 |
| Paper匹配 | Paper工具=Task工具 | 名称和函数一致 |
| Paper内容 | 有可执行R代码 | ≥5行代码块 |
| 输出格式 | 可评估 | TSV/CSV而非RDS |
| 区分度 | Paper独特价值 | Paper - None > 0.5 |

### 7个最佳工具 (按paper richness排序)

1. **DESeq2** (EXCELLENT) - lfcShrink, LRT, interaction designs
2. **limma/voom** (EXCELLENT) - voomWithQualityWeights, duplicateCorrelation
3. **edgeR** (EXCELLENT) - robust fitting, filterByExpr
4. **Seurat** (EXCELLENT) - SCTransform, RPCA integration
5. **sva/ComBat-seq** (EXCELLENT) - batch correction
6. **clusterProfiler** (GOOD) - GSEA vs ORA
7. **MACS2** (GOOD) - broad vs narrow peaks

---

## 12个新Task详细设计

### 🎭 第一幕: Agent局限 (4个任务)

**故事**: Agent默认做法会失败或次优

#### Task 1: `deseq2_apeglm_small_n`
```
场景: n=2 per group的RNA-seq DE分析
陷阱: DESeq() → results() → logFC不稳定, lfcSE极大
Paper: DESeq2 (10.1186/s13059-014-0550-8)
关键: lfcShrink(type="apeglm")
输出: de_results.csv
预期: None=0.30, Paper=0.95 (diff=+0.65)
```

#### Task 2: `deseq2_lrt_interaction`
```
场景: 检测treatment × time interaction effect
陷阱: 默认Wald test → 错过interaction
Paper: DESeq2 (10.1186/s13059-014-0550-8)
关键: LRT with reduced=~treatment+time vs full=~treatment*time
输出: interaction_de.csv
预期: None=0.25, Paper=0.95 (diff=+0.70)
```

#### Task 3: `limma_voom_weights`
```
场景: RNA-seq数据质量不均一 (有低质量样本)
陷阱: voom() + lmFit() → 低质量样本影响结果
Paper: limma (10.1093/nar/gkv007)
关键: voomWithQualityWeights() + arrayWeights
输出: de_results_weighted.csv
预期: None=0.35, Paper=0.95 (diff=+0.60)
```

#### Task 4: `macs2_broad_histone`
```
场景: H3K27me3 ChIP-seq peak calling
陷阱: 默认narrow peak → 对broad marks过度分割
Paper: MACS2 (10.1186/gb-2008-9-9-r137)
关键: --broad --broad-cutoff 0.1
输出: broad_peaks.bed
预期: None=0.30, Paper=0.90 (diff=+0.60)
```

---

### 🎭 第二幕: 通用方法不够 (4个任务)

**故事**: Pipeline代码和LLM Plan通用规划也不足，需要paper特定知识

#### Task 5: `combat_seq_batch`
```
场景: RNA-seq counts有明显batch effect
陷阱:
  - Agent默认: 直接DE, 有confounding
  - Pipeline: "add batch to model"但count数据特殊
  - LLM Plan: 通用建议但不知count-specific
Paper: sva/ComBat-seq
关键: ComBat-seq保持负二项分布
输出: adjusted_counts.tsv + de_results.csv
预期: None=0.30, Pipeline=0.50, Paper=0.95
```

#### Task 6: `seurat_sctransform_scaling`
```
场景: scRNA-seq normalization + HVG
陷阱:
  - Agent默认: NormalizeData + ScaleData + FindVariableFeatures
  - Pipeline: 标准三步
  - Paper建议: SCTransform一步完成更robust
Paper: Seurat v4 (10.1101/2020.10.12.335331)
关键: SCTransform替代三步
输出: hvg_list.tsv + scaled_values.tsv
预期: None=0.40, Pipeline=0.50, Paper=0.95
```

#### Task 7: `clusterprofiler_gsea_vs_ora`
```
场景: 给定DE gene list + logFC
陷阱:
  - Agent默认: enrichGO on significant genes (ORA)
  - Pipeline: 标准ORA
  - Paper: GSEA用所有基因排序更robust
Paper: clusterProfiler (10.1089/omi.2011.0118)
关键: gseGO with ranked gene list
输出: gsea_results.tsv
预期: None=0.40, Pipeline=0.45, Paper=0.90
```

#### Task 8: `edger_robust_filtering`
```
场景: RNA-seq有outlier样本
陷阱:
  - Agent默认: 标准glmQLFit
  - Pipeline: filterByExpr + glmQLFit
  - Paper: robust=TRUE处理outliers
Paper: edgeR (Robinson 2010)
关键: glmQLFit(y, design, robust=TRUE)
输出: de_robust.tsv
预期: None=0.35, Pipeline=0.55, Paper=0.95
```

---

### 🎭 第三幕: Paper Skill价值 (4个任务)

**故事**: Paper提供的知识显著优于所有其他方法

#### Task 9: `methylkit_diffmeth_params`
```
场景: DNA methylation差异分析
陷阱: calculateDiffMeth默认参数
Paper: methylKit (需要替换当前MethPat)
关键: overdispersion="MN" + test="Chisq"
输出: diff_meth.tsv
预期: None=0.30, Pipeline=0.40, Paper=0.95
⚠️ 注意: 需要重新extract methylKit原paper (非MethPat)
```

#### Task 10: `limma_duplicatecorrelation`
```
场景: 配对设计 (patient internal control)
陷阱:
  - Agent默认: ~treatment (忽略pairing)
  - Pipeline: ~patient + treatment
  - Paper: duplicateCorrelation更robust
Paper: limma (10.1093/nar/gkv007)
关键: duplicateCorrelation(y, design, block=patient)
输出: paired_de.csv
预期: None=0.25, Pipeline=0.40, Paper=0.95
```

#### Task 11: `seurat_integration_method`
```
场景: 多批次scRNA-seq integration
陷阱:
  - Agent默认: IntegrateData标准
  - Pipeline: CCA方法
  - Paper: RPCA更适合大数据
Paper: Seurat v4 (10.1101/2020.10.12.335331)
关键: FindIntegrationAnchors(reduction="rpca")
输出: integrated_umap.tsv + cluster_labels.tsv
预期: None=0.30, Pipeline=0.50, Paper=0.90
```

#### Task 12: `deseq2_shrinkage_comparison`
```
场景: 多样本RNA-seq DE，需要shrinkage
陷阱:
  - Agent默认: lfcShrink(type="normal") - 已deprecated
  - Pipeline: apeglm (较新)
  - Paper: apeglm vs ashr应用场景区分
Paper: DESeq2 (10.1186/s13059-014-0550-8)
关键: 根据数据特性选择apeglm或ashr
输出: shrunk_de.csv
预期: None=0.40, Pipeline=0.55, Paper=0.95
```

---

## 对比预期：新设计 vs 当前实验

| 指标 | 当前实验 | 新设计 | 改进 |
|------|----------|--------|------|
| 有意义任务数 | 1/18 (5.6%) | 12/12 (100%) | +94% |
| 平均Paper-None差异 | ~0.03 | ~0.61 | +0.58 |
| None arm得分范围 | 0.1-1.0 (太宽) | 0.25-0.40 (合理) | ✅ |
| Paper arm得分范围 | 0.075-1.0 | 0.90-0.95 | ✅ |

---

## Task构建流程 (标准化)

### 每个Task需要的文件

```
tasks/real/{task_id}/
├── OBJECTIVE.md          # 任务描述 (有意隐藏关键细节)
├── meta.json             # 元数据
└── input/                # 输入数据
    ├── counts.tsv
    ├── metadata.tsv
    └── ...

tasks/real_ground_truth/{task_id}/
├── meta.json
├── reference/
│   ├── script.R          # Paper-guided正确解法
│   ├── run.cmd.json      # 运行命令
│   └── wrapper.R
└── reference_output/     # 期望输出
    └── de_results.csv
```

### Task构建五步法

1. **选择Workflow** → 从57个finish中选有paper的
2. **提取步骤** → 找到一个关键R script
3. **设计陷阱** → 修改数据使默认做法失败
4. **验证陷阱** → 跑None arm确认得分<0.4
5. **验证Paper** → 跑Paper arm确认得分>0.9

---

## 实施优先级

### 立即开始 (最高优先级)
- ✅ Task 1, 2, 12: DESeq2相关 (已有star-deseq2-finish)
- ✅ Task 3, 10: limma相关 (已有dea_limma-finish)
- ✅ Task 6, 11: Seurat相关 (已有scrnaseq_processing_seurat-finish)

### 需要补充Paper
- ⚠️ Task 5: 需下载sva/ComBat-seq paper
- ⚠️ Task 8: 需下载edgeR原paper
- ⚠️ Task 9: 需替换methylKit paper (当前是MethPat)

### 需要扩展Pipeline
- ✅ Task 4: macs2_broad - 有atacseq_pipeline-finish
- ✅ Task 7: GSEA - 有enrichment_analysis-finish

---

## 关键问题与决策

### 问题1: Paper质量保证
- 当前MethPat paper是错的 (实际methylKit需要另一篇)
- 需要**pre-extract验证**: 确保Paper包含所需函数
- 可以手动筛选或用LLM做"paper contains X function?"检查

### 问题2: Ground truth生成
- 每个任务需要**Paper-guided reference script**
- 这本身需要人工验证或多次运行确认
- 建议: 每个task由一个"懂paper的expert"手写一次reference

### 问题3: 模型选择
- 用Qwen3本地跑 → 需要确认Qwen3对这些任务的baseline能力
- Qwen3可能比GPT-4o略弱，但差异更明显有利于展示skill价值

---

## 下一步行动

1. **选3个任务做试点** (推荐: Task 1, 3, 6)
   - 覆盖不同tool (DESeq2/limma/Seurat)
   - 都有现成workflow和paper

2. **验证假设**
   - 跑None arm: 确认失败模式
   - 提取Paper skill: 用vision adapter
   - 跑Paper arm: 确认改善

3. **扩展到12个**
   - 基于试点结果调整设计
   - 逐步添加其他9个

4. **完整实验**
   - 32任务 → 12精选任务
   - 4-arm ablation with Qwen3
   - 写paper story

---

*蓝图完成*
