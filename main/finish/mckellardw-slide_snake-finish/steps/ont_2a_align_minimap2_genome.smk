configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_2a_align_minimap2_genome"


rule all:
  input:
    "results/finish/ont_2a_align_minimap2_genome.done"


rule run_ont_2a_align_minimap2_genome:
  output:
    "results/finish/ont_2a_align_minimap2_genome.done"
  run:
    run_step(STEP_ID, output[0])
