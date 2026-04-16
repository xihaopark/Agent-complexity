configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "multiqc_fastqc_reads"


rule all:
  input:
    "results/finish/multiqc_fastqc_reads.done"


rule run_multiqc_fastqc_reads:
  output:
    "results/finish/multiqc_fastqc_reads.done"
  run:
    run_step(STEP_ID, output[0])
