configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "rseqc_innerdis"


rule all:
  input:
    "results/finish/rseqc_innerdis.done"


rule run_rseqc_innerdis:
  output:
    "results/finish/rseqc_innerdis.done"
  run:
    run_step(STEP_ID, output[0])
