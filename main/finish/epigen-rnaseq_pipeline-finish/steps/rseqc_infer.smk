configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "rseqc_infer"


rule all:
  input:
    "results/finish/rseqc_infer.done"


rule run_rseqc_infer:
  output:
    "results/finish/rseqc_infer.done"
  run:
    run_step(STEP_ID, output[0])
