# Paper2Skills 故事设计指南

> 如何构建能证明"Paper自动提取Skill有价值"的完整叙事

---

## 核心发现：为什么当前实验没讲好故事

### 震惊的发现

唯一"成功"案例 (`methylkit_filt_norm`, diff +0.843) 实际上是个**假阳性**！

| 方面 | 实际情况 |
|------|---------|
| **Skill内容** | ❌ 无R代码，是关于MethPat可视化的 |
| **Task成功原因** | ✅ 输出TSV(可评估) + Agent已知filterByCoverage函数 |
| **真实情况** | **不是**skill帮助了agent，而是task设计合理+agent本身知识足够 |

**结论**: 我们以为的"成功案例"，实际上skill质量并不好，成功是因为其他因素。

---

## 真正需要的故事结构

### 对比：实际 vs 理想

```
实际发生的故事:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Agent已有知识 + Task设计合理 → Agent完成任务
(Skill内容质量不重要)

我们需要的故事:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Agent没有知识 + Task很难 → Agent失败 (None arm: 0.2-0.4)
Agent获得Paper Skill → Agent成功 (Paper arm: >0.9)
Paper vs None差异 > 0.5 → 证明Skill独特价值
```

---

## 模式分析：成功案例 vs 失败案例

### 五类模式总结

| Task | 状态 | Paper质量 | Task难度 | 关键问题 | 教训 |
|------|------|-----------|----------|----------|------|
| `methylkit_filt_norm` | 表面成功 | 低(无代码) | 中 | 不是skill帮助 | **需要更难的任务** |
| `star_deseq2_init` | 中性 | 高(有代码) | **低** | 任务太简单，所有arm都会 | **需要非标准流程** |
| `dea_limma` | 中性 | 高(有代码) | 中 | 所有arm都难，无区分度 | **需要区分度高的设计** |
| `snakepipes_merge_fc` | **有害** | 低(工作流描述) | 中 | Skill与Task不匹配 | **必须严格匹配工具** |
| `methylkit2tibble_split` | 失败 | 低(无代码) | 高 | 评估器限制(RDS) | **避免S4对象输出** |

### 四类任务的分布

```
18个有Paper Skill的任务分布:

🌟 HIGHLY EFFECTIVE (diff > 0.5): 1个 (5.6%)
   └─ methylkit_filt_norm (假阳性)

⚪ NEUTRAL (diff ≈ 0): 13个 (72%)
   ├─ 8个: 任务太简单，四臂全过
   └─ 5个: 任务有缺陷，所有arm都失败

❌ HARMFUL (diff < -0.1): 4个 (22%)
   └─ Skill内容与Task不匹配或误导
```

---

## 讲故事的三幕结构

### 第一幕: "展示Agent的局限" (3-4个任务)

**目标**: 证明Agent仅靠自身知识不够

**设计策略**:
- 标准流程但有陷阱
- None arm预期得分: 0.2-0.4
- 失败模式: 使用默认方法导致次优结果

**示例任务**:

| 任务 | 陷阱 | None得分 | Paper得分 |
|------|------|----------|-----------|
| `small_sample_shrinkage` | 标准DESeq2 lfcShrink在n=2时不稳定 | 0.35 | 0.95 |
| `batch_combat_first` | 直接TMM导致批次效应残留 | 0.30 | 0.95 |
| `composition_bias_sc` | 简单library size不够 | 0.30 | 0.95 |

**需要的Paper类型**:
- Methods paper on shrinkage estimators
- Batch effect correction tutorial
- scRNA-seq best practices

---

### 第二幕: "展示通用方法不够" (3-4个任务)

**目标**: 证明Pipeline代码模板和LLM Plan规划不够

**设计策略**:
- 需要领域特定知识
- Pipeline arm预期得分: 0.4-0.6 (比None好但不够)
- LLM Plan arm预期得分: 0.4-0.6 (有规划但缺知识)

**示例任务**:

