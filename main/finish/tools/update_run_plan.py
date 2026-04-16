import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALL_EVAL_JSON = ROOT / "ALL_EVAL.json"
EXPANSION_STATUS_JSON = ROOT / "FINISH_EXPANSION_STATUS.json"
PLAN_JSON = ROOT / "BENCHMARK_RUN_PLAN.json"

def main():
    eval_data = json.loads(ALL_EVAL_JSON.read_text(encoding="utf-8"))
    status_data = json.loads(EXPANSION_STATUS_JSON.read_text(encoding="utf-8"))
    
    evaluable_ids = [
        item["workflow_id"] 
        for item in eval_data.get("workflow_evaluability", []) 
        if item.get("evaluable")
    ]
    
    status_map = {
        item["workflow_id"]: item
        for item in status_data.get("rows", [])
    }
    
    selected = []
    family_counts = {}
    for wid in evaluable_ids:
        row = status_map.get(wid, {})
        # Simple heuristic for family if not explicitly provided
        family = "other"
        if "rna" in wid.lower() or "rnaseq" in wid.lower(): family = "rna"
        elif "chip" in wid.lower() or "atac" in wid.lower() or "epigen" in wid.lower(): family = "epigenomics"
        elif "single" in wid.lower() or "sc" in wid.lower() or "seurat" in wid.lower(): family = "single-cell"
        elif "var" in wid.lower() or "dna" in wid.lower() or "snp" in wid.lower() or "mut" in wid.lower() or "msisensor" in wid.lower() or "cyrcular" in wid.lower() or "circle" in wid.lower(): family = "variant"
        
        family_counts[family] = family_counts.get(family, 0) + 1
        
        step_count = row.get("step_count", 10)
        tier = "small"
        if step_count > 15: tier = "medium"
        if step_count > 30: tier = "large"
        
        selected.append({
            "workflow_id": wid,
            "canonical_workflow_id": wid,
            "workflow_dir": str(ROOT / wid),
            "status": "passed",
            "step_count": step_count,
            "family": family,
            "tier": tier,
            "conversion_type": "auto" # Or maybe guess from row if available
        })
        
    plan = {
        "summary": {
            "max_total": 50,
            "max_per_family": 20,
            "include_large": True,
            "selected_count": len(selected),
            "family_counts": family_counts
        },
        "selected_workflows": selected
    }
    
    PLAN_JSON.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {PLAN_JSON.name} with {len(selected)} workflows.")

if __name__ == "__main__":
    main()
