# Paper2Skills Agent 框架结构流程图

## 1. 整体架构概览

```mermaid
flowchart TB
    subgraph InputLayer["输入层"]
        UserTask["用户任务<br/>task_id + objective"]
        Registry["Task Registry<br/>32个Real Tasks"]
        Config["Agent Config<br/>GPT-4o + 温度/长度限制"]
    end

    subgraph SkillLayer["技能注入层"]
        SkillNone["none: 空技能"]
        SkillLLM["llm_plan: 任务专属计划"]
        SkillPipeline["pipeline: 源码方法提取"]
        SkillPaper["paper: 学术论文摘要<br/>Vision Adapter提取"]
    end

    subgraph PromptEngine["Prompt引擎"]
        BasePrompt["基础System Prompt"]
        SkillPlaceholder["{{SKILL_MD}}<br/>占位符替换"]
        FinalPrompt["完整渲染Prompt"]
    end

    subgraph AgentCore["Agent核心 (ldp.SimpleAgent)"]
        LLM["GPT-4o<br/>openrouter/openai/gpt-4o"]
        AgentState["Agent State<br/>工具列表+上下文"]
    end

    subgraph ToolLayer["工具层 (8个函数)"]
        RunShell["run_shell<br/>bash执行"]
        ReadFile["read_text_file<br/>文件读取"]
        WriteFile["write_text_file<br/>文件写入"]
        RunR["run_rscript<br/>R代码执行"]
        ListDir["list_workdir<br/>目录列表"]
        WritePlan["write_plan<br/>计划写入"]
        CheckProgress["check_progress<br/>进度检查"]
        SubmitDone["submit_done<br/>任务提交"]
    end

    subgraph EnvLayer["环境层 (RTaskEvalEnv)"]
        WorkDir["workspace/<br/>隔离工作目录"]
        InputData["input/<br/>合成输入数据"]
        OutputDir["output/<br/>结果输出"]
        Objective["OBJECTIVE.md<br/>任务目标"]
        StateMgmt["状态管理<br/>done/truncated/reward"]
    end

    subgraph OutputLayer["输出层"]
        Trajectory["trajectory.jsonl<br/>完整执行轨迹"]
        Metadata["metadata.json<br/>运行元数据"]
        Result["output/<br/>任务结果文件"]
    end

    subgraph EvalLayer["评估层 (V2.1)"]
        GroundTruth["real_ground_truth/<br/>参考输出"]
        Evaluator["evaluate_real_run_v2.1<br/>连续评分评估器"]
        Score["overall_score<br/>0.3*process + 0.7*files"]
        Verdict["verdict<br/>pass/partial/fail"]
    end

    %% 数据流
    UserTask --> Registry
    Registry --> Config
    Config --> SkillLayer
    
    SkillNone & SkillLLM & SkillPipeline & SkillPaper --> PromptEngine
    
    BasePrompt --> SkillPlaceholder
    SkillPlaceholder --> FinalPrompt
    FinalPrompt --> LLM
    
    LLM --> AgentState
    AgentState --> ToolLayer
    
    ToolLayer --> EnvLayer
    RunShell & ReadFile & WriteFile & RunR & ListDir & WritePlan & CheckProgress & SubmitDone --> WorkDir
    
    WorkDir --> InputData
    WorkDir --> OutputDir
    WorkDir --> Objective
    WorkDir --> StateMgmt
    
    OutputDir --> Result
    StateMgmt --> Trajectory
    StateMgmt --> Metadata
    
    Result --> EvalLayer
    GroundTruth --> Evaluator
    Trajectory --> Evaluator
    Evaluator --> Score
    Score --> Verdict

    %% 样式
    style SkillPaper fill:#e1f5fe,stroke:#01579b,stroke-width:3px
    style LLM fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style Evaluator fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    style Verdict fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
```

---

## 2. Rollout 执行流程

