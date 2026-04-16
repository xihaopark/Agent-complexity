configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "build_primer_regions"


rule all:
  input:
    "results/finish/build_primer_regions.done"


rule run_build_primer_regions:
  output:
    "results/finish/build_primer_regions.done"
  run:
    run_step(STEP_ID, output[0])
