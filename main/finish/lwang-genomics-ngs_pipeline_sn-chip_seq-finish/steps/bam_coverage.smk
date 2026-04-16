configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bam_coverage"


rule all:
  input:
    "results/finish/bam_coverage.done"


rule run_bam_coverage:
  output:
    "results/finish/bam_coverage.done"
  run:
    run_step(STEP_ID, output[0])
