configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_3a_STARsolo_firstPass"


rule all:
  input:
    "results/finish/ilmn_3a_STARsolo_firstPass.done"


rule run_ilmn_3a_STARsolo_firstPass:
  output:
    "results/finish/ilmn_3a_STARsolo_firstPass.done"
  run:
    run_step(STEP_ID, output[0])
