"""
Step 6: Differential Expression Analysis / 步骤6：差异表达分析

Perform differential expression analysis using DESeq2.
使用 DESeq2 执行差异表达分析。

Usage / 使用方法:
  snakemake -s steps/differential_expression.smk --configfile config_basic/config.yaml --cores 8

Input / 输入:
  results/counts/all.tsv - Merged count matrix from step 5 / 步骤5产生的合并计数矩阵

Output / 输出:
  results/deseq2/all.rds - Serialized DESeq2 dataset object / 序列化的 DESeq2 数据集对象
  results/deseq2/normcounts.tsv - Normalized count matrix / 标准化计数矩阵
  results/deseq2/normcounts.symbol.tsv - Normalized counts with gene symbols / 标准化计数（基因符号）
  results/diffexp/ - Differential expression results and MA-plots / 差异表达结果和 MA 图
"""

configfile: "config_basic/config.yaml"


include: "common.smk"


rule all:
  """
  Target rule for differential expression step / 差异表达步骤的目标规则

  收集 DESeq2 初始化输出、标准化计数、差异表达结果及其基因符号注释版本。
  """
  input:
    "results/deseq2/all.rds",
    "results/deseq2/normcounts.symbol.tsv",
    expand(
      "results/diffexp/{contrast}.diffexp.symbol.tsv",
      contrast=config["diffexp"]["contrasts"],
    ),
    expand(
      "results/diffexp/{contrast}.ma-plot.svg",
      contrast=config["diffexp"]["contrasts"],
    ),


rule deseq2_init:
  """
  Initialize DESeq2 analysis / 初始化 DESeq2 分析

  1. 读取计数矩阵和样本元数据
  2. 设置变量的基准水平（base level）
  3. 构建设计公式（自动或手动指定）
  4. 创建 DESeqDataSet 对象并运行 DESeq()
  5. 过滤低表达基因（rowSums > 1）
  6. 导出标准化计数和序列化的 DDS 对象
  """
  input:
    counts="results/counts/all.tsv",
  output:
    "results/deseq2/all.rds",
    "results/deseq2/normcounts.tsv",
  log:
    "logs/deseq2/init.log",
  threads: get_deseq2_threads()
  script:
    "../workflow/scripts/deseq2-init.R"


rule deseq2:
  """
  Perform contrast-specific differential expression / 执行特定对比的差异表达分析

  Args / 参数:
    input: DESeq2 dataset object (all.rds) / DESeq2 数据集对象
    params.contrast: Contrast definition from config / 来自配置的对比定义

  对指定的对比（contrast）提取差异表达结果，
  使用 ashr 方法缩减 log-fold-change，
  生成差异基因表和 MA-plot 可视化图。
  """
  input:
    "results/deseq2/all.rds",
  output:
    table="results/diffexp/{contrast}.diffexp.tsv",
    ma_plot="results/diffexp/{contrast}.ma-plot.svg",
  params:
    contrast=get_contrast,
  log:
    "logs/deseq2/{contrast}.diffexp.log",
  threads: get_deseq2_threads()
  script:
    "../workflow/scripts/deseq2.R"


rule gene_2_symbol_normcounts:
  """
  Convert normalized count IDs to gene symbols / 将标准化计数的基因 ID 转换为基因符号

  对 DESeq2 输出的标准化计数矩阵进行基因符号注释。
  """
  input:
    counts="results/deseq2/normcounts.tsv",
  output:
    symbol="results/deseq2/normcounts.symbol.tsv",
  params:
    species=get_bioc_species_name(),
  log:
    "logs/gene2symbol/results/deseq2/normcounts.log",
  script:
    "../workflow/scripts/gene2symbol.R"


rule gene_2_symbol_diffexp:
  """
  Convert differential expression result IDs to gene symbols / 将差异表达结果的基因 ID 转换为基因符号

  对每个 contrast 的差异表达结果进行基因符号注释。
  """
  input:
    counts="results/diffexp/{contrast}.diffexp.tsv",
  output:
    symbol="results/diffexp/{contrast}.diffexp.symbol.tsv",
  params:
    species=get_bioc_species_name(),
  log:
    "logs/gene2symbol/results/diffexp/{contrast}.diffexp.log",
  script:
    "../workflow/scripts/gene2symbol.R"
