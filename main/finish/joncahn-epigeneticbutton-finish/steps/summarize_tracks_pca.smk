configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "summarize_tracks_pca"


rule all:
  input:
    "results/finish/summarize_tracks_pca.done"


rule run_summarize_tracks_pca:
  output:
    "results/finish/summarize_tracks_pca.done"
  run:
    run_step(STEP_ID, output[0])
