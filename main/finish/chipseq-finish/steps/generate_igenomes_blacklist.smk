configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "generate_igenomes_blacklist"


rule all:
  input:
    "results/finish/generate_igenomes_blacklist.done"


rule run_generate_igenomes_blacklist:
  output:
    "results/finish/generate_igenomes_blacklist.done"
  run:
    run_step(STEP_ID, output[0])
