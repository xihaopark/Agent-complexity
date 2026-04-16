configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "multiqc"


rule all:
  input:
    "results/finish/multiqc.done"


rule run_multiqc:
  output:
    "results/finish/multiqc.done"
  run:
    run_step(STEP_ID, output[0])
