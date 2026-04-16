configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "rseqc_junction_annotation"


rule all:
  input:
    "results/finish/rseqc_junction_annotation.done"


rule run_rseqc_junction_annotation:
  output:
    "results/finish/rseqc_junction_annotation.done"
  run:
    run_step(STEP_ID, output[0])
