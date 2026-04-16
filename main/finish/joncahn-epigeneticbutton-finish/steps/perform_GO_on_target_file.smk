configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "perform_GO_on_target_file"


rule all:
  input:
    "results/finish/perform_GO_on_target_file.done"


rule run_perform_GO_on_target_file:
  output:
    "results/finish/perform_GO_on_target_file.done"
  run:
    run_step(STEP_ID, output[0])
