# LDP R-Task Eval Environment Setup

> 隔离虚拟环境配置，用于 Paper2Skills 实验（含 discovery mode）。

---

## 快速激活

```bash
cd main/paper_primary_benchmark/ldp_r_task_eval

# 激活虚拟环境
source .venv-ldp-r-task/bin/activate

# 验证
python3 -c "from aviary.core import Environment; from ldp.agent import Agent; print('OK')"
```

---

## 环境详情

| 项目 | 设置 |
|------|------|
| Python | 3.12.9 |
| 位置 | `main/paper_primary_benchmark/ldp_r_task_eval/.venv-ldp-r-task/` |
| fhaviary | >=0.18.0 |
| ldp | >=0.26.0 |
| pydantic | >=2.0 |
| PyYAML | >=6.0 |

---

## 安装步骤（已执行）

```bash
# 1. 创建虚拟环境
python3.12 -m venv .venv-ldp-r-task

# 2. 激活
source .venv-ldp-r-task/bin/activate

# 3. 安装依赖
pip install "fhaviary>=0.18.0" "ldp>=0.26.0" "pydantic>=2.0" "PyYAML>=6.0"
```

---

## 运行实验

### 激活后运行（所有 runner 都需要在 venv 中）

```bash
# 激活环境
source .venv-ldp-r-task/bin/activate

# 运行绑定模式实验
python batch_runner.py \
    --registry r_tasks/registry.paper_sensitive_v1.json \
    --config config/paper_sweep_15steps.yaml \
    --skill-source paper \
    --run-id paper_binding_test

# 运行检索模式实验（discovery mode）
python discovery_runner.py \
    --registry r_tasks/registry.paper_sensitive_v1.json \
    --config config/paper_discovery_mode.yaml \
    --run-id paper_discovery_test
```

---

## 验证环境

```bash
source .venv-ldp-r-task/bin/activate

# 测试核心导入
python3 -c "
from aviary.core import Environment, Tool
from ldp.agent.simple_agent import SimpleAgent
from paper_primary_benchmark.ldp_r_task_eval.r_task_env import RTaskEvalEnv
print('✓ All core imports OK')
"

# 测试 discovery 工具
python3 -c "
import sys
sys.path.insert(0, '../../../paperskills/library')
from discovery_tool import DISCOVERY_TOOLS
print('✓ Discovery tools OK:', list(DISCOVERY_TOOLS.keys()))
"
```

---

## 注意事项

1. **每次新终端都需要激活**: `source .venv-ldp-r-task/bin/activate`

2. **OpenRouter API Key**: 确保 `openrouterkey.txt` 在仓库根目录

3. **Python 版本**: 必须使用 3.12（ldp 依赖要求）

4. **不要提交 venv**: `.venv-ldp-r-task/` 已在 `.gitignore`

---

## 故障排除

### ImportError: No module named 'aviary'

```bash
# 未激活虚拟环境
cd main/paper_primary_benchmark/ldp_r_task_eval
source .venv-ldp-r-task/bin/activate
```

### 版本不匹配

```bash
# 升级依赖
source .venv-ldp-r-task/bin/activate
pip install --upgrade "fhaviary>=0.18.0" "ldp>=0.26.0"
```

### Discovery tools 找不到

```bash
# 确保在项目根目录运行，或设置正确的 PYTHONPATH
cd /home/park/Agent-complexity
source main/paper_primary_benchmark/ldp_r_task_eval/.venv-ldp-r-task/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

---

*Setup Date: 2026-05-01*  
*Status: ✅ Ready for experiments*
