# Agent Skills Library 使用指南

> **核心理念**: 不是遵循固定的 task→skill 映射，而是**根据当前场景自主发现、评估并选择合适的技能**。

---

## 1. 什么时候查询 Library？

### 🟢 强烈建议查询
- 面对**不熟悉**的分析任务时
- 知道工具名但**不确定参数选择**时
- 当前方法**失败或结果异常**时（寻找替代方案）
- 需要**验证**自己的分析策略是否合理时

### 🟡 可考虑查询
- 熟悉的任务但**出现了新的数据特征**（如 unusually small sample size）
- 多个工具都能做，需要**选择最合适的**

### 🔴 不必查询
- 明确知道该怎么做，且过往经验证明有效
- 纯机械的数据整理步骤

---

## 2. 如何查询？（三种模式）

### 模式 A: 场景驱动 (推荐)

```bash
# 我不确定怎么分析，先查场景
python paperskills/library/discovery.py --scenario rna_de_analysis
```

输出示例：
```
📋 Scenario: Differential expression analysis of RNA-seq data

💡 Decision Guide:
   Use DESeq2 for count-based analysis with built-in normalization. 
   Use limma+voom if you need flexible designs or have quality variations.

🔧 Relevant Skills:
   • DESeq2
   • limma
```

**Agent 行动**: 阅读 Decision Guide，根据数据特征选择。

---

### 模式 B: 标准匹配

```bash
# 明确知道分析类型、数据类型、设计
python paperskills/library/discovery.py \
    --analysis differential_expression \
    --data-type rna_seq_counts \
    --design small_sample
```

输出示例：
```
🔍 Matching skills (by relevance):
   [5★] DESeq2 - differential_expression
   [4★] limma - differential_expression
```

**Agent 行动**: 查看高匹配度的技能，阅读 SKILL.md 的具体指导。

---

### 模式 C: 关系探索

```bash
# 我在用 DESeq2，想看看有没有更好的选择
python paperskills/library/discovery.py --alternatives-to DESeq2

# DESeq2 做完后，下一步该做什么？
python paperskills/library/discovery.py --downstream-of DESeq2

# 我在做 pathway analysis，之前应该用什么工具？
python paperskills/library/discovery.py --upstream-of clusterProfiler
```

---

## 3. 如何阅读 SKILL.md？

每个 SKILL.md 的结构：

```markdown
## Method
核心方法描述。问自己：这与我的数据匹配吗？

## Parameters  
关键参数。问自己：我需要调整默认值吗？

## Commands / Code Snippets
实际代码。问自己：能直接运行还是需要修改？

## Notes for R-analysis agent
Agent 专属建议。重点阅读！
```

### 评估检查清单

阅读后，回答以下问题：

| 检查项 | 问题 |
|--------|------|
| ✅ 数据类型匹配 | 我的数据符合 "applicable_data_types" 吗？ |
| ✅ 设计匹配 | 我的实验设计在 "experimental_designs" 中吗？ |
| ⚠️ 限制注意 | "limitations" 中有没有我踩中的坑？ |
| 🔧 参数调整 | "Parameters" 中哪些我需要显式设置？ |

---

## 4. 选择决策流程

```
┌─────────────────────────────────────────┐
│  1. 分析当前任务特征                     │
│     - 数据类型？counts/normalized？      │
│     - 实验设计？两组/多组/时间/配对？     │
│     - 样本量？小样本 (n<5) 还是充足？    │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│  2. 查询 discovery.py                   │
│     --scenario 或 --analysis/--design   │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│  3. 获取 2-3 个候选技能                  │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│  4. 阅读各 SKILL.md 的 Method + Notes   │
│     重点看 use_when / not_when          │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│  5. 做出选择                            │
│     - 如果有明确匹配 → 用最优选择       │
│     - 如果不确定 → 尝试最保守的选项     │
│     - 如果有时间 → 对比 2 个备选        │
└─────────────────────────────────────────┘
```

---

## 5. 常见场景速查

### 场景: RNA-seq DE analysis, 样本充足 (n≥3 per group)

```bash
# Query
python paperskills/library/discovery.py --scenario rna_de_analysis

# Expected recommendation
首选: DESeq2 (counts) 或 limma+voom (需要灵活设计)

# 阅读 SKILL.md 重点
- DESeq2: design formula, results() 提取 contrast
- 注意: lfcShrink() 是否需要？默认 type="normal" 已 deprecated，用 apeglm
```

### 场景: RNA-seq, 极小样本 (n=2 per group)

```bash
# Query
python paperskills/library/discovery.py \
    --analysis differential_expression \
    --design small_sample

# Expected recommendation  
首选: DESeq2 with lfcShrink(type="apeglm")

# 阅读 SKILL.md 重点
- "apeglm provides more stable estimates than ashr for n<5"
- 避免: ashr 或 normal shrinkage
```

### 场景: 配对设计 (patient-matched tumor/normal)

```bash
# Query  
python paperskills/library/discovery.py \
    --analysis differential_expression \
    --design paired_samples

# Expected recommendation
首选: limma + duplicateCorrelation()

# 阅读 SKILL.md 重点
- block=patient 参数
- 先 estimate correlation, 再 fit model
```

### 场景: ChIP-seq peak calling

```bash
# Query
python paperskills/library/discovery.py --scenario chip_peak_calling

# Expected recommendation
首选: MACS2

# 关键决策
- Histone marks (H3K27me3, H3K36me3) → --broad
- Transcription factors → default narrow peaks
```

---

## 6. 避免的错误

### ❌ 不要
- **盲目使用绑定 skill** → 没有评估是否适合当前数据
- **忽视 limitations** → 每个方法都有适用边界
- **不看 not_when** → "not_when" 往往包含常见误用

### ✅ 要
- **优先阅读 Notes for R-analysis agent** → 专门为 agent 写的建议
- **检查实验设计匹配** → 配对设计用 duplicateCorrelation，小样本用 apeglm
- **考虑工具链** → DESeq2 → clusterProfiler 是自然 workflow

---

## 7. 进阶: 对比多个选择

当你有两个候选工具（如 DESeq2 vs limma）时：

```bash
# 获取各自详细信息
python paperskills/library/query.py --tool DESeq2 --json > /tmp/deseq2.json
python paperskills/library/query.py --tool limma --json > /tmp/limma.json

# 对比维度
- 数据类型: DESeq2 (counts) vs limma (voom transforms counts)
- 设计灵活性: limma > DESeq2
- 小样本稳健性: DESeq2+apeglm ≈ limma+eBayes
- 速度: limma 通常更快
```

**决策原则**: 如果有明确优势匹配当前场景，选择更优的；否则选择你更熟悉的。

---

## 8. Library 更新与反馈

### 如果某个 skill 帮助了你完成任务
```bash
# 可选：记录成功经验
# 这帮助改进 "use_when" 描述，而非强制绑定
```

### 如果 skill 不 work
1. 检查是否违反了 "not_when"
2. 尝试 discovery 推荐的 alternatives
3. 可能需要补充新的 skill（如尚未入库的 edgeR）

---

**记住**: Library 是**指南针**，不是**地图**。它指引方向，但具体路线需要 agent 根据实时情况选择。
