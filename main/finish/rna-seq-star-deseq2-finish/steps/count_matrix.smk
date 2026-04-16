"""
Step 5: Count Matrix / 步骤5：计数矩阵

Merge per-sample gene counts from STAR into a unified count matrix and annotate with gene symbols.
将 STAR 产生的各样本基因计数合并为统一计数矩阵，并用基因符号注释。

Usage / 使用方法:
  snakemake -s steps/count_matrix.smk --configfile config_basic/config.yaml --cores 1

Input / 输入:
  results/star/*/ReadsPerGene.out.tab - Per-sample gene counts from STAR / STAR 产生的各样本基因计数

Output / 输出:
  results/counts/all.tsv - Merged count matrix with Ensembl IDs / 合并后的计数矩阵（Ensembl ID）
  results/counts/all.symbol.tsv - Count matrix with gene symbols / 计数矩阵（基因符号）
"""

configfile: "config_basic/config.yaml"


include: "common.smk"


rule all:
  """
  Target rule for count matrix step / 计数矩阵步骤的目标规则
  """
  input:
    "results/counts/all.tsv",
    "results/counts/all.symbol.tsv",


rule count_matrix:
  """
  Merge STAR gene counts into a single matrix / 合并 STAR 基因计数为单一矩阵

  读取所有样本的 ReadsPerGene.out.tab 文件（STAR 输出），
  根据链特异性选择正确的计数列，
  合并技术重复（同一生物学样本的不同 lane 求和），
  输出统一的计数矩阵。
  """
  input:
    expand(
      "results/star/{unit.sample_name}-{unit.unit_name}/ReadsPerGene.out.tab",
      unit=units.itertuples(),
    ),
  output:
    "results/counts/all.tsv",
  log:
    "logs/count-matrix.log",
  params:
    samples=units["sample_name"].tolist(),
    strand=get_strandedness(units),
  script:
    "../workflow/scripts/count-matrix.py"


rule gene_2_symbol:
  """
  Convert Ensembl gene IDs to gene symbols / 将 Ensembl 基因 ID 转换为基因符号

  Args / 参数:
    input.counts: TSV file with Ensembl IDs as row names / 以 Ensembl ID 为行名的 TSV 文件
    params.species: Bioconductor species name / Bioconductor 格式物种名

  使用 biomaRt 连接 Ensembl BioMart 数据库，
  实现多镜像重试机制确保稳定性。
  """
  input:
    counts="results/counts/all.tsv",
  output:
    symbol="results/counts/all.symbol.tsv",
  params:
    species=get_bioc_species_name(),
  log:
    "logs/gene2symbol/results/counts/all.log",
  script:
    "../workflow/scripts/gene2symbol.R"
