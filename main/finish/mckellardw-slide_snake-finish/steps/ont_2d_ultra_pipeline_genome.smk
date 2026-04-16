configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_2d_ultra_pipeline_genome"


rule all:
  input:
    "results/finish/ont_2d_ultra_pipeline_genome.done"


rule run_ont_2d_ultra_pipeline_genome:
  output:
    "results/finish/ont_2d_ultra_pipeline_genome.done"
  run:
    run_step(STEP_ID, output[0])
