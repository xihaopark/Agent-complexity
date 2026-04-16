"""
Step 7: PCA Visualization / 步骤7：PCA 可视化

Generate PCA plots for sample clustering visualization.
生成 PCA 图用于样本聚类可视化。

Usage / 使用方法:
  snakemake -s steps/pca_plot.smk --configfile config_basic/config.yaml --cores 1

Input / 输入:
  results/deseq2/all.rds - DESeq2 dataset object from step 6 / 步骤6产生的 DESeq2 数据集对象

Output / 输出:
  results/pca.{variable}.svg - PCA plot colored by each variable / 按各变量着色的 PCA 图
"""

configfile: "config_basic/config.yaml"


include: "common.smk"


def get_pca_variables():
  """
  Collect all variables for PCA plotting / 收集所有用于 PCA 绘图的变量

  Returns / 返回值:
    list[str]: Variable names for PCA / PCA 变量名列表

  合并 variables_of_interest、batch_effects 和 pca.labels 中的变量。
  """
  pca_variables = list(config["diffexp"]["variables_of_interest"])
  if config["diffexp"]["batch_effects"]:
    pca_variables.extend(config["diffexp"]["batch_effects"])
  if config["pca"]["labels"]:
    pca_variables.extend(config["pca"]["labels"])
  return pca_variables


rule all:
  """
  Target rule for PCA visualization step / PCA 可视化步骤的目标规则
  """
  input:
    expand("results/pca.{variable}.svg", variable=get_pca_variables()),


rule pca:
  """
  Generate PCA plot for a given variable / 为指定变量生成 PCA 图

  Args / 参数:
    input: DESeq2 dataset object (all.rds) / DESeq2 数据集对象
    wildcards.variable: Column name to color samples by / 用于着色的样本元数据列名

  对 DESeq2 数据集执行 rlog 转换后进行 PCA 分析，
  按指定变量着色样本点，输出 SVG 矢量图。
  """
  input:
    "results/deseq2/all.rds",
  output:
    "results/pca.{variable}.svg",
  log:
    "logs/pca.{variable}.log",
  script:
    "../workflow/scripts/plot-pca.R"
