configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_selected_transcripts_aligned_read_bins"


rule all:
  input:
    "results/finish/get_selected_transcripts_aligned_read_bins.done"


rule run_get_selected_transcripts_aligned_read_bins:
  output:
    "results/finish/get_selected_transcripts_aligned_read_bins.done"
  run:
    run_step(STEP_ID, output[0])
