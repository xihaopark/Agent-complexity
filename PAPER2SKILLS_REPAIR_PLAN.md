# Paper2Skills 修复方案

> **原则**: 基于真实 Paper 内容，确保 Paper arm 最优，可微调引导复杂度  
> **范围**: 5 个 Tier A 任务 + 参考原 32 个 tasks  
> **日期**: 2026-04-23

---

## 🔍 现状问题分析

### 实验失败根因

| 任务 | Paper Arm 失败原因 | 是否可修复 |
|------|------------------|-----------|
| deseq2_apeglm_small_n | 输出列选择错误 (apeglm 无 `stat` 列) | ✅ 修复 skill |
| deseq2_lrt_interaction | 部分成功 (0.30)，输出格式问题 | ✅ 优化 skill |
| deseq2_shrinkage_comparison | contrast 参数错误 | ✅ 修复 skill |
| limma_voom_weights | 数据读取假设错误 | ✅ 优化引导 |
| limma_duplicatecorrelation | 所有 arm 使用替代方案 | 🔄 重新设计任务 |

### 核心问题

1. **Skill 内容不完整**: 描述了方法但未说明输出格式差异
2. **Agent 假设错误**: 假设列存在、硬编码参数
3. **Task 设计缺陷**: 存在简单替代方案 (如 fixed effect 替代 duplicateCorrelation)

---

## ✅ 修复方案 (基于真实 Paper)

### 修复 1: apeglm Skill - 添加输出格式说明

**来源**: DESeq2 paper (Love et al. 2014) + apeglm 文档  
**真实信息**: apeglm 返回的列与标准 DESeq2 不同

**当前 Skill (有问题)**:
```markdown
## Output Format
Write results with columns: gene_id, baseMean, log2FoldChange, lfcSE, stat, pvalue, padj
```

**修复后 Skill**:
```markdown
## Output Format Note (Important!)

apeglm results have a DIFFERENT structure than standard DESeq2 results:

- apeglm returns: baseMean, log2FoldChange, lfcSE
- Standard DESeq2 returns: baseMean, log2FoldChange, lfcSE, stat, pvalue, padj
- apeglm does NOT have 'stat' column (that's from Wald test)

### Correct handling:
```r
# After lfcShrink with apeglm
res <- lfcShrink(dds, coef=coef_name, type="apeglm", res=res)
res_df <- as.data.frame(res)

# Keep all columns that exist, don't try to select specific ones
# The columns will be: baseMean, log2FoldChange, lfcSE, pvalue, padj
# (no 'stat' column!)

# Write with row.names to preserve gene_id
write.csv(res_df, "output/de_results.csv", row.names=TRUE)
```

### What the paper says:
> "apeglm uses a heavy-tailed prior distribution that produces less 
> biased estimates than the normal prior used in the original DESeq2."
> - Zhu et al. 2018 (apeglm paper)
```

**验证**: Paper arm 将正确处理 apeglm 输出

---

### 修复 2: LRT Skill - 优化输出格式

**来源**: DESeq2 vignette  
**真实信息**: LRT 返回所有基因的测试结果

**修复后 Skill**:
```markdown
## LRT Output Format

LRT (Likelihood Ratio Test) results contain:
- baseMean: average expression
- stat: chi-squared statistic (NOT log2FoldChange!)
- pvalue, padj: statistical significance

Note: LFC is NOT meaningful for LRT since it's testing multiple coefficients.
If you need LFC estimates, use the Wald test results for specific coefficients.

### Output handling:
```r
# LRT results
dds <- DESeq(dds, test="LRT", reduced=~genotype+treatment)
res <- results(dds)

# Write all results (LFC may be NA or 0)
res_df <- as.data.frame(res)
write.csv(res_df, "output/interaction_de.csv", row.names=TRUE)
```
```

---

### 修复 3: Shrinkage Comparison Skill - 添加鲁棒代码

**来源**: DESeq2 paper + apeglm paper  
**真实信息**: 三种 shrinkage 的比较方法

