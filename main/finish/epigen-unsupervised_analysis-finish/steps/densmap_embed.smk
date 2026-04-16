configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "densmap_embed"


rule all:
  input:
    "results/finish/densmap_embed.done"


rule run_densmap_embed:
  output:
    "results/finish/densmap_embed.done"
  run:
    run_step(STEP_ID, output[0])
