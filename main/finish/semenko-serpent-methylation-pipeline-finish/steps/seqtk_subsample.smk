configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "seqtk_subsample"


rule all:
  input:
    "results/finish/seqtk_subsample.done"


rule run_seqtk_subsample:
  output:
    "results/finish/seqtk_subsample.done"
  run:
    run_step(STEP_ID, output[0])
