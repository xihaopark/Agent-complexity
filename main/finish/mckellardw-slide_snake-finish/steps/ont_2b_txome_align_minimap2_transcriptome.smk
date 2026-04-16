configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_2b_txome_align_minimap2_transcriptome"


rule all:
  input:
    "results/finish/ont_2b_txome_align_minimap2_transcriptome.done"


rule run_ont_2b_txome_align_minimap2_transcriptome:
  output:
    "results/finish/ont_2b_txome_align_minimap2_transcriptome.done"
  run:
    run_step(STEP_ID, output[0])
