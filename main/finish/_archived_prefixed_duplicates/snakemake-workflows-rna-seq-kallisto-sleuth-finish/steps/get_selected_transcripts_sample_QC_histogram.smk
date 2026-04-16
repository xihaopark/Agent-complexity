configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_selected_transcripts_sample_QC_histogram"


rule all:
  input:
    "results/finish/get_selected_transcripts_sample_QC_histogram.done"


rule run_get_selected_transcripts_sample_QC_histogram:
  output:
    "results/finish/get_selected_transcripts_sample_QC_histogram.done"
  run:
    run_step(STEP_ID, output[0])
