configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bam_stats"


rule all:
  input:
    "results/finish/bam_stats.done"


rule run_bam_stats:
  output:
    "results/finish/bam_stats.done"
  run:
    run_step(STEP_ID, output[0])
