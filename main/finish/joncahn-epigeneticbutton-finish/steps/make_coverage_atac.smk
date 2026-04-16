configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "make_coverage_atac"


rule all:
  input:
    "results/finish/make_coverage_atac.done"


rule run_make_coverage_atac:
  output:
    "results/finish/make_coverage_atac.done"
  run:
    run_step(STEP_ID, output[0])
