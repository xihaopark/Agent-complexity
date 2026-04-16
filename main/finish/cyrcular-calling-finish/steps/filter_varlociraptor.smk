configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "filter_varlociraptor"


rule all:
  input:
    "results/finish/filter_varlociraptor.done"


rule run_filter_varlociraptor:
  output:
    "results/finish/filter_varlociraptor.done"
  run:
    run_step(STEP_ID, output[0])
