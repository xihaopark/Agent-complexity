configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "meta_compare_diffexp"


rule all:
  input:
    "results/finish/meta_compare_diffexp.done"


rule run_meta_compare_diffexp:
  output:
    "results/finish/meta_compare_diffexp.done"
  run:
    run_step(STEP_ID, output[0])
