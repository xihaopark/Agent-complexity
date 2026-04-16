configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_1a_subset_fastq_by_adapter_type"


rule all:
  input:
    "results/finish/ont_1a_subset_fastq_by_adapter_type.done"


rule run_ont_1a_subset_fastq_by_adapter_type:
  output:
    "results/finish/ont_1a_subset_fastq_by_adapter_type.done"
  run:
    run_step(STEP_ID, output[0])
