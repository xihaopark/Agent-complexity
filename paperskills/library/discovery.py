#!/usr/bin/env python3
"""Skill Discovery Interface - Agent-oriented retrieval without hard bindings.

Philosophy: Instead of task->skill mappings, provide scenario->relevant_skills
with decision guidance. Let agent choose based on context.

Usage:
    # Discover skills for a scenario
    python paperskills/library/discovery.py --scenario rna_de_analysis
    
    # Find alternatives to a tool
    python paperskills/library/discovery.py --alternatives-to DESeq2
    
    # Chain: what comes after differential expression?
    python paperskills/library/discovery.py --downstream-of DESeq2
    
    # Multi-criteria search
    python paperskills/library/discovery.py \
        --analysis differential_expression \
        --data-type rna_seq_counts \
        --design small_sample
"""

import argparse
import json
from pathlib import Path
from typing import Any


def load_skill_graph() -> dict:
    """Load the skill discovery graph."""
    graph_path = Path(__file__).parent / "indices" / "skill_graph.json"
    return json.loads(graph_path.read_text())


def load_library_index() -> dict:
    """Load the master library index for metadata."""
    index_path = Path(__file__).parent / "indices" / "master_index.json"
    return json.loads(index_path.read_text())


def discover_for_scenario(scenario: str, graph: dict) -> dict | None:
    """Get discovery information for a scenario."""
    rules = graph.get("discovery_rules", {}).get("scenario_to_skills", {})
    return rules.get(scenario)


def get_skill_metadata(doi: str, graph: dict, index: dict) -> dict:
    """Enrich skill with both graph and index data."""
    skill_graph = graph.get("skills", {}).get(doi, {})
    skill_index = next((e for e in index.get("entries", []) if e["doi"] == doi), {})
    
    return {
        "doi": doi,
        "tool": skill_graph.get("tool") or skill_index.get("tool"),
        "analysis_type": skill_graph.get("primary_analysis"),
        "tags": skill_graph.get("tags", []),
        "use_when": skill_graph.get("use_when", []),
        "not_when": skill_graph.get("not_when", []),
        "related": skill_graph.get("related_tools", {}),
        "strengths": skill_graph.get("strengths", []),
        "limitations": skill_graph.get("limitations", []),
        "skill_md_path": skill_index.get("skill_md_path"),
    }


def find_alternatives(tool_name: str, graph: dict) -> list[dict]:
    """Find alternative tools to the given one."""
    # Find the skill with this tool
    target_doi = None
    for doi, skill in graph.get("skills", {}).items():
        if skill.get("tool", "").lower() == tool_name.lower():
            target_doi = doi
            break
    
    if not target_doi:
        return []
    
    related = graph["skills"][target_doi].get("related_tools", {})
    alternatives = related.get("alternatives", [])
    
    return alternatives


def find_workflow_chain(start_tool: str, graph: dict, index: dict, direction: str = "downstream") -> list[dict]:
    """Find tools upstream or downstream in analysis workflow."""
    # Find starting skill
    start_doi = None
    for doi, skill in graph.get("skills", {}).items():
        if skill.get("tool", "").lower() == start_tool.lower():
            start_doi = doi
            break
    
    if not start_doi:
        return []
    
    related = graph["skills"][start_doi].get("related_tools", {})
    
    if direction == "downstream":
        dois = related.get("downstream", []) + related.get("complements", [])
    elif direction == "upstream":
        dois = related.get("upstream_of", [])
    else:
        dois = []
    
    return [get_skill_metadata(doi, graph, index) for doi in dois if doi in graph.get("skills", {})]


