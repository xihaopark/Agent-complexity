configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "rseqc_readgc"


rule all:
  input:
    "results/finish/rseqc_readgc.done"


rule run_rseqc_readgc:
  output:
    "results/finish/rseqc_readgc.done"
  run:
    run_step(STEP_ID, output[0])
