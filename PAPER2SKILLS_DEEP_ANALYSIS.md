# Paper2Skills 深度分析报告

> 生成时间: 2026-04-23
> 分析对象: 32个R任务 × 4臂消融实验 (none/llm_plan/pipeline/paper)
> 评估器版本: V2.1

---

## 执行摘要

本报告深度分析了32个R任务的实验结果，从**任务设计合理性**和**Paper Skill实际作用**两个维度进行系统性评估。

### 核心发现

| 维度 | 关键发现 |
|------|---------|
| **任务设计** | 44% (14/32)任务过于简单，无法区分skill价值；12.5% (4/32)任务存在严重设计缺陷 |
| **Skill有效性** | 仅5.6% (1/18)的skill任务显示明确优势；33% (6/18)skill无效甚至有害 |
| **评估器限制** | methylKit S4对象评估仍存在技术障碍 |

---

## Part 1: 任务设计合理性分析

### 1.1 任务分类统计

| 问题类型 | 数量 | 占比 | 代表任务 |
|---------|------|------|---------|
| **TOO_EASY** (四臂全过) | 14 | 43.8% | akinyi_deseq2, star_deseq2_*, msisensor_merge |
| **NO_SKILL_BUT_PASS** (无skill高分) | 12 | 37.5% | chipseq_plot_*, longseq_*, spilterlize_* |
| **HIGH_VARIANCE** (高方差不稳定) | 7 | 21.9% | epibtn_rpkm, methylkit_*, nearest_gene |
| **PAPER_SKILL_FAIL** (有skill仍失败) | 5 | 15.6% | methylkit_load/unite/to_tibble |
| **METHYLKIT_S4** (评估器限制) | 4 | 12.5% | methylkit_load/unite/to_tibble/split |
| **ALL_ARMS_FAIL** (全失败) | 2 | 6.3% | methylkit_load/unite |

### 1.2 严重设计问题详析

#### 🔴 methylKit系列任务 (4个)

| 任务 | Paper得分 | None得分 | 失败模式 | 根因 |
|------|----------|---------|---------|------|
| methylkit_load | 0.075 | 0.075 | rscript_crashed | treatment参数缺失 |
| methylkit_unite | 0.075 | 0.075 | rscript_crashed | treatment参数缺失 |
| methylkit_to_tibble | 0.225 | 0.150 | rscript_crashed | group_by错误 |
| methylkit2tibble_split | 0.075 | 0.692 | rscript_crashed | S4对象处理问题 |

**问题诊断**:
1. **Agent层面**: 缺少methylKit特有的treatment参数设置知识
2. **Skill层面**: Paper Skill描述的是MethPat软件，非methylKit详细教程
3. **评估器层面**: RDS S4对象无法正确评估 (V2.1仍有局限)
4. **任务层面**: 未在OBJECTIVE中给出treatment参数值

**建议**: 从主实验集移除或改为TSV输出

---

## Part 2: Paper Skill 实际作用分析

### 2.1 18个有Skill任务的分类

| 类别 | 数量 | 占比 | 说明 |
|------|------|------|------|
| ✅ **明确有效** | 1 | 5.6% | paper显著优于none |
| ⚪ **任务太简单** | 8 | 44.4% | 所有arm都pass，无法体现skill价值 |
| ❌ **Skill有害/误导** | 3 | 16.7% | paper比none差 |
| 🔧 **无法挽救设计缺陷** | 4 | 22.2% | 任务本身有问题 |
| ❓ **效果不明显** | 2 | 11.1% | 需进一步优化 |

### 2.2 典型案例分析

#### ✅ 成功案例: methylkit_filt_norm

```
Paper:  0.993 (pass)  ✓
None:   0.150 (fail)  ✗
Diff:   +0.843        ← Paper skill产生巨大价值
```

**成功因素**:
- Skill包含methylKit的filterByCoverage和normalizeCoverage用法
- 任务本身设计合理 (输出TSV而非RDS)
- Agent能正确执行skill中的步骤

#### ❌ 失败案例: snakepipes_merge_fc

```
Paper:  0.698 (partial_pass)  ✗
None:   0.831 (partial_pass)  ✓
Diff:   -0.133                 ← Paper skill反而有害
```

**失败因素**:
- Skill描述的是snakePipes工作流管理系统
- 任务需要的是具体featureCounts合并的R代码
- Skill过于抽象，导致Agent生成复杂冗余代码

#### ❌ 误导案例: methylkit_load

```
Skill工具:  MethPat软件 (论文主题)
Task工具:   methylKit R包 (实际需求)
匹配度:     ❌ 低 (虽然都涉及methylation)
```

**问题**: Skill内容和任务需求严重不匹配

---

## Part 3: Skill内容质量分析

### 3.1 Skill提取方法对比