```mermaid
sequenceDiagram
    participant User as 用户
    participant Runner as batch_runner
    participant Agent as SimpleAgent
    participant Env as RTaskEvalEnv
    participant Tools as 工具函数
    participant FS as 文件系统

    User->>Runner: 启动实验 (4 arms × 32 tasks)
    
    loop 每个 Task
        Runner->>Runner: 复制workspace
        Runner->>Env: reset()
        Env->>FS: 读取OBJECTIVE.md
        Env->>FS: 列出input/目录
        Env->>Agent: 返回初始观察 + 工具列表
        
        Agent->>Agent: init_state(tools)
        
        loop max_steps (最多15步)
            Agent->>Agent: get_asv(state, observation)
            Agent->>Agent: LLM生成动作
            Agent->>Env: step(action)
            
            alt run_rscript
                Env->>Tools: run_rscript(code)
                Tools->>FS: 写入临时R脚本
                Tools->>FS: Rscript -e 执行
                FS->>Tools: 返回stdout/stderr
                Tools->>Env: 返回执行结果
            else write_text_file
                Env->>Tools: write_text_file(path, content)
                Tools->>FS: 写入文件
                Tools->>Env: 返回确认
            else read_text_file
                Env->>Tools: read_text_file(path)
                Tools->>FS: 读取文件
                Tools->>Env: 返回内容
            else submit_done
                Env->>Env: 检查success_artifact
                Env->>Agent: 返回done=true
            end
            
            Env->>Agent: 返回(next_obs, reward, done, truncated)
            Agent->>Agent: 记录transition
            
            opt done=true or truncated=true
                Agent->>Runner: 结束rollout
            end
        end
        
        Runner->>FS: 保存trajectory.jsonl
        Runner->>FS: 保存metadata.json
    end
    
    Runner->>User: 32个tasks完成
```

---

## 3. Skill注入对比 (4 Arms)

```mermaid
flowchart LR
    subgraph Base["基础Prompt"]
        BP1["你解决R-centric分析任务"]
        BP2["可用工具: run_shell, run_rscript..."]
        BP3["Prefer R for numeric/statistical work"]
    end

    subgraph NoneArm["none arm"]
        N1["{{SKILL_MD}} = ''"]
        N2["仅基础Prompt"]
    end

    subgraph LLMPlanArm["llm_plan arm"]
        LP1["OBJECTIVE.md分析"]
        LP2["GPT-4o生成计划"]
        LP3["1. 读取数据<br/>2. 过滤ERCC<br/>3. DESeq2分析"]
    end

    subgraph PipelineArm["pipeline arm"]
        PA1["workflow源码分析"]
        PA2["scripts/deseq_analysis.r"]
        PA3["提取方法: DESeqDataSetFromMatrix<br/>design formula<br/>lfcThreshold"]
    end

    subgraph PaperArm["paper arm ⭐"]
        PP1["PDF论文提取"]
        PP2["Vision Adapter<br/>gpt-4o-vision"]
        PP3["方法摘要:<br/>Alevin pipeline流程<br/>关键参数<br/>最佳实践"]
    end

    Base --> NoneArm & LLMPlanArm & PipelineArm & PaperArm
    
    style PaperArm fill:#e1f5fe,stroke:#01579b,stroke-width:3px
```

---

## 4. 评估器V2.1评分流程

```mermaid
flowchart TD
    subgraph Input["评估输入"]
        Traj["trajectory.jsonl<br/>执行轨迹"]
        Meta["metadata.json<br/>运行配置"]
        Output["workspace/output/<br/>Agent输出"]
        Ref["real_ground_truth/<br/>参考输出"]
    end

    subgraph ProcessSignals["流程信号评估"]
        S1["tool_calls_executed_meaningful<br/>>2次非平凡调用"]
        S2["rscript_invoked_and_exited_zero"]
        S3["submit_done_called"]
        S4["outputs_dir_nonempty_and_valid"]
        PM["process_mean = mean(4 signals)"]
    end

    subgraph FileEvaluation["逐文件评估"]
        F1["byte_identical?<br/>SHA256对比"]
        F2["normalized_text_equal?<br/>BOM/CRLF处理"]
        F3["normalized_table_equal?<br/>canonical TSV"]
        F4["tabular_tolerance<br/>连续评分 V2.1"]
        F5["rds_semantic<br/>S4对象提取"]
        FC["process_credit<br/>0.25保底"]
    end

    subgraph TabularDetails["Tabular评分细节 (V2.1改进)"]
        T1["列对齐<br/>by_name / by_position"]
        T2["行fingerprint<br/>数值容差桶"]
        T3["multiset匹配<br/>row_match_fraction"]
        T4["cell级对比<br/>cell_match_fraction"]
        T5["V2.1: blended = max(eff, 0.85*cell)"]
        T6["V2.1: 放宽col_penalty<br/>超集模式×0.95"]
    end

    subgraph FinalScore["最终评分"]
        FM["file_scores_mean<br/>所有文件平均分"]
        OS["overall_score = 0.3*process + 0.7*files"]
        VD["verdict<br/>pass≥0.9<br/>partial≥0.6<br/>fail<0.3"]
    end

    Traj --> ProcessSignals
    Meta --> ProcessSignals
    Output --> FileEvaluation
    Ref --> FileEvaluation
    
    F4 --> TabularDetails
    
    S1 & S2 & S3 & S4 --> PM
    F1 & F2 & F3 & F4 & F5 & FC --> FM
    
    PM & FM --> OS
    OS --> VD

    style TabularDetails fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style VD fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
```

