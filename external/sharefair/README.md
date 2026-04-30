# ShareFAIR Copalink（子模块）

本目录通过 **git submodule** 挂载 LIRIS GitLab 上的两个仓库：

| 子模块路径 | 上游 |
|------------|------|
| `copalink/` | https://gitlab.liris.cnrs.fr/sharefair/copalink |
| `copalink-experiments/` | https://gitlab.liris.cnrs.fr/sharefair/copalink-experiments |

## 克隆本仓库后拉取子模块

在仓库根目录执行：

```bash
git submodule update --init --recursive
```

仅更新这两个子模块：

```bash
git submodule update --init external/sharefair/copalink external/sharefair/copalink-experiments
```

若 GitLab 仓库为私有，需配置对该域名的访问（HTTPS 凭据或 SSH remote 改写），参见 GitLab 文档。
