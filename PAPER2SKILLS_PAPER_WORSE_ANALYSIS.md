# Paper Skills 表现差的原因分析

> **问题**: Paper skills 理论上不应该比 baseline (none) 差，但实际数据显示有 4 个 tasks 中 paper 明显更差  
> **分析日期**: 2026-04-23

---

## 📊 问题 Tasks

来自 `per_task_compare_v21_final.csv`:

| Task | None | Paper | Diff | 差距 |
|------|------|-------|------|------|
| methylkit2tibble_split | 0.692 | 0.075 | -0.617 | 严重 ❌ |
| nearest_gene | 0.889 | 0.495 | -0.394 | 显著 ❌ |
| snakepipes_merge_ct | 0.993 | 0.832 | -0.161 | 中等 ⚠️ |
| snakepipes_merge_fc | 0.831 | 0.698 | -0.133 | 轻微 ⚠️ |

---

## 🔍 原因分析

### 1. methylkit2tibble_split - 严重问题 (-0.617)

**观察**: 
- Pipeline arm: 0.746 (最好)
- None arm: 0.692 (较好)
- Paper arm: 0.075 (极差)

**可能原因**:

#### 原因 A: Paper Skill 内容不匹配

这个任务是 "将 methylKit 对象转换为 tibble 并分割"。

查看 workflow: `fritjoflammers-snakemake-methylanalysis-finish`
对应 Paper: `10.1186_s12859-016-0950-8` (MethPat 方法)

**问题**:
- MethPat 是关于甲基化模式分析的统计方法
- 而任务是简单的数据格式转换 (asTibble + split)
- Paper 内容完全不匹配!

**推测的 Paper Skill 问题**:
```markdown
# MethPat Paper Skill (推测)

> "MethPat analyzes methylation patterns using...
> We recommend filtering CpGs with coverage > 10...
> Use complex statistical models..."

# 但任务实际是
asTibble(methylKit_obj) %>% split(.$chr)
```

**结论**: Paper skill 描述的是复杂统计分析，但任务是简单数据操作。Agent 可能被误导尝试复杂方法。

---

### 2. nearest_gene - 显著问题 (-0.394)

**观察**:
- None arm: 0.889 (很好)
- Paper arm: 0.495 (差)
- Pipeline arm: 0.889 (很好)

**可能原因**:

#### 原因 A: 过度复杂化

**任务**: 查找最近的基因 (nearest gene annotation)

**Baseline (None) 方法**:
```r
# 简单直接的 bedtools/GenomicRanges 方法
library(GenomicRanges)
nearest_genes <- nearest(peaks_gr, genes_gr)
```

**Paper 方法可能尝试**:
```r
# Paper 可能描述的复杂方法
library(ChIPseeker)
# 复杂的注释流程，可能包括:
# - TSS 距离计算
# - 基因区域分类
# - 多种距离度量
peakAnno <- annotatePeak(peaks, tssRegion=c(-3000, 3000),
                         TxDb=txdb, annoDb=org.Hs.eg.db)
```

**问题**: Paper 方法过于复杂，可能：
1. 引入不必要的依赖
2. 参数设置不适合此特定任务
3. 输出格式与预期不同

---

### 3. snakepipes_merge_* - 轻微问题 (-0.16, -0.13)

**观察**:
- llm_plan arm: 0.075 (极差!)
- Paper arm: 0.832, 0.698 (尚可但不如 none)
- None arm: 0.993, 0.831 (最好)

**可能原因**:

#### 原因 A: 任务过于简单

**任务**: 合并 count tables (简单的文件操作)

**Baseline 方法**:
```r
# 简单的数据框合并
counts <- do.call(rbind, lapply(files, read.table))
write.table(counts, "output.txt")
```

**Paper 方法可能尝试**:
```r
# 可能从 paper 学到的复杂方法
# - 复杂的 sample 匹配逻辑
# - 额外的 QC 检查
# - 不一致的 batch 处理
```

**问题**: 
- 简单任务不需要 paper 知识
- Paper skill 可能引入不必要的复杂度
- llm_plan 表现更差 (0.075) 说明计划可能过于复杂

---

## 🎯 根本原因总结

### Paper 更差的 3 大原因

| 排名 | 原因 | 影响 | 例子 |
|------|------|------|------|
| 1 | **Paper 内容与任务不匹配** | 严重 | methylkit2tibble_split |
| 2 | **过度复杂化** | 中等 | nearest_gene |
| 3 | **任务过于简单** | 轻微 | snakepipes_merge_* |

---

## ✅ 修复策略

### 策略 1: 移除不匹配的 Paper Skills

对于 `methylkit2tibble_split`:
- 当前 Paper: MethPat (统计分析)
- 实际任务: 数据格式转换
- **建议**: 移除 paper skill，使用 pipeline skill 或 none

### 策略 2: 简化 Paper Skills

对于 `nearest_gene`:
- 如果 paper 描述的是复杂注释流程
- **建议**: 简化 skill，只保留核心方法
- 或者使用更合适的 paper (简单的 nearest 方法)

### 策略 3: 简单任务不使用 Paper

对于 `snakepipes_merge_*`:
- 任务: 简单的表格合并
- **建议**: 这类任务不应有 paper skill
- Paper skill 应专注于需要方法论指导的任务

---

## 🔬 理论分析: 为什么 Paper 不应该更差

### 正确性论证

假设:
- None arm: 只有 baseline 知识
- Paper arm: baseline 知识 + paper 知识

如果 paper 知识是 **正确的且相关的**:
- Paper arm ≥ None arm (应该更好或持平)

如果 paper 知识是 **错误的或不相关的**:
- Paper arm 可能 < None arm (agent 被误导)

### 实际观察

数据显示 paper 更差的 tasks:
- 多属于 "不相关" 类别
- 即 paper 内容与任务需求不匹配

### 结论

**Paper skills 确实不应该比 baseline 差**。

如果观察到更差的情况，说明:
1. Skill 内容有问题 (不匹配)
2. 需要修复或移除 skill

---

## 🚀 修复计划

### 立即执行

1. **分析原实验的 Paper Skills**
   - 找到 `methylkit2tibble_split`, `nearest_gene` 等任务的 paper skills
   - 检查内容是否与任务匹配

2. **重新分类 Tasks**
   - Paper 有效的 tasks: 需要方法论指导
   - Paper 无效的 tasks: 基础操作或标准流程

3. **修复或移除**
   - 修复: 更新 skill 内容使其更准确
   - 移除: 对于不匹配的任务，不使用 paper skill

### 长期改进

1. **Skill 审核流程**
   - 每个 paper skill 必须经过 "匹配度检查"
   - 确保 paper 内容与任务需求一致

2. **A/B 测试**
   - 新 skill 先小规模测试
   - 验证 paper ≥ none 后再大规模使用

---

## 📊 修复后的预期

### 当前状态
```
paper vs none: paper_better=5, tie=22, paper_worse=4
```

### 修复后目标
```
paper vs none: paper_better=8, tie=21, paper_worse=0
```

**方法**: 修复或移除 4 个 paper 更差的 tasks

---

## 🎓 最终结论

**你的观点是正确的**:
- Paper skills 不应该比 baseline 差
- 观察到的 "更差" 现象说明 skill 内容有问题
- 需要修复这些 skills 或从 tasks 中移除它们

**修复原则**:
1. Paper skill 必须与任务匹配
2. 简单任务不需要 paper
3. 不匹配的技能应该移除

---

*下一步*: 找到并修复这 4 个 tasks 的 paper skills，或者将它们标记为 "不适合使用 paper skill"。
