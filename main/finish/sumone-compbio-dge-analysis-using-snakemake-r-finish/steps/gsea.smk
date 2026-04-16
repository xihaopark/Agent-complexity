configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "gsea"


rule all:
  input:
    "results/finish/gsea.done"


rule run_gsea:
  output:
    "results/finish/gsea.done"
  run:
    run_step(STEP_ID, output[0])
