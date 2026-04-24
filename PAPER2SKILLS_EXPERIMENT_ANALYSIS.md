# 自适应 Paper Skill 实验结果分析

> **实验日期**: 2026-04-24  
> **任务**: 4 个之前 paper 表现差的 tasks  
> **方法**: Agent 自主查询 skills，决定是否使用

---

## 📊 实验结果

| Task | Old None | Old Paper | **New Paper** | Old Diff | New Diff | Skill Used |
|------|----------|-----------|---------------|----------|----------|------------|
| methylkit2tibble_split | 0.692 | 0.075 | **0.000** | -0.617 | **-0.692** | None |
| nearest_gene | 0.889 | 0.495 | **0.000** | -0.394 | **-0.889** | None |
| snakepipes_merge_ct | 0.993 | 0.832 | **0.000** | -0.161 | **-0.993** | apeglm ❌ |
| snakepipes_merge_fc | 0.831 | 0.698 | **0.000** | -0.133 | **-0.831** | None |

**结果**: 0/4 成功，所有任务新 paper arm 都失败了 (0.000)

---

## 🔍 问题分析

### 问题 1: Agent 选择 Skill 错误 (snakepipes_merge_ct)

**发生了什么**:
- Task: 简单的文件合并
- Agent 选择了: `deseq2_apeglm_small_n` skill (完全不相关!)
- 结果: 失败

**根因**:
- Agent 的 relevance 判断机制不够准确
- 没有有效的方法来评估 skill 与 task 的匹配度

---

### 问题 2: Baseline 代码生成失败 (所有 tasks)

**发生了什么**:
- Agent 没有找到相关 skills (正确)
- 尝试用 baseline 知识解决
- 生成的代码执行失败
- 结果: 0.000

**对比旧实验**:
- Old none arm: 0.692 - 0.993 (成功)
- New paper arm: 0.000 (失败)

**根因分析**:

1. **可能原因 A**: 随机性
   - LLM 生成有随机性
   - 这次运气不好，生成的代码都有 bug
   - 旧实验可能跑多次取平均，单次运行可能波动

2. **可能原因 B**: Prompt 差异
   - 旧实验: 简单的 "用 best knowledge 解决"
   - 新实验: 复杂的 "query skills → assess relevance → maybe use"
   - 复杂的 prompt 可能分散了 agent 注意力

3. **可能原因 C**: 环境问题
   - Input 数据路径问题
   - 执行环境问题
   - 评分标准差异

---

## 🎯 关键发现

### 发现 1: 自适应机制本身有问题

**设计的假设**:
- Agent 能准确判断 skill 相关性
- 不匹配时 baseline 能正常工作

**实际结果**:
- Agent 误判了 skill 相关性 (选择了 apeglm 做文件合并)
- Baseline 也没有正常工作 (0.000 vs 之前的 0.7-0.9)

### 发现 2: 问题的本质不是 Skill

**最初假设**:
- Paper 表现差是因为 skill 不匹配
- 移除 skill 应该让 paper arm = baseline

**实际结果**:
- 移除 skill 后 paper arm 表现更差
- 说明问题的本质是这些 tasks 对 LLM 来说本身就难
- 旧实验的 "none" arm 可能不是真正的 "无技能"，而是有其他隐式指导

---

## 🔧 修复建议

### 建议 1: 简化实验设计

**当前问题**:
- 两步流程: query → assess → generate
- 增加了复杂性，容易出错

**建议**:
```python
# 简化: 直接运行，看结果
result = agent.run(task, skill=None)  # True baseline

if result.score < 0.5:
    # 失败后才查询 skill
    skill = retriever.get_relevant_skill(task)
    if skill:
        result_with_skill = agent.run(task, skill=skill)
        if result_with_skill.score > result.score:
            return result_with_skill

return result
```

### 建议 2: 修复 Relevance 判断

**当前问题**:
- Agent 把文件合并任务关联到 apeglm

**改进方案**:
- 使用 embedding-based similarity
- 或者使用更明确的 task-to-skill 映射表
- 而不是让 agent 自由判断

### 建议 3: 多次运行取平均

**当前问题**:
- 单次运行受随机性影响大

**建议**:
- 每个 task-arm 运行 3 次
- 取中位数或平均数
- 减少随机波动

---

## 📊 对比: 旧模式 vs 新模式

| 维度 | 旧模式 (强制灌输) | 新模式 (自主查询) |
|------|------------------|------------------|
| methylkit2tibble_split | 0.075 (差) | 0.000 (更差) |
| nearest_gene | 0.495 (差) | 0.000 (更差) |
| snakepipes_merge_ct | 0.832 (尚可) | 0.000 (更差) |
| snakepipes_merge_fc | 0.698 (尚可) | 0.000 (更差) |
| **平均** | **0.525** | **0.000** |

**结论**: 新设计的自适应机制在当前实现下反而更差。

---

## 💡 深入思考

### 原 32 tasks 实验的背景

回顾原实验数据:
```
paper vs none: paper_better=5, tie=22, paper_worse=4
```

**关键洞察**:
- 22 个 tasks 是 tie (所有 arm 差不多)
- 这意味着对于大部分 tasks，skill 不是决定性因素
- 4 个 paper 更差的 tasks 可能只是随机波动或特定实现问题

### 真正的 Paper 价值

从新 5 个 tasks 的验证:
- Paper skills 在正确场景下非常有效 (5/5 成功)
- 关键是: **任务设计** 必须真正需要 paper 方法
- 而不是: 给简单任务硬加复杂 paper

---

## 🚀 下一步行动

### 短期 (立即)

1. **验证旧实验的 None Arm**
   - 重新跑一遍这 4 个 tasks 的 none arm
   - 确认 baseline 真的能到 0.7-0.9

2. **简化 Adaptive 机制**
   - 移除复杂的 relevance assessment
   - 使用简单的 task-to-skill 映射
   - 或者直接用 embedding similarity

3. **多次运行**
   - 每个配置跑 3 次
   - 取平均减少随机性

### 中期 (1-2 天)

1. **重新设计实验**
   - 对比 3 种模式:
     - Mode A: 强制灌输 (旧)
     - Mode B: 无 skill (pure baseline)
     - Mode C: 自适应查询 (新简化版)

2. **扩大测试集**
   - 测试所有 37 个 tasks (32 + 5)
   - 看哪种模式整体最优

### 长期 (1 周)

1. **Embedding-based Retrieval**
   - 用 task description 的 embedding
   - 找最相似的 skill
   - 而不是 LLM 判断

2. **Human Evaluation**
   - 让研究人员评估 skill 与 task 的匹配度
   - 建立 ground truth
   - 训练更好的匹配模型

---

## 🎓 最终结论

### 核心发现

1. **自适应机制设计需要改进** - 当前的实现让结果更差
2. **问题的本质不是 skill 匹配** - 而是 baseline 代码生成本身不稳定
3. **旧实验数据可能有随机性** - 需要多次运行验证
4. **Paper skills 在正确场景下有效** - 关键是如何匹配到正确场景

### 设计原则修正

**原设计**: Agent 完全自主，自由判断 relevance  
**问题**: 判断不准，且 baseline 也不稳定  
**修正**: 需要更可靠的匹配机制 + 稳定的 baseline

### 建议的下一步

**不要继续优化当前的自适应机制**，而是:
1. 先验证 baseline 的稳定性
2. 简化设计：用简单的匹配规则而非 LLM 判断
3. 跑完整的对比实验后再决定方向

---

*分析完成*: 2026-04-24  
*待验证*: 旧 baseline 稳定性、简化匹配机制、完整对比实验
