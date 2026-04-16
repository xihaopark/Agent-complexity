configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "MergeBamAlignment"


rule all:
  input:
    "results/finish/MergeBamAlignment.done"


rule run_MergeBamAlignment:
  output:
    "results/finish/MergeBamAlignment.done"
  run:
    run_step(STEP_ID, output[0])
