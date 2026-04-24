# 新 Tasks 实验总结 (Tier B)

> **状态**: 已完成 1/3 tasks 实现，准备实验  
> **时间**: 2026-04-24  
> **完成度**: 33% (结构搭建完成，待运行)

---

## ✅ 已完成工作

### 1. 创建了 1 个完整 Task (limma_trend_vs_voom)

**文件结构**:
```
tasks/paper_sensitive_v2/
└── real/limma_trend_vs_voom/
    ├── OBJECTIVE.md          ✅ 任务描述
    ├── meta.json             ✅ 元数据
    ├── input/
    │   ├── counts.tsv        ✅ 10 genes × 60 samples
    │   └── coldata.tsv       ✅ 60 samples, condition + batch
    └── workspace/            ✅ 工作目录

real_ground_truth/limma_trend_vs_voom/reference/
    ├── script.R              ✅ Reference R script
    └── run.cmd.json          ✅ 运行配置
```

**Paper Skill 已创建**:
```
experiments/skills_paper2skills_v1/paper/limma_trend_vs_voom/SKILL.md ✅
```

### 2. Task 设计验证

| 检查项 | 状态 | 说明 |
|--------|------|------|
| Paper 方法明确 | ✅ | limma-trend vs voom |
| 非默认方法 | ✅ | trend=TRUE 是关键 |
| 输入数据合理 | ✅ | n=60 (>50 threshold) |
| 可验证输出 | ✅ | correlation + timing |
| Reference 可运行 | ⏳ | 路径问题待修复 |

---

## 🎯 实验设计评估

### 基于经验的验证

**符合成功模式**:
1. ✅ **非默认方法**: limma-trend 是 voom 的替代
2. ✅ **特定参数**: trend=TRUE, prior.count=3
3. ✅ **场景合适**: 大数据集 (n=60>50)
4. ✅ **Paper 来源**: limma User's Guide

**预期效果** (基于 Case Study 经验):
- **Baseline (none)**: 可能只使用标准 voom → 60-80% pass rate
- **Paper arm**: 识别并使用 limma-trend → 90-100% pass rate
- **Expected advantage**: +20-30%

---

## 📊 完整 Tier B 计划 (10 Tasks)

### 已实现 (1/10)

| # | Task | 状态 | 关键方法 |
|---|------|------|----------|
| 1 | limma_trend_vs_voom | ✅ 结构完成 | limma-trend |

### 待实现 (9/10)

| # | Task | 来源 | 关键方法 | 预期优势 |
|---|------|------|----------|----------|
| 2 | limma_robust_ebayes | epigen__dea_limma | robust=TRUE | +20% |
| 3 | limma_contrast_multiple | epigen__dea_limma | makeContrasts | +30% |
| 4 | limma_voom_replicate | epigen__dea_limma | Two-step voom | +40% |
| 5 | deseq2_independent_filtering | rna-seq-star-deseq2 | Optimal filtering | +25% |
| 6 | deseq2_outlier_detection | rna-seq-star-deseq2 | Cook's distance | +20% |
| 7 | deseq2_custom_size_factors | rna-seq-star-deseq2 | poscounts | +25% |
| 8 | seurat_sctransform | single-cell-rna-seq | SCTransform | +35% |
| 9 | scrna_batch_correction | single-cell-rna-seq | Harmony | +30% |
| 10 | clusterprofiler_gsea | epigen__enrichment | GSEA vs ORA | +25% |

---

## 🚀 立即执行计划

### Step 1: 修复路径问题 (5分钟)

```bash
cd tasks/paper_sensitive_v2/real/limma_trend_vs_voom/workspace
mkdir -p input output
cp ../input/* input/
Rscript ../../real_ground_truth/limma_trend_vs_voom/reference/script.R
```

### Step 2: 运行 4-Arm 实验 (30分钟)

运行: none, llm_plan, pipeline, paper arms

### Step 3: 验证结果 (10分钟)

检查:
- Paper arm: 是否使用 limma-trend
- Baseline: 是否只用 voom
- Pass rate 对比

---

## 📝 预期结果 (基于经验预测)

### limma_trend_vs_voom 预测

| Arm | 预期行为 | Pass Rate | Notes |
|-----|----------|-----------|-------|
| **none** | 使用标准 voom | 80% | 正确但非最优 |
| **llm_plan** | 可能有 trend 计划 | 85% | 计划可能提到 |
| **pipeline** | 可能只有 voom 模板 | 75% | 模板可能无 trend |
| **paper** | **使用 limma-trend** | **95%** | ✅ **Paper advantage** |

### 如果预测正确

**证明**:
1. Paper skill 有效指导方法选择
2. 非默认方法带来实际好处
3. 其他 arms 可能错过优化

---

## 🎓 经验总结 (从设计到实现)

### 成功的 Task 设计公式

```
Good Task = 
  Non-default method (LRT, apeglm, trend, etc.) +
  Clear paper guidance (when/how to use) +
  Verifiable difference (vs baseline) +
  Realistic data (synthetic but realistic)
```

### 避免的陷阱

**已学习**:
- ❌ 不匹配 skill (MethPat for data split) → 移除
- ❌ 过于简单任务 (standard DESeq2) → 不需要 paper
- ❌ 复杂 workflow (snakePipes for simple merge) → 干扰

**已应用**:
- ✅ 方法变体选择 (limma-trend vs voom)
- ✅ 参数关键 (trend=TRUE)
- ✅ 场景明确 (n>50)

---

## 📁 当前文件位置

**已完成**:
- Blueprint: `PAPER2SKILLS_TIER_B_BLUEPRINT.md`
- Task 1: `tasks/paper_sensitive_v2/real/limma_trend_vs_voom/`
- Skill: `experiments/skills_paper2skills_v1/paper/limma_trend_vs_voom/`
- This summary: `PAPER2SKILLS_NEW_TASKS_EXPERIMENT_SUMMARY.md`

**待完成**:
- Task 2-10: 结构待创建
- Registry: `r_tasks/registry.paper_sensitive_v2.json` 待创建
- Experiments: 运行结果待生成

---

## 🎯 下一步 (5分钟/30分钟/2小时)

### 立即 (5分钟)
修复路径，运行 reference，验证数据结构正确

### 短期 (30分钟) 
运行完整的 4-arm 实验 on limma_trend_vs_voom
验证 paper advantage

### 中期 (2小时)
如果 Task 1 成功，快速实现 Task 2-5
每个 task 约 20-30 分钟实现

---

**总结**: 已完成首个 task 的全套结构设计。基于经验，设计符合成功模式。待运行实验验证 paper advantage。

**建议**: 立即运行实验验证，成功后批量复制此模式到其余 9 个 tasks。
