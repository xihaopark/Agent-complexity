configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plotCorrelation_spearman"


rule all:
  input:
    "results/finish/plotCorrelation_spearman.done"


rule run_plotCorrelation_spearman:
  output:
    "results/finish/plotCorrelation_spearman.done"
  run:
    run_step(STEP_ID, output[0])
