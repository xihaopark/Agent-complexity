configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "rseqc_readdis"


rule all:
  input:
    "results/finish/rseqc_readdis.done"


rule run_rseqc_readdis:
  output:
    "results/finish/rseqc_readdis.done"
  run:
    run_step(STEP_ID, output[0])
