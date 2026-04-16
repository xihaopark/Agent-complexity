configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_2b_ribodetector"


rule all:
  input:
    "results/finish/ilmn_2b_ribodetector.done"


rule run_ilmn_2b_ribodetector:
  output:
    "results/finish/ilmn_2b_ribodetector.done"
  run:
    run_step(STEP_ID, output[0])
