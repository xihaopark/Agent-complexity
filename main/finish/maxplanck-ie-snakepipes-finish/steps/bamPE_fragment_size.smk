configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bamPE_fragment_size"


rule all:
  input:
    "results/finish/bamPE_fragment_size.done"


rule run_bamPE_fragment_size:
  output:
    "results/finish/bamPE_fragment_size.done"
  run:
    run_step(STEP_ID, output[0])
