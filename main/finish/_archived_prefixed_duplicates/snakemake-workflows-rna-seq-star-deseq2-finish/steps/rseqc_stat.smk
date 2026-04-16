configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "rseqc_stat"


rule all:
  input:
    "results/finish/rseqc_stat.done"


rule run_rseqc_stat:
  output:
    "results/finish/rseqc_stat.done"
  run:
    run_step(STEP_ID, output[0])
