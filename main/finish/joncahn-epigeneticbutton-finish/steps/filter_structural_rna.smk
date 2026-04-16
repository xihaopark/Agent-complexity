configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "filter_structural_rna"


rule all:
  input:
    "results/finish/filter_structural_rna.done"


rule run_filter_structural_rna:
  output:
    "results/finish/filter_structural_rna.done"
  run:
    run_step(STEP_ID, output[0])
