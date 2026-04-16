configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "rseqc_readdup"


rule all:
  input:
    "results/finish/rseqc_readdup.done"


rule run_rseqc_readdup:
  output:
    "results/finish/rseqc_readdup.done"
  run:
    run_step(STEP_ID, output[0])