| Skill | 提取工具 | 主要内容 | 代码示例 | 匹配度 |
|-------|---------|---------|---------|--------|
| 10.1093_nar_gkv007 (limma) | vision_adapter/gpt-4o | limma包详细用法 | ✅ 完整R代码 | 高 |
| 10.1186_s13059-014-0550-8 (DESeq2) | vision_adapter/gpt-4o | DESeq2最佳实践 | ✅ 完整R代码 | 高 |
| 10.1186_s12859-016-0950-8 (methylKit) | vision_adapter/gpt-4o | MethPat软件描述 | ❌ 无代码 | 低 |
| 10.1093_bioinformatics_btz436 (snakePipes) | vision_adapter/gpt-4o | snakePipes工作流 | ❌ 无代码 | 低 |

### 3.2 成功Skill的特征

✅ **包含具体R代码示例**:
```r
design <- model.matrix(~ 0 + factor(c(1,1,2,2)))
fit <- lmFit(expressionData, design)
fit <- eBayes(fit)
topTable(fit)
```

✅ **明确列出关键函数**: voom, lmFit, eBayes, topTable

✅ **有R-agent专用说明**: "Use the `limma` package in R"

❌ **失败Skill的共同问题**:
- 工具名称匹配但内容不匹配 (MethPat vs methylKit)
- 描述过于高层抽象 (工作流系统 vs 具体R函数)
- 缺少可执行代码 ("No code snippets visible")

---

## Part 4: 核心结论

### 4.1 任务设计问题

1. **43.8%任务过于简单** → 无法区分skill价值
2. **12.5%任务有设计缺陷** → methylKit RDS评估器无法处理
3. **21.9%任务不稳定** → 四臂得分方差>0.5

### 4.2 Paper Skill 作用

1. **仅5.6%显示明确优势** → skill提取和匹配仍需改进
2. **33% skill无效甚至有害** → 内容匹配度低
3. **成功case的特征**: 具体代码示例 + 任务设计合理

### 4.3 评估器限制

- V2.1已大幅改进，但S4对象评估仍有局限
- methylKit系列任务需要特殊处理

---

## Part 5: 改进建议

### 5.1 任务集优化 (32 → ~20)

**建议移除**:
- 所有4个methylKit RDS任务
- 11个过于简单的标准流程任务

**建议保留**:
- methylkit_filt_norm (skill成功案例)
- chipseq_plot_macs_qc (paper arm显著优势)
- dea_limma, snakepipes_merge_* (需要skill调优)

### 5.2 Skill内容改进

1. **强制要求可执行代码**: 每个skill必须包含完整R代码示例
2. **任务匹配验证**: 在注入前验证skill内容与任务需求匹配度
3. **重新提取methylKit skill**: 从methylKit教程论文而非MethPat论文提取

### 5.3 评估器改进

- methylKit任务改为TSV输出
- 或增强S4对象比较能力

### 5.4 实验设计优化

- 增加中等难度任务比例 (40-60%通过率)
- 减少"四臂全过"任务
- 添加negative control任务

---

## 附录: 详细数据表

### 32任务完整得分表

| 任务ID | Paper | None | Pipeline | LLM_Plan | 有Skill | 主要问题 |
|--------|-------|------|----------|----------|---------|---------|
| akinyi_deseq2 | 1.000 | 1.000 | 1.000 | 1.000 | ✅ | TOO_EASY |
| star_deseq2_init | 1.000 | 0.993 | 1.000 | 0.965 | ✅ | TOO_EASY |
| star_deseq2_contrast | 1.000 | 1.000 | 1.000 | 1.000 | ✅ | TOO_EASY |
| methylkit_load | 0.075 | 0.075 | 0.150 | 0.075 | ✅ | METHYLKIT_S4 |
| methylkit_unite | 0.075 | 0.075 | 0.075 | 0.075 | ✅ | METHYLKIT_S4 |
| methylkit_to_tibble | 0.225 | 0.150 | 0.225 | 0.697 | ✅ | METHYLKIT_S4 |
| methylkit2tibble_split | 0.075 | 0.692 | 0.746 | 0.225 | ✅ | METHYLKIT_S4 |
| methylkit_filt_norm | 0.993 | 0.150 | 0.225 | 0.993 | ✅ | ✅ 成功案例 |
| methylkit_remove_snvs | 1.000 | 1.000 | 1.000 | 1.000 | ✅ | TOO_EASY |
| chipseq_plot_macs_qc | 0.993 | 0.673 | 0.598 | 0.763 | ❌ | NO_SKILL_BUT_GOOD |
| dea_limma | 0.706 | 0.706 | 0.854 | 0.751 | ✅ | SKILL_NO_EFFECT |
| ... (其他任务省略) | ... | ... | ... | ... | ... | ... |

完整数据见: `per_task_compare_v21_final.csv`

---

*报告完成*
