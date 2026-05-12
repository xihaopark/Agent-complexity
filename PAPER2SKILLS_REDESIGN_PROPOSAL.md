# Paper2Skills 实验重新设计提案

> 目标: 设计能真正证明"从Paper自动提取Skill对Agent有独特益处"的实验

---

## 当前实验的核心问题

### 问题1: 任务太简单 (44%的任务)

**现象**: 14个任务四臂全部通过 (得分接近1.0)

**例子**:
- `akinyi_deseq2`: DESeq2标准流程
- `star_deseq2_init/contrast`: 标准DESeq2分析
- `clean_histoneHMM`: 简单bed文件处理

**为什么这是问题**:
```
Agent已经知道标准流程
↓
有无Paper Skill都能完成
↓
无法证明Paper Skill的价值
```

### 问题2: Paper内容不匹配 (33%的有Skill任务)

**现象**: Skill内容与Task需求不匹配，甚至误导Agent

**例子**:

| Task | 需要的知识 | Paper Skill给的 | 结果 |
|------|-----------|-----------------|------|
| `methylkit_load` | methylKit R包操作代码 | MethPat可视化工具描述 | Paper 0.075 |
| `snakepipes_merge_fc` | 具体R merge代码 | snakePipes工作流框架描述 | Paper 0.698 (比None差) |
| `dea_limma` | limma使用代码 | limma论文确实有代码 | 效果好 |

**为什么这是问题**:
```
Paper是关于工具A的
↓
Task需要工具B的操作
↓
Skill无效或有害
```

### 问题3: 没有设计"非显而易见"的任务

**现象**: 所有任务都是"标准做法就能完成"的

**缺少什么**:
- 有陷阱的任务 (看似应该这样做，但实际那样做才对)
- 需要特定参数的任务 (默认参数会失败)
- 需要领域知识的任务 (通用知识不够)

---

## 理想的实验应该证明什么

### 核心假设

```
当Agent具备特定的、非显而易见的领域知识时
↓
它能解决仅靠通用知识无法解决的任务
↓
这些知识可以从相关Paper自动提取
```

### 成功的标准

| 对比 | 理想差异 | 当前实验表现 | 评估 |
|------|---------|-------------|------|
| Paper vs None | > 0.5 | methylkit_filt_norm: 0.843 ✅<br>其他: 0.0-0.2 ❌ | 仅1个成功 |
| Paper vs Pipeline | > 0.3 | 多数: 0.0-0.1 ❌ | Pipeline足够 |
| Paper vs LLM_Plan | > 0.4 | 多数: 0.0-0.2 ❌ | Plan足够 |

---

## 重新设计的两大支柱

### 支柱1: 正确选择Paper

#### 不应该选择的Paper类型

❌ **工作流系统论文** (当前大量使用)
- 例子: snakePipes论文描述Snakemake工作流框架
- 问题: 没有具体R代码，全是配置描述

❌ **可视化工具论文**
- 例子: MethPat论文是关于可视化工具，不是methylKit教程
- 问题: 工具不匹配

❌ **纯综述或概念论文**
- 没有可执行代码
- 只有高层概念

#### 应该选择的Paper类型

✅ **方法学论文 (Methods Papers)**
- 专门介绍新算法或工具的论文
- 必须有具体可执行代码

✅ **最佳实践指南 (Best Practice Guidelines)**
- "RNA-seq分析十个注意点"
- "小样本RNA-seq处理建议"

✅ **教程类论文 (Tutorials)**
- 软件官方教程或vignette
- 有完整代码示例

#### Paper内容质量检查清单

**强制要求** (不满足则不使用):
- [ ] 包含可执行的R代码片段 (>= 5行)
- [ ] 明确提及Task所需的具体函数/包
- [ ] 有参数设置建议 (非全默认)

**重要加分项**:
- [ ] 有输入数据格式说明
- [ ] 有输出结果示例
- [ ] 指出常见错误或注意事项

**排除项** (有任一即跳过):
- [ ] 纯工作流框架描述
- [ ] 纯可视化/图形工具
- [ ] 只有高层概念无代码
- [ ] 与Task工具明显不匹配

---

### 支柱2: 设计"Skill敏感型"任务

#### 原则

设计**只有**具备正确外部知识(Paper Skill)时才能成功的任务

仅靠:
- 内部知识 (LLM训练数据) ❌
- 通用代码 (Pipeline) ❌
- 通用规划 (LLM Plan) ❌

#### 三种有效策略

##### 策略A: 设计"有陷阱"的任务

**概念**: 任务有看似合理的默认解法，但实际上会失败或次优

**示例1: `tricky_normalization`**
```
场景: 提供有明显批次效应的count数据

陷阱解法: 直接TMM normalization
→ 批次效应残留 → 假阳性DE
→ 得分: 0.3

正确解法 (Paper Skill): ComBat去批次 → TMM
→ 批次效应去除 → 真阴性保留
→ 得分: 0.95

Skill内容: "对于这种数据，应先ComBat去批次再TMM"
```

**示例2: `small_sample_shrinkage`**
```
场景: n=2 per group的RNA-seq数据

陷阱解法: 标准DESeq2 lfcShrink
→ lfcSE极大 → 不可靠logFC
→ 得分: 0.4

正确解法 (Paper Skill): apeglm或ashr shrinkage
→ 稳定shrinkage
→ 得分: 0.95

Skill内容: "n<3时应使用apeglm或ashr shrinkage"
```

##### 策略B: 设计"需要特定参数"的任务

**概念**: 任务有必须设置的特定参数，默认/通用参数会导致失败

