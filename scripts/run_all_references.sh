#!/bin/bash
# Run all Tier A reference scripts to generate ground truth
# Usage: ./scripts/run_all_references.sh

set -e

TASKS=(
    "deseq2_apeglm_small_n"
    "deseq2_lrt_interaction"
    "deseq2_shrinkage_comparison"
    "limma_voom_weights"
    "limma_duplicatecorrelation"
)

BASE_DIR="main/paper_primary_benchmark/ldp_r_task_eval/tasks/paper_sensitive_v1"

echo "=== Running Reference Scripts for Tier A Tasks ==="
echo ""

for task in "${TASKS[@]}"; do
    echo "[$task] Running reference script..."
    
    WORKSPACE="$BASE_DIR/real/$task/workspace"
    REF_SCRIPT="$BASE_DIR/real_ground_truth/$task/reference/script.R"
    OUTPUT_DIR="$BASE_DIR/real_ground_truth/$task/reference_output"
    
    # Ensure workspace exists
    mkdir -p "$WORKSPACE/input"
    mkdir -p "$WORKSPACE/output"
    mkdir -p "$OUTPUT_DIR"
    
    # Copy input data to workspace if not exists
    if [ ! -f "$WORKSPACE/input/counts.tsv" ]; then
        cp "$BASE_DIR/real/$task/input/"*.tsv "$WORKSPACE/input/" 2>/dev/null || echo "  Warning: No input data found for $task"
    fi
    
    # Run reference script
    cd "$WORKSPACE"
    Rscript "$REF_SCRIPT" 2>&1 | tee "output/reference_run.log"
    
    # Copy output to reference_output
    if [ -f "output/de_results.csv" ] || [ -f "output/interaction_de.csv" ] || [ -f "output/shrunk_de.csv" ] || [ -f "output/de_results_weighted.csv" ] || [ -f "output/paired_de.csv" ]; then
        cp output/*.csv "$OUTPUT_DIR/"
        echo "  ✓ Ground truth generated in $OUTPUT_DIR"
    else
        echo "  ✗ No output files found!"
        exit 1
    fi
    
    cd - > /dev/null
done

echo ""
echo "=== All reference runs complete ==="
echo "Ground truth locations:"
for task in "${TASKS[@]}"; do
    echo "  - $BASE_DIR/real_ground_truth/$task/reference_output/"
done
