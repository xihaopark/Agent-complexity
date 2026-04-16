configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_1c_fastq_call_bc_from_adapter"


rule all:
  input:
    "results/finish/ont_1c_fastq_call_bc_from_adapter.done"


rule run_ont_1c_fastq_call_bc_from_adapter:
  output:
    "results/finish/ont_1c_fastq_call_bc_from_adapter.done"
  run:
    run_step(STEP_ID, output[0])
