"""
Step 3: RSeQC Quality Control / 步骤3：RSeQC 质量控制

Evaluate RNA-seq alignment quality using RSeQC suite.
使用 RSeQC 工具套件评估 RNA-seq 比对质量。

Usage / 使用方法:
  snakemake -s steps/rseqc_qc.smk --configfile config_basic/config.yaml --cores 8

Input / 输入:
  results/star/ - BAM files from step 2 / 步骤2产生的 BAM 文件
  resources/genome.gtf - Gene annotation / 基因注释文件

Output / 输出:
  results/qc/rseqc/ - RSeQC analysis results for each sample / 每个样本的 RSeQC 分析结果
"""

configfile: "config_basic/config.yaml"


include: "common.smk"


rule all:
  """
  Target rule for RSeQC QC step / RSeQC 质控步骤的目标规则

  收集所有 8 类 RSeQC 分析结果作为目标输出。
  """
  input:
    expand(
      "results/qc/rseqc/{unit.sample_name}-{unit.unit_name}.junctionanno.junction.bed",
      unit=units.itertuples(),
    ),
    expand(
      "results/qc/rseqc/{unit.sample_name}-{unit.unit_name}.junctionsat.junctionSaturation_plot.pdf",
      unit=units.itertuples(),
    ),
    expand(
      "results/qc/rseqc/{unit.sample_name}-{unit.unit_name}.infer_experiment.txt",
      unit=units.itertuples(),
    ),
    expand(
      "results/qc/rseqc/{unit.sample_name}-{unit.unit_name}.stats.txt",
      unit=units.itertuples(),
    ),
    expand(
      "results/qc/rseqc/{unit.sample_name}-{unit.unit_name}.inner_distance_freq.inner_distance.txt",
      unit=units.itertuples(),
    ),
    expand(
      "results/qc/rseqc/{unit.sample_name}-{unit.unit_name}.readdistribution.txt",
      unit=units.itertuples(),
    ),
    expand(
      "results/qc/rseqc/{unit.sample_name}-{unit.unit_name}.readdup.DupRate_plot.pdf",
      unit=units.itertuples(),
    ),
    expand(
      "results/qc/rseqc/{unit.sample_name}-{unit.unit_name}.readgc.GC_plot.pdf",
      unit=units.itertuples(),
    ),


rule rseqc_gtf2bed:
  """
  Convert GTF annotation to BED12 format / 将 GTF 注释转换为 BED12 格式

  RSeQC 工具需要 BED12 格式的注释文件。
  使用 gffutils 库解析 GTF 并提取 transcript 特征。
  """
  input:
    "resources/genome.gtf",
  output:
    bed="results/qc/rseqc/annotation.bed",
    db=temp("results/qc/rseqc/annotation.db"),
  log:
    "logs/rseqc_gtf2bed.log",
  script:
    "../workflow/scripts/gtf2bed.py"


rule rseqc_junction_annotation:
  """
  Annotate splice junctions / 注释剪接位点

  验证比对的 reads 是否与已知剪接位点对齐，
  使用 MAPQ=255 过滤（STAR 对 unique mapper 的标记）。
  """
  input:
    bam="results/star/{sample}-{unit}/Aligned.sortedByCoord.out.bam",
    bed="results/qc/rseqc/annotation.bed",
  output:
    "results/qc/rseqc/{sample}-{unit}.junctionanno.junction.bed",
  priority: 1
  log:
    "logs/rseqc/rseqc_junction_annotation/{sample}-{unit}.log",
  params:
    extra=r"-q 255",
    prefix=lambda w, output: output[0].replace(".junction.bed", ""),
  shell:
    "junction_annotation.py {params.extra} -i {input.bam} -r {input.bed} -o {params.prefix} "
    "> {log[0]} 2>&1"


rule rseqc_junction_saturation:
  """
  Evaluate junction detection saturation / 评估剪接位点检测的饱和度

  通过下采样分析，判断测序深度是否足以检测到大部分剪接位点。
  """
  input:
    bam="results/star/{sample}-{unit}/Aligned.sortedByCoord.out.bam",
    bed="results/qc/rseqc/annotation.bed",
  output:
    "results/qc/rseqc/{sample}-{unit}.junctionsat.junctionSaturation_plot.pdf",
  priority: 1
  log:
    "logs/rseqc/rseqc_junction_saturation/{sample}-{unit}.log",
  params:
    extra=r"-q 255",
    prefix=lambda w, output: output[0].replace(".junctionSaturation_plot.pdf", ""),
  shell:
    "junction_saturation.py {params.extra} -i {input.bam} -r {input.bed} -o {params.prefix} "
    "> {log} 2>&1"