def multi_criteria_search(
    analysis_type: str | None,
    data_type: str | None,
    design: str | None,
    graph: dict,
    index: dict
) -> list[dict]:
    """Find skills matching multiple criteria."""
    results = []
    
    for doi, skill in graph.get("skills", {}).items():
        score = 0
        
        if analysis_type and skill.get("primary_analysis") == analysis_type:
            score += 3
        if data_type and data_type in skill.get("applicable_data_types", []):
            score += 2
        if design and design in skill.get("experimental_designs", []):
            score += 2
        
        if score > 0:
            meta = get_skill_metadata(doi, graph, index)
            meta["relevance_score"] = score
            results.append(meta)
    
    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    return results


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    
    # Scenario-based discovery
    ap.add_argument("--scenario", help="Discover skills for a scenario (e.g., rna_de_analysis)")
    ap.add_argument("--list-scenarios", action="store_true", help="List available scenarios")
    
    # Relationship queries
    ap.add_argument("--alternatives-to", help="Find alternatives to a tool (e.g., DESeq2)")
    ap.add_argument("--downstream-of", help="Find tools that come after (e.g., DESeq2)")
    ap.add_argument("--upstream-of", help="Find tools that come before")
    
    # Multi-criteria search
    ap.add_argument("--analysis", help="Analysis type (e.g., differential_expression)")
    ap.add_argument("--data-type", dest="data_type", help="Data type (e.g., rna_seq_counts)")
    ap.add_argument("--design", help="Experimental design (e.g., small_sample)")
    
    # Output
    ap.add_argument("--json", action="store_true", help="Output as JSON")
    ap.add_argument("--verbose", "-v", action="store_true", help="Show detailed guidance")
    
    args = ap.parse_args()
    
    graph = load_skill_graph()
    index = load_library_index()
    
    if args.list_scenarios:
        scenarios = graph.get("discovery_rules", {}).get("scenario_to_skills", {})
        print("Available scenarios:")
        for name, info in scenarios.items():
            print(f"  {name}: {info.get('description', '')}")
        return
    
    if args.scenario:
        discovery = discover_for_scenario(args.scenario, graph)
        if not discovery:
            print(f"Unknown scenario: {args.scenario}")
            print(f"Use --list-scenarios to see available scenarios")
            return
        
        if args.json:
            print(json.dumps(discovery, indent=2))
        else:
            print(f"\n📋 Scenario: {discovery['description']}")
            print(f"\n💡 Decision Guide:\n   {discovery['decision_guide']}")
            print(f"\n🔧 Relevant Skills:")
            for doi in discovery.get("relevant_skills", []):
                skill = get_skill_metadata(doi, graph, index)
                print(f"   • {skill['tool']}")
                if args.verbose:
                    for use in skill.get("use_when", [])[:2]:
                        print(f"     ✓ {use}")
        return
    
    if args.alternatives_to:
        alts = find_alternatives(args.alternatives_to, graph)
        if not alts:
            print(f"No alternatives found for {args.alternatives_to}")
            return
        
        print(f"\n🔄 Alternatives to {args.alternatives_to}:")
        for doi in alts:
            if doi not in graph.get("skills", {}):
                print(f"   • {doi} (skill not in library yet)")
                continue
            skill = get_skill_metadata(doi, graph, index)
            print(f"   • {skill['tool']}")
            if args.verbose and skill.get("strengths"):
                print(f"     Strengths: {', '.join(skill['strengths'][:2])}")
        return
    
    if args.downstream_of:
        chain = find_workflow_chain(args.downstream_of, graph, index, "downstream")
        print(f"\n⬇️  After {args.downstream_of}, consider:")
        for skill in chain:
            print(f"   • {skill['tool']} ({skill.get('analysis_type', 'N/A')})")
        return
    
    if args.upstream_of:
        chain = find_workflow_chain(args.upstream_of, graph, index, "upstream")
        print(f"\n⬆️  Before {args.upstream_of}, you need:")
        for skill in chain:
            print(f"   • {skill['tool']}")
        return
    
    if args.analysis or args.data_type or args.design:
        results = multi_criteria_search(
            args.analysis, args.data_type, args.design,
            graph, index
        )
        
        if not results:
            print("No skills match the criteria")
            return
        
        print(f"\n🔍 Matching skills (by relevance):")
        for skill in results[:5]:
            score = skill.get("relevance_score", 0)
            print(f"   [{score}★] {skill['tool']} - {skill.get('analysis_type', 'N/A')}")
            if args.verbose:
                tags = ", ".join(skill.get("tags", [])[:3])
                print(f"       Tags: {tags}")
        return
    
    ap.print_help()


if __name__ == "__main__":
    main()