| 任务 | 为什么通用方法不够 | None | Pipeline | Paper |
|------|-------------------|------|----------|-------|
| `specific_frag_len` | 需要参数=200的知识 | 0.25 | 0.40 | 0.95 |
| `scrna_size_factor` | 需要scran特定方法 | 0.30 | 0.45 | 0.95 |
| `paired_design_model` | 需要~patient+treatment设计 | 0.25 | 0.50 | 0.95 |

**需要的Paper类型**:
- Tool documentation with parameter guide
- Statistical design papers
- Linear model tutorials

---

### 第三幕: "展示Paper Skill的价值" (4-6个任务)

**目标**: 证明Paper Skill显著优于所有其他方法

**设计策略**:
- 有匹配的高质量Paper Skill
- Paper arm预期得分: 0.9-1.0
- Paper vs None > 0.5
- Paper vs Pipeline > 0.3
- Paper vs LLM Plan > 0.4

**示例任务**:

| 任务 | Skill关键内容 | Paper得分 | 关键对比 |
|------|--------------|-----------|----------|
| `apeglm_shrinkage` | apeglm替代lfcShrink | 0.95 | vs None +0.60 |
| `combat_seq_params` | ComBat-seq参数调优 | 0.95 | vs Pipeline +0.50 |
| `interaction_contrast` | makeContrasts复杂设置 | 0.95 | vs LLM Plan +0.55 |
| `outlier_pca_method` | PCA-based outlier检测 | 0.95 | vs None +0.65 |

**需要的Paper类型**:
- 高质量Methods papers
- 软件官方vignettes
- Best practice guidelines with code

---

## 成功因素 vs 失败因素

### ✅ 关键成功因素

