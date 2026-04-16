configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plotCorrelation_pearson"


rule all:
  input:
    "results/finish/plotCorrelation_pearson.done"


rule run_plotCorrelation_pearson:
  output:
    "results/finish/plotCorrelation_pearson.done"
  run:
    run_step(STEP_ID, output[0])
