#!/usr/bin/env python3
"""Discovery Tool for Agent - Wraps discovery.py as a callable function.

This module provides functions that can be registered as tools in RTaskEvalEnv.
Agent can call these to discover relevant skills on-demand.
"""

import json
from pathlib import Path
from typing import Any

# Import discovery functionality
from paperskills.library.discovery import (
    load_skill_graph,
    load_library_index,
    discover_for_scenario,
    get_skill_metadata,
    find_alternatives,
    find_workflow_chain,
    multi_criteria_search,
)


def discover_skills_by_scenario(scenario: str) -> str:
    """Discover relevant skills for a given analysis scenario.
    
    Use this when you need guidance on what tools to use for a specific type of analysis.
    
    Args:
        scenario: Analysis scenario name (e.g., "rna_de_analysis", "scrna_analysis",
                 "small_sample_rna", "paired_design_rna", "chip_peak_calling")
    
    Returns:
        JSON string with relevant skills and decision guide.
    
    Example:
        discover_skills_by_scenario("small_sample_rna")
        # Returns: skills list with DESeq2 (apeglm) recommendation
    """
    graph = load_skill_graph()
    index = load_library_index()
    
    discovery = discover_for_scenario(scenario, graph)
    if not discovery:
        available = list(graph.get("discovery_rules", {}).get("scenario_to_skills", {}).keys())
        return json.dumps({
            "error": f"Unknown scenario: {scenario}",
            "available_scenarios": available
        }, indent=2)
    
    # Enrich with full metadata
    skills = []
    for doi in discovery.get("relevant_skills", []):
        meta = get_skill_metadata(doi, graph, index)
        skills.append({
            "tool": meta["tool"],
            "doi": meta["doi"],
            "analysis_type": meta["analysis_type"],
            "use_when": meta["use_when"][:3] if meta["use_when"] else [],
            "skill_md_path": meta["skill_md_path"],
        })
    
    result = {
        "scenario": scenario,
        "description": discovery.get("description"),
        "decision_guide": discovery.get("decision_guide"),
        "recommended_skills": skills,
    }
    
    return json.dumps(result, indent=2, ensure_ascii=False)


def discover_skills_by_criteria(
    analysis_type: str | None = None,
    data_type: str | None = None,
    experimental_design: str | None = None,
) -> str:
    """Discover skills matching specific criteria.
    
    Use this when you know specific characteristics of your data/analysis.
    
    Args:
        analysis_type: Type of analysis (e.g., "differential_expression", 
                      "peak_calling", "normalization", "clustering")
        data_type: Data type (e.g., "rna_seq_counts", "scrna_expression",
                  "chip_seq_reads", "methylation_data")
        experimental_design: Design type (e.g., "two_group_comparison",
                            "paired_samples", "small_sample", "batch_effects")
    
    Returns:
        JSON string with matching skills ranked by relevance.
    
    Example:
        discover_skills_by_criteria(
            analysis_type="differential_expression",
            data_type="rna_seq_counts",
            experimental_design="small_sample"
        )
    """
    graph = load_skill_graph()
    index = load_library_index()
    
    results = multi_criteria_search(
        analysis_type, data_type, experimental_design,
        graph, index
    )
    
    skills = []
    for skill in results[:5]:  # Top 5
        skills.append({
            "tool": skill["tool"],
            "doi": skill["doi"],
            "relevance_score": skill.get("relevance_score", 0),
            "analysis_type": skill.get("analysis_type"),
            "tags": skill.get("tags", [])[:5],
            "skill_md_path": skill["skill_md_path"],
        })
    
    return json.dumps({
        "query": {
            "analysis_type": analysis_type,
            "data_type": data_type,
            "experimental_design": experimental_design,
        },
        "matching_skills": skills,
    }, indent=2, ensure_ascii=False)


def get_skill_details(tool_name: str) -> str:
    """Get detailed information about a specific tool/skill.
    
    Use this to read the full details of a skill before using it.
    
    Args:
        tool_name: Name of the tool (e.g., "DESeq2", "limma", "MACS2")
    
    Returns:
        JSON string with complete skill metadata.
    """
    graph = load_skill_graph()
    index = load_library_index()
    
    # Find by tool name
    target_doi = None
    for doi, skill in graph.get("skills", {}).items():
        if skill.get("tool", "").lower() == tool_name.lower():
            target_doi = doi
            break
    
    if not target_doi:
        # Try fuzzy match
        available = [s.get("tool") for s in graph.get("skills", {}).values()]
        return json.dumps({
            "error": f"Tool '{tool_name}' not found",
            "available_tools": [t for t in available if t],
        }, indent=2)
    
    meta = get_skill_metadata(target_doi, graph, index)
    
    # Load full SKILL.md content if available
    skill_md_content = ""
    if meta.get("skill_md_path"):
        md_path = Path(meta["skill_md_path"])
        if not md_path.is_absolute():
            # Relative to repo root
            repo_root = Path(__file__).resolve().parents[3]
            md_path = repo_root / md_path
        if md_path.exists():
            skill_md_content = md_path.read_text(encoding="utf-8")
    
    result = {
        "tool": meta["tool"],
        "doi": meta["doi"],
        "analysis_type": meta["analysis_type"],
        "tags": meta.get("tags", []),
        "strengths": meta.get("strengths", []),
        "limitations": meta.get("limitations", []),
        "use_when": meta.get("use_when", []),
        "not_when": meta.get("not_when", []),
        "related_tools": meta.get("related", {}),
        "skill_md_content": skill_md_content,
    }
    
    return json.dumps(result, indent=2, ensure_ascii=False)


def find_alternative_tools(tool_name: str) -> str:
    """Find alternative tools to the given one.
    
    Use this when your current approach isn't working and want to try something else.
    
    Args:
        tool_name: Current tool name (e.g., "DESeq2")
    
    Returns:
        JSON string with alternative tools and their relative strengths.
    """
    graph = load_skill_graph()
    index = load_library_index()
    
    alts = find_alternatives(tool_name, graph)
    
    alternatives = []
    for doi in alts:
        if doi in graph.get("skills", {}):
            meta = get_skill_metadata(doi, graph, index)
            alternatives.append({
                "tool": meta["tool"],
                "doi": meta["doi"],
                "strengths": meta.get("strengths", [])[:3],
                "use_when": meta.get("use_when", [])[:2],
            })
    
    return json.dumps({
        "current_tool": tool_name,
        "alternatives": alternatives,
    }, indent=2, ensure_ascii=False)


def list_available_scenarios() -> str:
    """List all available discovery scenarios.
    
    Returns:
        JSON string with scenario names and descriptions.
    """
    graph = load_skill_graph()
    scenarios = graph.get("discovery_rules", {}).get("scenario_to_skills", {})
    
    result = []
    for name, info in scenarios.items():
        result.append({
            "name": name,
            "description": info.get("description"),
        })
    
    return json.dumps({"scenarios": result}, indent=2, ensure_ascii=False)


# Tool registry for easy import
DISCOVERY_TOOLS = {
    "discover_skills_by_scenario": discover_skills_by_scenario,
    "discover_skills_by_criteria": discover_skills_by_criteria,
    "get_skill_details": get_skill_details,
    "find_alternative_tools": find_alternative_tools,
    "list_available_scenarios": list_available_scenarios,
}