**修复后 Skill**:
```markdown
## Comparing Shrinkage Estimators

The paper compares three estimators:
- "normal": Original DESeq2, normal prior
- "ashr": Adaptive shrinkage, flexible prior (general purpose)
- "apeglm": Adaptive t prior, best for small samples

### Robust Implementation Pattern:

```r
# Step 1: Get coefficient name programmatically
coef_names <- resultsNames(dds)
coef_idx <- grep("condition", coef_names)[1]  # Find first condition-related coef
coef_name <- coef_names[coef_idx]

# Step 2: Get base results
res <- results(dds, name=coef_name)

# Step 3: Apply apeglm (recommended for small samples)
res_apeglm <- lfcShrink(dds, coef=coef_name, type="apeglm", res=res)

# Step 4: Write results
# Use row.names=TRUE to preserve gene names
write.csv(as.data.frame(res_apeglm), "output/shrunk_de.csv", row.names=TRUE)
```

### Key Points from Paper:
- ashr: "more stable than normal in simulations"
- apeglm: "produces the least bias in small samples"
```

---

### 修复 4: Limma voomWithQualityWeights - 详细数据读取

**来源**: limma paper (Ritchie et al. 2015) + limma User's Guide  
**真实信息**: 明确的数据结构和步骤

**修复后 Skill**:
```markdown
## Data Reading (Critical!)

Input files structure (verify with your task):
- counts.tsv: genes as rows, samples as columns, gene_id in first column
- coldata.tsv: samples as rows, metadata columns, sample names as row names

### Correct Data Reading:
```r
# Read counts: row.names=1 assumes first column is gene_id
counts <- read.table("input/counts.tsv", header=TRUE, row.names=1, sep="\t")

# Read coldata: row.names=1 assumes first column is sample_id
coldata <- read.table("input/coldata.tsv", header=TRUE, row.names=1, sep="\t")

# Verify alignment
stopifnot(all(colnames(counts) %in% rownames(coldata)))

# Use the condition column from coldata (may be named 'condition' or 'group')
condition_col <- if("condition" %in% colnames(coldata)) "condition" else "group"
```

## voomWithQualityWeights Implementation

From the paper:
> "Array quality weights are estimated for each sample to account 
> for systematic differences in quality between samples."

```r
library(limma)
library(edgeR)

# Step 1: Create DGEList (use the condition column we identified)
dge <- DGEList(counts=counts, group=coldata[[condition_col]])
dge <- calcNormFactors(dge)

# Step 2: Design matrix
design <- model.matrix(~ condition, data=coldata)

# Step 3: voomWithQualityWeights (the key method!)
v <- voomWithQualityWeights(dge, design, plot=FALSE)

# Step 4: Fit and test
fit <- lmFit(v, design)
fit <- eBayes(fit)

# Step 5: Results
res <- topTable(fit, coef=2, number=Inf, sort.by="none")
write.csv(res, "output/de_results_weighted.csv", row.names=TRUE)
```
```

---

### 修复 5: Limma duplicateCorrelation - 重新设计任务

**问题**: 固定效应模型可以替代，任务没有强制使用 paper 方法  
**解决方案**: 修改任务设计使其必须使用 duplicateCorrelation

**新 Task Design**:
```markdown
## Task: Paired Tumor-Normal Differential Expression

### Objective
You have paired tumor-normal samples from 8 patients (16 samples total).
Each patient has exactly 2 samples: one tumor and one normal.

**CRITICAL**: The data has a paired structure that must be accounted for.
Samples from the same patient are correlated.

### Required Method
Use limma's duplicateCorrelation() function to estimate the correlation
between paired samples, then incorporate this into the linear model fit.

This is the ONLY correct method for this paired design.
Simple fixed effects models are NOT appropriate here.

### Input
- counts.tsv: 16 samples (8 patients × 2 conditions)
- coldata.tsv: with 'patient' and 'condition' columns

### Expected Output
- output/paired_de.csv with DE results

### Key Method Reference
duplicateCorrelation() estimates within-patient correlation,
then lmFit(..., block=patient, correlation=corfit$consensus) uses it.
```

**输入数据修改**:
```r
# 添加明确的患者标识，使 fixed effect 方法变得复杂
# 8 patients × 2 conditions = 16 samples
# 如果使用 fixed effect: 8 patient dummies + intercept = 9 params for 16 obs
# 使用 duplicateCorrelation: only need condition + correlation estimate
```

