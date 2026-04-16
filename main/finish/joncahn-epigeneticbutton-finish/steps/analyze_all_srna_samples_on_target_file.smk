configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "analyze_all_srna_samples_on_target_file"


rule all:
  input:
    "results/finish/analyze_all_srna_samples_on_target_file.done"


rule run_analyze_all_srna_samples_on_target_file:
  output:
    "results/finish/analyze_all_srna_samples_on_target_file.done"
  run:
    run_step(STEP_ID, output[0])
