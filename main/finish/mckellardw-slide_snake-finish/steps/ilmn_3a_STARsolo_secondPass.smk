configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_3a_STARsolo_secondPass"


rule all:
  input:
    "results/finish/ilmn_3a_STARsolo_secondPass.done"


rule run_ilmn_3a_STARsolo_secondPass:
  output:
    "results/finish/ilmn_3a_STARsolo_secondPass.done"
  run:
    run_step(STEP_ID, output[0])
