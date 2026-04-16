configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "varlociraptor_call"


rule all:
  input:
    "results/finish/varlociraptor_call.done"


rule run_varlociraptor_call:
  output:
    "results/finish/varlociraptor_call.done"
  run:
    run_step(STEP_ID, output[0])
