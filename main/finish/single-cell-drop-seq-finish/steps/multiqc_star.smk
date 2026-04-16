configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "multiqc_star"


rule all:
  input:
    "results/finish/multiqc_star.done"


rule run_multiqc_star:
  output:
    "results/finish/multiqc_star.done"
  run:
    run_step(STEP_ID, output[0])
