configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bam_hist"


rule all:
  input:
    "results/finish/bam_hist.done"


rule run_bam_hist:
  output:
    "results/finish/bam_hist.done"
  run:
    run_step(STEP_ID, output[0])