rule rseqc_stat:
  """
  Generate BAM alignment statistics / 生成 BAM 比对统计信息

  报告总读段数、映射率、配对信息等基础比对指标。
  """
  input:
    "results/star/{sample}-{unit}/Aligned.sortedByCoord.out.bam",
  output:
    "results/qc/rseqc/{sample}-{unit}.stats.txt",
  priority: 1
  log:
    "logs/rseqc/rseqc_stat/{sample}-{unit}.log",
  shell:
    "bam_stat.py -i {input} > {output} 2> {log}"


rule rseqc_infer:
  """
  Infer RNA-seq strandedness / 推断 RNA-seq 链特异性

  通过比较 reads 与已知转录本的方向关系，
  推断文库制备方案的链特异性（forward/reverse/unstranded）。
  """
  input:
    bam="results/star/{sample}-{unit}/Aligned.sortedByCoord.out.bam",
    bed="results/qc/rseqc/annotation.bed",
  output:
    "results/qc/rseqc/{sample}-{unit}.infer_experiment.txt",
  priority: 1
  log:
    "logs/rseqc/rseqc_infer/{sample}-{unit}.log",
  shell:
    "infer_experiment.py -r {input.bed} -i {input.bam} > {output} 2> {log}"


rule rseqc_innerdis:
  """
  Analyze inner distance of paired-end reads / 分析双端 reads 的内部距离分布

  评估文库片段大小分布，对双端测序数据的质量评估很重要。
  """
  input:
    bam="results/star/{sample}-{unit}/Aligned.sortedByCoord.out.bam",
    bed="results/qc/rseqc/annotation.bed",
  output:
    "results/qc/rseqc/{sample}-{unit}.inner_distance_freq.inner_distance.txt",
  priority: 1
  log:
    "logs/rseqc/rseqc_innerdis/{sample}-{unit}.log",
  params:
    prefix=lambda w, output: output[0].replace(".inner_distance.txt", ""),
  shell:
    "inner_distance.py -r {input.bed} -i {input.bam} -o {params.prefix} > {log} 2>&1"


rule rseqc_readdis:
  """
  Analyze read distribution across genomic features / 分析 reads 在基因组特征上的分布

  统计 reads 在外显子、内含子、基因间区等区域的分布比例。
  """
  input:
    bam="results/star/{sample}-{unit}/Aligned.sortedByCoord.out.bam",
    bed="results/qc/rseqc/annotation.bed",
  output:
    "results/qc/rseqc/{sample}-{unit}.readdistribution.txt",
  priority: 1
  log:
    "logs/rseqc/rseqc_readdis/{sample}-{unit}.log",
  shell:
    "read_distribution.py -r {input.bed} -i {input.bam} > {output} 2> {log}"


rule rseqc_readdup:
  """
  Evaluate read duplication rate / 评估 reads 重复率

  分析 PCR 重复程度，过高的重复率可能表明文库复杂度不足。
  """
  input:
    "results/star/{sample}-{unit}/Aligned.sortedByCoord.out.bam",
  output:
    "results/qc/rseqc/{sample}-{unit}.readdup.DupRate_plot.pdf",
  priority: 1
  log:
    "logs/rseqc/rseqc_readdup/{sample}-{unit}.log",
  params:
    prefix=lambda w, output: output[0].replace(".DupRate_plot.pdf", ""),
  shell:
    "read_duplication.py -i {input} -o {params.prefix} > {log} 2>&1"


rule rseqc_readgc:
  """
  Analyze read GC content distribution / 分析 reads 的 GC 含量分布

  GC 含量偏差可能指示文库制备或测序的系统性偏差。
  """
  input:
    "results/star/{sample}-{unit}/Aligned.sortedByCoord.out.bam",
  output:
    "results/qc/rseqc/{sample}-{unit}.readgc.GC_plot.pdf",
  priority: 1
  log:
    "logs/rseqc/rseqc_readgc/{sample}-{unit}.log",
  params:
    prefix=lambda w, output: output[0].replace(".GC_plot.pdf", ""),
  shell:
    "read_GC.py -i {input} -o {params.prefix} > {log} 2>&1"
