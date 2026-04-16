configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "create_panel_of_normals_samples_list"


rule all:
  input:
    "results/finish/create_panel_of_normals_samples_list.done"


rule run_create_panel_of_normals_samples_list:
  output:
    "results/finish/create_panel_of_normals_samples_list.done"
  run:
    run_step(STEP_ID, output[0])
