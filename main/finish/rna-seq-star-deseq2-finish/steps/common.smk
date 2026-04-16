"""
Common module / 共享模块

Provides shared configuration loading and helper functions for all step scripts.
提供所有步骤脚本共享的配置加载和辅助函数。

This file should be included by each step Snakefile via `include: "common.smk"`.
各步骤 Snakefile 通过 `include: "common.smk"` 引入本文件。
"""

import glob
import pandas as pd


# ── Load sample and unit metadata / 加载样本和测序单元元数据 ──────────────
# 读取 samples.tsv，以 sample_name 为索引
samples = (
  pd.read_csv(config["samples"], sep="\t", dtype={"sample_name": str})
  .set_index("sample_name", drop=False)
  .sort_index()
)

# 读取 units.tsv，以 (sample_name, unit_name) 为双层索引
units = (
  pd.read_csv(config["units"], sep="\t", dtype={"sample_name": str, "unit_name": str})
  .set_index(["sample_name", "unit_name"], drop=False)
  .sort_index()
)


# ── Wildcard constraints / 通配符约束 ────────────────────────────────────
# 限制 sample 和 unit 通配符只能匹配已知的值，避免歧义
wildcard_constraints:
  sample="|".join(samples["sample_name"]),
  unit="|".join(units["unit_name"]),


# ── Helper functions / 辅助函数 ──────────────────────────────────────────

def get_units_fastqs(wildcards):
  """
  Get FASTQ file paths for a given sample-unit pair / 获取指定样本-单元的 FASTQ 文件路径

  Args / 参数:
    wildcards: Snakemake wildcards containing sample and unit / 包含 sample 和 unit 的通配符对象

  Returns / 返回值:
    list[str]: FASTQ file path(s) / FASTQ 文件路径列表

  根据 units.tsv 中的配置，返回本地文件路径或 SRA 下载路径。
  """
  u = units.loc[(wildcards.sample, wildcards.unit)]
  if pd.isna(u["fq1"]):
    # SRA sample (always paired-end for now)
    accession = u["sra"]
    return expand(
      "sra/{accession}_{read}.fastq",
      accession=accession,
      read=["1", "2"],
    )
  if not is_paired_end(wildcards.sample):
    return [u["fq1"]]
  else:
    return [u["fq1"], u["fq2"]]


def is_paired_end(sample):
  """
  Check if a sample is paired-end sequencing / 判断样本是否为双端测序

  Args / 参数:
    sample (str): Sample name / 样本名称

  Returns / 返回值:
    bool: True if paired-end, False if single-end / 双端返回 True，单端返回 False

  通过检查 units.tsv 中 fq2 和 sra 列是否有值来判断。
  同一个样本的所有 unit 必须同为双端或同为单端，否则抛出异常。
  """
  sample_units = units.loc[sample]
  fq2_null = sample_units["fq2"].isnull()
  sra_null = sample_units["sra"].isnull()
  paired = ~fq2_null | ~sra_null
  all_paired = paired.all()
  all_single = (~paired).all()
  assert (
    all_single or all_paired
  ), "invalid units for sample {}, must be all paired end or all single end".format(
    sample
  )
  return all_paired


def get_fq(wildcards):
  """
  Get FASTQ input files for alignment / 获取用于比对的 FASTQ 输入文件

  Args / 参数:
    wildcards: Snakemake wildcards containing sample and unit / 包含 sample 和 unit 的通配符对象

  Returns / 返回值:
    dict[str, str]: Dict with keys fq1 (and optionally fq2) / 包含 fq1（和可选的 fq2）的字典

  根据 config 中 trimming 是否激活，自动选择使用修剪后数据或原始数据。
  """
  if config["trimming"]["activate"]:
    # 使用 fastp 修剪后的数据
    if is_paired_end(wildcards.sample):
      return dict(
        zip(
          ["fq1", "fq2"],
          expand(
            "results/trimmed/{sample}/{sample}-{unit}_{read}.fastq.gz",
            read=["R1", "R2"],
            **wildcards,
          ),
        )
      )
    return {
      "fq1": "results/trimmed/{sample}/{sample}-{unit}_single.fastq.gz".format(
        **wildcards
      )
    }
  else:
    # 使用原始 reads
    fqs = get_units_fastqs(wildcards)
    if len(fqs) == 1:
      return {"fq1": f"{fqs[0]}"}
    elif len(fqs) == 2:
      return {"fq1": f"{fqs[0]}", "fq2": f"{fqs[1]}"}
    else:
      raise ValueError(f"Expected one or two fastq file paths, but got: {fqs}")


def get_strandedness(units):
  """
  Get strandedness information from units table / 从 units 表中获取链特异性信息

  Args / 参数:
    units (DataFrame): Units metadata table / 测序单元元数据表

  Returns / 返回值:
    list[str]: Strandedness values for each unit / 每个 unit 的链特异性值

  如果 units.tsv 中没有 strandedness 列，则默认为 "none"（非链特异性）。
  """
  if "strandedness" in units.columns:
    return units["strandedness"].tolist()
  else:
    strand_list = ["none"]
    return strand_list * units.shape[0]


def get_deseq2_threads(wildcards=None):
  """
  Determine thread count for DESeq2 analysis / 动态确定 DESeq2 分析的线程数

  Args / 参数:
    wildcards: Optional Snakemake wildcards / 可选的通配符对象

  Returns / 返回值:
    int: Number of threads to use / 使用的线程数

  当样本数 < 100 或对比系数 < 10 时使用单线程，否则使用 6 线程。
  参考：https://twitter.com/mikelove/status/918770188568363008
  """
  few_coeffs = False if wildcards is None else len(get_contrast(wildcards)) < 10
  return 1 if len(samples) < 100 or few_coeffs else 6


def get_bioc_species_name():
  """
  Convert Ensembl species name to Bioconductor format / 将 Ensembl 物种名转为 Bioconductor 格式

  Returns / 返回值:
    str: Bioconductor species name / Bioconductor 格式物种名（如 "Hsapiens"）

  取物种名首字母 + 下划线后的亚种名，例如 "homo_sapiens" → "Hsapiens"。
  """
  first_letter = config["ref"]["species"][0]
  subspecies = config["ref"]["species"].split("_")[1]
  return first_letter + subspecies


def get_contrast(wildcards):
  """
  Get contrast definition from config / 从配置中获取对比定义

  Args / 参数:
    wildcards: Snakemake wildcards containing contrast name / 包含 contrast 名称的通配符对象

  Returns / 返回值:
    dict: Contrast definition / 对比定义字典

  返回 config["diffexp"]["contrasts"] 中指定 contrast 的定义。
  """
  return config["diffexp"]["contrasts"][wildcards.contrast]
