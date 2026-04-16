configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "varlociraptor_preprocess"


rule all:
  input:
    "results/finish/varlociraptor_preprocess.done"


rule run_varlociraptor_preprocess:
  output:
    "results/finish/varlociraptor_preprocess.done"
  run:
    run_step(STEP_ID, output[0])
