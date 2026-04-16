configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_2b_ribodetector_filter_R1"


rule all:
  input:
    "results/finish/ilmn_2b_ribodetector_filter_R1.done"


rule run_ilmn_2b_ribodetector_filter_R1:
  output:
    "results/finish/ilmn_2b_ribodetector_filter_R1.done"
  run:
    run_step(STEP_ID, output[0])
