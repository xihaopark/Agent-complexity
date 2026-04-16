configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "preseq_lc_extrap"


rule all:
  input:
    "results/finish/preseq_lc_extrap.done"


rule run_preseq_lc_extrap:
  output:
    "results/finish/preseq_lc_extrap.done"
  run:
    run_step(STEP_ID, output[0])
