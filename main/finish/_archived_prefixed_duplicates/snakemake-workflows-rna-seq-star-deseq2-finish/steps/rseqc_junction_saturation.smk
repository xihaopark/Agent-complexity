configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "rseqc_junction_saturation"


rule all:
  input:
    "results/finish/rseqc_junction_saturation.done"


rule run_rseqc_junction_saturation:
  output:
    "results/finish/rseqc_junction_saturation.done"
  run:
    run_step(STEP_ID, output[0])
