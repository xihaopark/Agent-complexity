"""
Step 2: Alignment / 步骤2：序列比对

Align trimmed reads to the reference genome using STAR aligner.
使用 STAR 比对器将修剪后的 reads 比对到参考基因组。

Usage / 使用方法:
  snakemake -s steps/alignment.smk --configfile config_basic/config.yaml --cores 8

Input / 输入:
  results/trimmed/ - Trimmed FASTQ files from step 1 / 步骤1产生的修剪后 FASTQ 文件
  resources/star_genome/ - Pre-built STAR genome index / 预构建的 STAR 基因组索引

Output / 输出:
  results/star/{sample}-{unit}/ - BAM files, gene counts, and alignment logs / BAM 文件、基因计数和比对日志
"""

configfile: "config_basic/config.yaml"


include: "common.smk"


rule all:
  """
  Target rule for alignment step / 序列比对步骤的目标规则

  收集所有样本的 BAM 文件和 ReadsPerGene 计数作为目标输出。
  """
  input:
    expand(
      "results/star/{unit.sample_name}-{unit.unit_name}/Aligned.sortedByCoord.out.bam",
      unit=units.itertuples(),
    ),
    expand(
      "results/star/{unit.sample_name}-{unit.unit_name}/ReadsPerGene.out.tab",
      unit=units.itertuples(),
    ),


rule star_index:
  """
  Build STAR genome index / 构建 STAR 基因组索引

  Args / 参数:
    input.fasta: Reference genome FASTA / 参考基因组 FASTA 文件
    input.gtf: Gene annotation GTF / 基因注释 GTF 文件

  如果 resources/star_genome/ 已存在则自动跳过。
  使用多线程加速索引构建过程。
  """
  input:
    fasta="resources/genome.fasta",
    gtf="resources/genome.gtf",
  output:
    directory("resources/star_genome"),
  log:
    "logs/star_index_genome.log",
  params:
    extra=config.get("params", {}).get("star", {}).get("index", ""),
  threads: 4
  shell:
    "STAR --runMode genomeGenerate"
    " --runThreadN {threads}"
    " --genomeFastaFiles {input.fasta}"
    " --sjdbGTFfile {input.gtf}"
    " --genomeDir {output}"
    " {params.extra}"
    " > {log} 2>&1"


rule star_align:
  """
  Align reads to genome with STAR / 使用 STAR 将 reads 比对到基因组

  Args / 参数:
    input.fq1, input.fq2: Trimmed FASTQ files / 修剪后的 FASTQ 文件
    input.idx: STAR genome index directory / STAR 基因组索引目录
    input.gtf: Gene annotation GTF / 基因注释 GTF 文件

  同时执行比对和基因定量（--quantMode GeneCounts），
  输出按坐标排序的 BAM 文件和每基因读段计数表。
  """
  input:
    unpack(get_fq),
    idx="resources/star_genome",
    gtf="resources/genome.gtf",
  output:
    aln="results/star/{sample}-{unit}/Aligned.sortedByCoord.out.bam",
    reads_per_gene="results/star/{sample}-{unit}/ReadsPerGene.out.tab",
    log_file="results/star/{sample}-{unit}/Log.out",
    sj="results/star/{sample}-{unit}/SJ.out.tab",
    log_final="results/star/{sample}-{unit}/Log.final.out",
  log:
    "logs/star/{sample}-{unit}.log",
  params:
    out_prefix=lambda wc: f"results/star/{wc.sample}-{wc.unit}/",
    extra=lambda wc, input: " ".join(
      [
        "--outSAMtype BAM SortedByCoordinate",
        "--quantMode GeneCounts",
        f'--sjdbGTFfile "{input.gtf}"',
        config.get("params", {}).get("star", {}).get("align", ""),
      ]
    ),
    # 如果输入是 .gz 文件则需要 gunzip 解压
    read_cmd=lambda wc, input: (
      '--readFilesCommand "gunzip -c"'
      if hasattr(input, "fq1") and input.fq1.endswith(".gz")
      else ""
    ),
  threads: 24
  shell:
    "STAR --runThreadN {threads}"
    " --genomeDir {input.idx}"
    " --readFilesIn {input.fq1} "
    " $([ -f '{input.fq2}' ] 2>/dev/null && echo '{input.fq2}' || true)"
    " {params.read_cmd}"
    " --outFileNamePrefix {params.out_prefix}"
    " {params.extra}"
    " > {log} 2>&1"
