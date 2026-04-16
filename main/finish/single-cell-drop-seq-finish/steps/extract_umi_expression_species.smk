configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "extract_umi_expression_species"


rule all:
  input:
    "results/finish/extract_umi_expression_species.done"


rule run_extract_umi_expression_species:
  output:
    "results/finish/extract_umi_expression_species.done"
  run:
    run_step(STEP_ID, output[0])