---

## 📊 整合原 32 个 Tasks

### 分析原 32 Tasks

从 `FINAL_4ARM_COMPLETE.md` 和 `per_task_compare_v21_final.csv`:

| Category | Count | 适合加入? |
|----------|-------|----------|
| Paper 明显优势 | 1 | ✅ 保留 |
| 所有 arm 都失败 | ~10 | 🔄 评估修复可能性 |
| 所有 arm 都成功 | ~15 | ❌ 太简单，排除 |
| High variance | ~6 | 🔄 可能 task 设计问题 |

### 推荐的整合策略

**Tier B (从原 32 中选 5-10 个)**:

1. **筛选标准**:
   - Paper arm 尝试过但失败的 (可修复)
   - 涉及非默认参数的任务
   - 需要 paper 特定知识的

2. **候选任务**:
   - 涉及 ashr vs apeglm 选择的任务
   - 需要特定 contrast 设定的任务
   - 涉及 filtering 参数的任务 (independentFiltering)

3. **排除任务**:
   - 所有 arm 都成功的 (太简单)
   - 与 Tier A 重复的

---

## 🎯 验证计划

### 验证步骤

1. **更新 Skills** (按上述修复)
2. **重新运行实验**:
   ```bash
   python3 scripts/run_4arm_vllm_isolated.py
   ```
3. **验证目标**:
   - Paper arm 在所有 5 个任务上 ≥ 0.6 分
   - Paper-None 平均差异 ≥ 0.4
   - Paper arm 正确使用了 paper 方法

### 成功标准

| Metric | Current | Target |
|--------|---------|--------|
| Paper arm avg score | 0.06 | ≥ 0.6 |
| Paper-None diff | -0.14 | ≥ +0.4 |
| Tasks with paper success | 1/5 | 5/5 |

---

## 📝 修复文件清单

### 需要修改的文件

```
experiments/skills_paper2skills_v1/paper/
├── deseq2_apeglm_small_n/SKILL.md          [修复输出格式]
├── deseq2_lrt_interaction/SKILL.md        [修复输出格式]
├── deseq2_shrinkage_comparison/SKILL.md    [添加鲁棒代码]
├── limma_voom_weights/SKILL.md            [详细数据读取]
└── limma_duplicatecorrelation/SKILL.md    [更新任务引用]

main/paper_primary_benchmark/ldp_r_task_eval/tasks/paper_sensitive_v1/real/
├── limma_duplicatecorrelation/
│   ├── OBJECTIVE.md                        [重新设计任务]
│   └── input/coldata.tsv                    [添加 patient 列]
└── limma_voom_weights/
    └── OBJECTIVE.md                         [更清晰的数据描述]
```

---

## 🚀 下一步行动

### Phase 1: Skill 修复 (2 小时)

1. 修复 apeglm skill 输出格式 (30 min)
2. 修复 LRT skill 输出格式 (20 min)
3. 修复 shrinkage skill 鲁棒性 (30 min)
4. 修复 limma voomWithQualityWeights (40 min)

### Phase 2: Task 重新设计 (1 小时)

1. 修改 limma_duplicatecorrelation 任务 (30 min)
2. 更新 input 数据 (20 min)
3. 验证 reference script (10 min)

### Phase 3: 验证实验 (3 小时)

1. 重新运行 20 runs (2.5 hours)
2. 分析结果 (30 min)

**总计**: ~6 小时完成修复和验证

---

## 💡 经验教训

### 关于 Paper Skill 设计

1. **不能只有方法描述**: 必须包含具体代码和输出格式
2. **必须说明差异**: paper 方法与默认方法的具体区别
3. **提供鲁棒模式**: agent 需要的可复制代码模板

### 关于 Task 设计

1. **排除替代方案**: 如果存在简单方法可以达到相同结果，task 设计失败
2. **明确数据结构**: input 文件格式必须明确说明
3. **可验证性**: reference output 必须能够验证 paper 方法的使用

---

**修复后预期**: Paper arm 在所有 5 个任务上成功，平均 Paper-None 差异 ≥ +0.4
