configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "remove_non_pass"


rule all:
  input:
    "results/finish/remove_non_pass.done"


rule run_remove_non_pass:
  output:
    "results/finish/remove_non_pass.done"
  run:
    run_step(STEP_ID, output[0])
