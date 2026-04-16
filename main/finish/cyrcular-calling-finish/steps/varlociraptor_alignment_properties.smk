configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "varlociraptor_alignment_properties"


rule all:
  input:
    "results/finish/varlociraptor_alignment_properties.done"


rule run_varlociraptor_alignment_properties:
  output:
    "results/finish/varlociraptor_alignment_properties.done"
  run:
    run_step(STEP_ID, output[0])