**示例: `fragment_length_specific`**
```
场景: 单端RNA-seq数据，需要估计插入片段长度

默认参数: 不使用fragment length或auto
→ 结果错误
→ 得分: 0.2

正确参数 (Paper Skill): --frag-len 200
→ 结果正确
→ 得分: 0.95

Skill内容: "对于单端数据，建议使用--frag-len 200"
```

##### 策略C: 设计"多步骤特定顺序"的任务

**概念**: 步骤顺序或组合方式影响结果，Paper提供验证过的流程

**示例: `specific_filter_order`**
```
场景: RNA-seq QC和过滤

错误顺序: normalize → filter
→ 低表达基因影响normalization因子
→ 得分: 0.4

正确顺序 (Paper Skill): filter → normalize
→ 正确的normalization
→ 得分: 0.95

Skill内容: "低表达基因应在normalization前过滤"
```

---

## 具体的新Task设计建议

### 10个示例任务

#### 类别1: Normalization陷阱 (3个)

1. **`batch_effect_rna`**
   - 输入: 有明显批次效应的counts
   - 所需知识: ComBat去批次后再normalization
   - 预期: None 0.3, Paper 0.95

2. **`composition_bias_sc`**
   - 输入: 有强烈composition bias的scRNA-seq
   - 所需知识: scran的computeSumFactors
   - 预期: None 0.35, Paper 0.95

3. **`spike_in_norm`**
   - 输入: 有ERCC spike-in的RNA-seq
   - 所需知识: spike-in based normalization
   - 预期: None 0.3, Paper 0.95

#### 类别2: DE分析特异性 (3个)

4. **`small_sample_shrinkage`**
   - 输入: n=2 per group
   - 所需知识: apeglm/ashr shrinkage
   - 预期: None 0.4, Paper 0.95

5. **`paired_design_de`**
   - 输入: 配对设计数据(治疗前后)
   - 所需知识: ~patient + treatment模型
   - 预期: None 0.3, Paper 0.95

6. **`interaction_contrast`**
   - 输入: 需要检验交互作用的数据
   - 所需知识: 正确的contrast设置
   - 预期: None 0.35, Paper 0.95

#### 类别3: QC和过滤特异性 (2个)

7. **`adaptive_filter_threshold`**
   - 输入: 需要动态过滤阈值的数据
   - 所需知识: 根据数据质量调整阈值
   - 预期: None 0.4, Paper 0.9

8. **`outlier_detection`**
   - 输入: 有潜在outlier样本的数据
   - 所需知识: PCA-based outlier检测
   - 预期: None 0.35, Paper 0.9

#### 类别4: 特定工具使用 (2个)

9. **`complex_heatmap_params`**
   - 输入: 需要复杂热图的多组学数据
   - 所需知识: ComplexHeatmap特定参数
   - 预期: None 0.3, Paper 0.9

10. **`specific_biomarker_cutoff`**
    - 输入: 生物标志物表达数据
    - 所需知识: 特定疾病的标准cutoff
    - 预期: None 0.25, Paper 0.95

---

## 实验对比的预期效果

### 我们希望看到的效果矩阵

| 任务类型 | None | LLM_Plan | Pipeline | Paper | 结论 |
|---------|------|----------|----------|-------|------|
| **标准流程**<br>(如标准DESeq2) | 0.95 | 0.95 | 0.95 | 0.95 | 太简单<br>移除 |
| **需要外部知识**<br>(如特定normalization) | 0.25 | 0.30 | 0.40 | 0.95 | ✅ **理想情况** |
| **代码模板足够**<br>(如标准merge) | 0.25 | 0.30 | 0.90 | 0.90 | Pipeline有效<br>Paper无额外优势 |
| **领域知识关键**<br>(如癌症特异性) | 0.25 | 0.30 | 0.35 | 0.95 | ✅ **Paper独特价值** |

### 关键指标阈值

- **Paper vs None** 差异 > 0.5 → 证明Skill有价值
- **Paper vs Pipeline** 差异 > 0.3 → 证明Paper比代码模板更有价值
- **Paper vs LLM_Plan** 差异 > 0.4 → 证明具体Paper知识比通用Plan有效

---

## 实施路线图

### 阶段1: 立即执行 (1-2周)

1. **筛选现有任务**
   - 标记所有"四臂全过"任务 (14个)
   - 标记所有"有Paper Skill但失败"任务 (5个)
   - 保留`methylkit_filt_norm`作为成功案例

2. **重新评估Paper匹配**
   - 检查5个失败Skill的Paper内容
   - 如果不匹配，寻找替代Paper

### 阶段2: 新Task开发 (2-4周)

1. **设计10个新Task**
   - 按照上述三类策略
   - 每个Task配套寻找合适Paper

2. **预实验验证**
   - 小样本测试None arm表现
   - 确认Task足够难

### 阶段3: 完整实验 (2-3周)

1. **运行4-Arm实验**
2. **分析结果**
3. **验证假设是否成立**

---

## 核心转变总结

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                        关键转变                                ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                                                ┃
┃  从: "让Agent完成标准生物信息学任务"                           ┃
┃  到: "设计只有具备特定领域知识才能做好的任务"                  ┃
┃                                                                ┃
┃  从: "从workflow关联的paper提取skill"                         ┃
┃  到: "为特定技术问题寻找最相关的tutorial/methods paper"        ┃
┃                                                                ┃
┃  从: "测试Agent的基础能力"                                    ┃
┃  到: "测试外部知识注入的独特价值"                              ┃
┃                                                                ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

*提案完成*
