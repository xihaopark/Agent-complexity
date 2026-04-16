configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "generate_igenomes"


rule all:
  input:
    "results/finish/generate_igenomes.done"


rule run_generate_igenomes:
  output:
    "results/finish/generate_igenomes.done"
  run:
    run_step(STEP_ID, output[0])
