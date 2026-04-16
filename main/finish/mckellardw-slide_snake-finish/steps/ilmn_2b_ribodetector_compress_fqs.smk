configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_2b_ribodetector_compress_fqs"


rule all:
  input:
    "results/finish/ilmn_2b_ribodetector_compress_fqs.done"


rule run_ilmn_2b_ribodetector_compress_fqs:
  output:
    "results/finish/ilmn_2b_ribodetector_compress_fqs.done"
  run:
    run_step(STEP_ID, output[0])
