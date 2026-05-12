# Agent 执行方法论

## 核心循环：观察 → 思考 → 行动

```mermaid
flowchart TD
    Start([开始]) --> Load["加载Skill<br/>Paper/Plan/Pipeline/None"]
    Load --> Reset["初始化环境"]
    Reset --> Observe["观察<br/>读取任务目标+输入数据"]
    Observe --> Plan["写计划<br/>write_plan"]
    Plan --> Loop

    subgraph Loop["执行循环"]
        Think["思考<br/>LLM生成下一步"]
        Act["行动<br/>选择工具"]
        Exec["执行<br/>run_rscript/read_file/write_file..."]
        Feedback["反馈<br/>观察结果"]
        Check{"完成?"}
    end

    Submit["提交<br/>submit_done"]
    End([结束])

    Think --> Act --> Exec --> Feedback --> Check
    Check -->|No| Think
    Check -->|Yes| Submit --> End

    style Loop fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style Think fill:#fff3e0,stroke:#e65100
    style Submit fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
```

---

## 四臂差异：Skill如何影响行动

```mermaid
flowchart LR
    Task["Task: DESeq2分析"] --> Arms

    subgraph Arms["四臂对比"]
        N["❌ none<br/>无Skill<br/>试错猜参数<br/>反复调试"] 
        L["⚠️ llm_plan<br/>有计划步骤<br/>缺领域知识"]
        P["⚠️ pipeline<br/>复制原脚本<br/>可能过拟合"]
        PP["✅ paper<br/>方法框架<br/>关键参数<br/>一步到位"]
    end

    style PP fill:#e1f5fe,stroke:#01579b,stroke-width:3px
```

---

## 关键洞察：为什么Paper更强

```mermaid
flowchart TD
    Problem["无Skill时的问题<br/>不知道用哪个包<br/>参数猜错<br/>边界条件遗漏"] --> Skill["Paper Skill<br/>提供方法框架<br/>关键参数提醒<br/>最佳实践"]
    Skill --> Result["结果<br/>6步完成<br/>0错误<br/>100%匹配"]

    style Skill fill:#e1f5fe,stroke:#01579b,stroke-width:3px
    style Result fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
```

---

## 典型轨迹对比

```mermaid
flowchart LR
    subgraph Paper["Paper Arm"]
        P1["写计划"] --> P2["读数据"] --> P3["执行R代码"] --> P4["完成✅"]
    end

    subgraph None["None Arm"]
        N1["尝试R代码❌"] --> N2["试错..."] --> N3["调试循环"] --> N4["失败/截断❌"]
    end

    style P4 fill:#c8e6c9,stroke:#2e7d32
    style N4 fill:#ffcdd2,stroke:#c62828
```

---

## 一句话总结

> **Agent的方法论是"观察→思考→行动"循环，Skill决定思考质量。Paper Skill提供学术论文的方法论框架，使Agent一步到位正确执行。**

---

## 补充：详细执行流程

### Step-by-Step 执行示例 (chipseq_plot_macs_qc)

```mermaid
sequenceDiagram
    participant A as Agent
    participant E as Environment
    participant T as Tools
    participant F as 文件系统

    Note over A: 初始状态<br/>已加载Paper Skill

    A->>E: reset()
    E->>F: 读取OBJECTIVE.md
    E->>F: 列出input/目录
    E->>A: 返回观察: 任务目标+文件列表

    A->>A: LLM思考: "需要读取MACS2输出并提取QC统计"
    A->>T: write_plan("1.读取peaks.xls 2.提取QC统计 3.输出tsv")
    T->>F: 写入.plan.md
    T->>A: 确认

    A->>A: LLM思考: "现在执行第1步:读取输入"
    A->>T: read_text_file("input/peaks.xls")
    T->>F: 读取文件
    T->>A: 返回文件内容

    A->>A: LLM思考: "数据已读取，现在用R处理<br/>根据Paper Skill，MACS2输出格式是..."
    A->>T: run_rscript("library(dplyr); peaks <- read.table(...)")
    T->>F: 执行R代码
    F->>T: 返回stdout+stderr
    T->>A: exit=0 (成功)

    A->>T: list_workdir()
    T->>F: 检查output/
    T->>A: 返回文件列表

    A->>A: LLM思考: "输出已生成，检查完成条件"
    A->>T: submit_done(success=true)
    T->>E: 设置done=true
    T->>A: 返回完成确认

    Note over A: 完成<br/>共6步
```

---

## 补充：Skill注入机制

```mermaid
flowchart LR
    subgraph Prompt["System Prompt构造"]
        Base["基础指令"]
        BaseText["你解决R-centric分析任务...<br/>可用工具: run_shell, run_rscript..."]
    end

    subgraph SkillInsert["Skill插入"]
        Placeholder["{{SKILL_MD}}"]
        PaperContent["Paper Skill内容<br/>方法: Alevin流程<br/>参数: --keepDuplicates<br/>注意: 内存使用..."]
    end

    subgraph Final["最终Prompt"]
        F1["基础指令"]
        F2["---"]
        F3["Paper Skill内容"]
    end

    Base --> Placeholder
    BaseText --> PaperContent
    Placeholder --> F2
    PaperContent --> F3

    style PaperContent fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style F3 fill:#e1f5fe,stroke:#01579b,stroke-width:2px
```

---

## 补充：失败模式对比

```mermaid
flowchart TD
    subgraph CommonTask["共同任务: methylKit分析"]
        T["输入: .bam文件<br/>目标: 生成甲基化统计"]
    end

    subgraph SuccessPath["Paper Arm ✅"]
        S1["Step1: 读取Paper Skill<br/>了解methylKit流程"]
        S2["Step2: methRead正确参数<br/>treatment=c(1,1,0,0)"]
        S3["Step3: unite()过滤"]
        S4["Step4: 完成✅"]
    end

    subgraph FailPath["None Arm ❌"]
        F1["Step1: 猜测参数<br/>treatment=c(0,0,0,0)❌"]
        F2["Step2: 错误<br/>不知道需要sample.id"]
        F3["Step3-14: 反复试错<br/>各种参数组合"]
        F4["Step15: 失败/截断❌"]
    end

    T --> SuccessPath
    T --> FailPath

    style SuccessPath fill:#e8f5e9,stroke:#1b5e20
    style FailPath fill:#ffebee,stroke:#c62828
```

---

## 补充：数据流全景

```mermaid
flowchart LR
    Input["输入<br/>Task Registry + Skill"] --> Agent["Agent<br/>LLM + Prompt"]
    Agent --> Action["行动<br/>选择工具"]
    Action --> Exec["执行<br/>run_rscript等"]
    Exec --> Env["环境<br/>workspace/"]
    Env --> Output["输出<br/>result文件"]
    Output --> Eval["评估<br/>vs Ground Truth"]
    Eval --> Score["分数<br/>overall_score"]

    style Agent fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style Score fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
```
