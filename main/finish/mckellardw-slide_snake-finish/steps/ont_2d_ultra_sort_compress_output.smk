configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_2d_ultra_sort_compress_output"


rule all:
  input:
    "results/finish/ont_2d_ultra_sort_compress_output.done"


rule run_ont_2d_ultra_sort_compress_output:
  output:
    "results/finish/ont_2d_ultra_sort_compress_output.done"
  run:
    run_step(STEP_ID, output[0])
