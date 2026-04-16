configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "reheader_varlociraptor"


rule all:
  input:
    "results/finish/reheader_varlociraptor.done"


rule run_reheader_varlociraptor:
  output:
    "results/finish/reheader_varlociraptor.done"
  run:
    run_step(STEP_ID, output[0])
