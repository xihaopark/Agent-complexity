configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "methylkit_unite_per_chr_all"


rule all:
  input:
    "results/finish/methylkit_unite_per_chr_all.done"


rule run_methylkit_unite_per_chr_all:
  output:
    "results/finish/methylkit_unite_per_chr_all.done"
  run:
    run_step(STEP_ID, output[0])
