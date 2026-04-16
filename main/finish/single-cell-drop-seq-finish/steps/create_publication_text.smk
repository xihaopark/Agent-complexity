configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "create_publication_text"


rule all:
  input:
    "results/finish/create_publication_text.done"


rule run_create_publication_text:
  output:
    "results/finish/create_publication_text.done"
  run:
    run_step(STEP_ID, output[0])
