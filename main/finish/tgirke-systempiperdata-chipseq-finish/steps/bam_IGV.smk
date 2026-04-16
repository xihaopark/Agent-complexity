configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bam_IGV"


rule all:
  input:
    "results/finish/bam_IGV.done"


rule run_bam_IGV:
  output:
    "results/finish/bam_IGV.done"
  run:
    run_step(STEP_ID, output[0])
