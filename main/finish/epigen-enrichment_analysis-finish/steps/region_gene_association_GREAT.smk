configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "region_gene_association_GREAT"


rule all:
  input:
    "results/finish/region_gene_association_GREAT.done"


rule run_region_gene_association_GREAT:
  output:
    "results/finish/region_gene_association_GREAT.done"
  run:
    run_step(STEP_ID, output[0])
