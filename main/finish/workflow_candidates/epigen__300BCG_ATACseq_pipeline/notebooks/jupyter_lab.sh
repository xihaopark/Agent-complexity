#!/bin/bash
#SBATCH --partition=interactiveq
#SBATCH --qos=interactiveq
#SBATCH --cpus-per-task=16
#SBATCH --mem=120G
#SBATCH --time 12:00:00
#SBATCH --job-name jupyterlab
#SBATCH --output ./jupyterlab.log 
#SBATCH --error ./jupyterlab.err 
# get tunneling info
port=$(shuf -i8000-9999 -n1)
node=$(hostname --long)
user=$(whoami)

# DON'T USE ADDRESS BELOW.
# DO USE TOKEN BELOW
jupyter lab --no-browser --port=${port} --ip=${node}
