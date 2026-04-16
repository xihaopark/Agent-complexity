configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "scanpy_preprocess"


rule all:
  input:
    "results/finish/scanpy_preprocess.done"


rule run_scanpy_preprocess:
  output:
    "results/finish/scanpy_preprocess.done"
  run:
    run_step(STEP_ID, output[0])
