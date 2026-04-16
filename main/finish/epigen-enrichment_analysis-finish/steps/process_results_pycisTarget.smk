configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "process_results_pycisTarget"


rule all:
  input:
    "results/finish/process_results_pycisTarget.done"


rule run_process_results_pycisTarget:
  output:
    "results/finish/process_results_pycisTarget.done"
  run:
    run_step(STEP_ID, output[0])