| 因素 | 重要性 | 检测方法 |
|------|--------|----------|
| **Task难度合适** | ⭐⭐⭐⭐⭐ | None arm 0.2-0.4 |
| **Paper严格匹配** | ⭐⭐⭐⭐⭐ | Skill包含Task所需函数名 |
| **Skill有代码** | ⭐⭐⭐⭐ | Skill有```r代码块 |
| **输出可评估** | ⭐⭐⭐⭐ | TSV/CSV而非RDS |
| **区分度高** | ⭐⭐⭐⭐ | Paper vs其他 > 0.5 |

### ❌ 必须避免的陷阱

| 陷阱 | 当前问题 | 解决方案 |
|------|---------|---------|
| Task太简单 | 44%四臂全过 | 增加陷阱或特定参数 |
| Paper不匹配 | MethPat vs methylKit | 严格匹配工具名称 |
| Skill无代码 | "No code snippets visible" | 筛选有代码的papers |
| RDS S4输出 | 评估器无法比较 | 改为TSV输出 |
| 缺乏baseline | 无法证明相对价值 | 确保None得分低 |

---

## 具体的新Task设计建议

### 完整Task清单 (12-14个任务，讲好三幕故事)

#### 第一幕: Agent局限 (4个任务)

| # | 任务名 | 场景 | 陷阱 | None | Paper | 差异 | Paper类型 |
|---|--------|------|------|------|-------|------|-----------|
| 1 | small_sample_shrinkage | n=2 per group | 标准lfcShrink不稳定 | 0.35 | 0.95 | +0.60 | apeglm methods |
| 2 | batch_combat_first | 有批次效应 | 直接TMM残留批次 | 0.30 | 0.95 | +0.65 | ComBat tutorial |
| 3 | composition_bias_sc | scRNA-seq | library size不够 | 0.30 | 0.95 | +0.65 | scran best practices |
| 4 | spike_in_norm | 有ERCC spike-in | 忽略spike-in | 0.25 | 0.95 | +0.70 | spike-in methods |

#### 第二幕: 通用方法不够 (4个任务)

| # | 任务名 | 为什么通用不够 | None | Pipeline | Paper | Paper类型 |
|---|--------|--------------|------|----------|-------|-----------|
| 5 | specific_frag_len | 需要参数=200 | 0.25 | 0.40 | 0.95 | tool docs |
| 6 | adaptive_threshold | 动态过滤阈值 | 0.30 | 0.45 | 0.95 | QC guide |
| 7 | outlier_pca | PCA-based检测 | 0.30 | 0.50 | 0.95 | outlier methods |
| 8 | paired_design | ~patient+treatment | 0.25 | 0.50 | 0.95 | limma tutorial |

#### 第三幕: Paper Skill价值 (6个任务)

| # | 任务名 | Skill关键知识 | Paper | vs None | vs Pipeline | Paper类型 |
|---|--------|--------------|-------|---------|-------------|-----------|
| 9 | apeglm_details | apeglm参数调优 | 0.95 | +0.60 | +0.50 | methods paper |
| 10 | combat_seq | ComBat-seq使用 | 0.95 | +0.65 | +0.50 | tutorial |
| 11 | complex_contrast | makeContrasts | 0.95 | +0.55 | +0.45 | limma guide |
| 12 | size_factor_scran | computeSumFactors | 0.95 | +0.65 | +0.55 | best practices |
| 13 | heatmap_complex | ComplexHeatmap | 0.95 | +0.70 | +0.50 | package vignette |
| 14 | biomarker_cutoff | 疾病特异cutoff | 0.95 | +0.70 | +0.60 | clinical guide |

---

## 实施路线图

### 阶段1: 筛选和改造现有任务 (1-2周)

1. **筛选现有任务**
   - ❌ 移除所有"四臂全过"任务 (14个)
   - ❌ 移除所有RDS输出任务 (4个methylKit)
   - ❌ 移除Skill不匹配的 harmful 任务 (4个)
   - ✅ 保留 `methylkit_filt_norm` 作为锚点案例

2. **改造可用任务**
   - 修改输出格式 (RDS → TSV)
   - 增加难度 (添加陷阱或特定参数要求)

### 阶段2: 开发新任务 (3-4周)

1. **设计12-14个新任务**
   - 按照三幕结构
   - 每个任务配套寻找合适Paper

2. **预实验验证**
   - 跑None arm确认难度
   - 目标: None 0.2-0.4, Paper >0.9

### 阶段3: 完整实验 (2-3周)

1. **运行4-Arm实验**
2. **分析结果**
3. **验证故事是否成立**

---

## 最终检验清单

### Task设计检验

- [ ] None arm预跑得分 0.2-0.4
- [ ] 有明确"陷阱"或特定参数需求
- [ ] 输出TSV/CSV (非RDS)
- [ ] 有匹配的高质量Paper

### Paper检验

- [ ] 包含可执行R代码 (≥5行)
- [ ] 明确提及Task所需函数
- [ ] 有非默认参数建议
- [ ] 与Task工具严格匹配

### 故事结构检验

- [ ] 第一幕 ≥3个任务 (展示Agent局限)
- [ ] 第二幕 ≥3个任务 (展示通用方法不够)
- [ ] 第三幕 ≥4个任务 (展示Paper Skill价值)
- [ ] Paper vs None 差异 > 0.5
- [ ] Paper vs Pipeline 差异 > 0.3

---

## 总结：讲故事的艺术

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                              ┃
┃  核心转变:                                                                   ┃
┃                                                                              ┃
┃  从: 证明"Agent能完成生物信息学任务"                                         ┃
┃  到: 证明"Paper Skill提供不可替代的领域知识"                                  ┃
┃                                                                              ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                                              ┃
┃  故事主线:                                                                   ┃
┃                                                                              ┃
┃  1️⃣ Agent会失败 (None 0.2-0.4)                                                ┃
┃       ↓                                                                      ┃
┃  2️⃣ 通用方法不够 (Pipeline 0.4-0.6)                                           ┃
┃       ↓                                                                      ┃
┃  3️⃣ Paper Skill拯救 (Paper 0.9-1.0)                                           ┃
┃       ↓                                                                      ┃
┃  🎯 结论: Paper自动提取Skill有价值！                                           ┃
┃                                                                              ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

*故事设计完成*
