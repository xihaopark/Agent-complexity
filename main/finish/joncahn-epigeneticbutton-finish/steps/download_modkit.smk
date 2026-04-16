configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "download_modkit"


rule all:
  input:
    "results/finish/download_modkit.done"


rule run_download_modkit:
  output:
    "results/finish/download_modkit.done"
  run:
    run_step(STEP_ID, output[0])