---

## 5. 数据流完整链路

```mermaid
flowchart LR
    subgraph Source["源数据层"]
        Workflow["workflow_candidates/<br/>145个真实workflow"]
        Scripts["*.R / *.Rmd<br/>真实R脚本"]
        PaperPDF["literature/<br/>学术论文PDF"]
    end

    subgraph TaskGen["Task生成层"]
        Builder["build_real_r_tasks.py"]
        Synthetic["合成输入数据<br/>seeded random"]
        GroundTruth["运行源脚本<br/>生成reference"]
    end

    subgraph TaskStorage["Task存储"]
        Registry["registry.real.json<br/>32 tasks"]
        Workspace["tasks/real/<br/>workspace/"]
        GT["tasks/real_ground_truth/<br/>隔离存储"]
    end

    subgraph Execution["执行层 (4 Arms)"]
        Batch["batch_runner.py"]
        Agent["SimpleAgent<br/>GPT-4o"]
        Env["RTaskEvalEnv"]
    end

    subgraph Results["结果层"]
        TrajDir["runs/batch_*/<br/>trajectory.jsonl"]
        EvalV2["_evaluations/<br/>V2评分"]
        EvalV21["_evaluations_v21/<br/>V2.1评分"]
    end

    subgraph Analysis["分析层"]
        Compare["4臂对比分析"]
        Report["技术报告<br/>FINAL_4ARM_COMPLETE.md"]
    end

    Workflow --> Scripts
    Scripts --> Builder
    PaperPDF --> Builder
    
    Builder --> Synthetic
    Builder --> GroundTruth
    
    Synthetic --> Workspace
    GroundTruth --> GT
    Builder --> Registry
    
    Registry --> Batch
    Workspace --> Batch
    GT -.-> Batch
    
    Batch --> Agent
    Agent --> Env
    Env --> TrajDir
    
    TrajDir --> EvalV2
    TrajDir --> EvalV21
    GT --> EvalV21
    
    EvalV21 --> Compare
    Compare --> Report

    style PaperPDF fill:#fff3e0,stroke:#e65100
    style EvalV21 fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style Report fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
```

---

## 6. Paper Arm 优势机制详解

```mermaid
flowchart TD
    subgraph Problem["无Skill时的常见问题"]
        P1["不知道用哪个R包<br/>尝试错误package"]
        P2["参数选择错误<br/>默认参数不适用"]
        P3["处理顺序错误<br/>先归一化后过滤"]
        P4["边界条件忽略<br/>忘记处理ERCC"]
        P5["反复试错<br/>infinite debug loop"]
    end

    subgraph PaperSkill["Paper Skill提供"]
        S1["方法框架<br/>'Use tximport for Alevin'"]
        S2["关键参数提醒<br/>'--keepDuplicates flag'"]
        S3["最佳实践顺序<br/>'Whitelist → Map → Deduplicate → Count'"]
        S4["陷阱预警<br/>'Memory usage for multi-threading'"]
    end

    subgraph Result["结果差异"]
        R1["直接正确执行<br/>6步完成"]
        R2["无Rscript错误<br/>rscript_err=0"]
        R3["无重试<br/>writes_after_first=0"]
        R4["高细胞匹配率<br/>100% cells match"]
    end

    P1 & P2 & P3 & P4 & P5 --> PaperSkill
    PaperSkill --> R1 & R2 & R3 & R4

    style PaperSkill fill:#e1f5fe,stroke:#01579b,stroke-width:3px
    style Result fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
```

---

## 图例说明

| 颜色 | 含义 |
|------|------|
| 🟦 蓝色高亮 | Paper Arm / V2.1评估器 (核心改进点) |
| 🟧 橙色 | GPT-4o LLM |
| 🟩 绿色 | 成功/Pass |
| 🟪 紫色 | 评估/分析 |

---

*图表生成于 2024-04-17*  
*对应实验: sweep_v3_paper_final (32 tasks, GPT-4o, V2.1评估)*
