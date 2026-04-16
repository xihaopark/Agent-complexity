# Workflow 快速启动

## 环境要求

- Docker 与 docker-compose
- 默认已挂载 `/var/run/docker.sock`（供 `-profile docker`）
- backend 镜像已内置 Docker CLI（不依赖宿主 `/usr/bin/docker` 挂载）
- backend 运行时会按需安装 nextflow/snakemake（可通过 `.env` 配置版本）

## 构建与启动

```bash
cd renzo
cp .env.example .env   # 可选
docker-compose up --build -d
```

服务地址（Docker 主模式）：
- 前端: `http://localhost:13000`
- 后端 API: `http://localhost:18000`
- Ready: `http://localhost:18000/api/ready`

## 验证 Workflow 发现与运行时状态

```bash
curl http://localhost:18000/api/workflows
curl http://localhost:18000/api/ready
```

`/api/ready` 会返回：
- `workflow_pool` 路径检查
- nextflow/snakemake/docker-cli/docker.sock 可用性
- `ready/degraded` 结果

## 运行 Workflow 2054 (metaTAXONx)

1. 打开 `http://localhost:13000`，切换到 Workflow 面板
2. 选择 workflow `2054`
3. 上传输入文件（FASTQ 或 samplesheet）
4. 点击 `Run`

或通过 API：

```bash
# 1) 创建 run
curl -X POST "http://localhost:18000/api/workflows/run" \
  -H "Content-Type: application/json" \
  -d '{"workflow_id":"2054","params":{},"profile":"docker"}'

# 2) 轮询 run 状态
curl "http://localhost:18000/api/workflows/runs/{run_id}"
```

## 常见问题

- **docker socket 不可用**：检查 `docker-compose.yml` 是否包含  
  `- /var/run/docker.sock:/var/run/docker.sock`
- **Runner 缺失**：查看 `GET /api/ready` 中 `workflow_runtime.checks`
- **Runtime 安装关闭**：确认 `.env` 中 `WORKFLOW_RUNTIME_INSTALL=1`
- **首次运行慢**：nextflow/snakemake 依赖与流程镜像首次拉取耗时较长
