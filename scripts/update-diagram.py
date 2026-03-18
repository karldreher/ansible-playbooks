#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Generate a Mermaid DAG diagram of Ansible role dependencies."""

import sys
from pathlib import Path

import yaml

ROLES_DIR = Path("roles")
OUTPUT_FILE = Path("DAG.md")

STYLE_DEFS = """\
    classDef facts fill:#4a9eff,stroke:#2b7de9,color:#fff
    classDef role fill:#2d2d2d,stroke:#555,color:#fff
    classDef default fill:#2d2d2d,stroke:#555,color:#fff"""


def _dep_name(dep: str | dict) -> str | None:
    """Extract role name from a dependency entry."""
    if isinstance(dep, dict) and "role" in dep:
        return dep["role"]
    if isinstance(dep, str):
        return dep
    return None


def parse_role_dependencies(roles_dir: Path) -> dict[str, list[str]]:
    """Parse all meta/main.yml files and return {role: [dependencies]}."""
    graph: dict[str, list[str]] = {}
    for meta_file in sorted(roles_dir.glob("*/meta/main.yml")):
        role_name = meta_file.parent.parent.name
        meta = yaml.safe_load(meta_file.read_text())
        graph[role_name] = [name for dep in (meta.get("dependencies") or []) if (name := _dep_name(dep))]

    for role_dir in sorted(roles_dir.iterdir()):
        if role_dir.is_dir() and role_dir.name not in graph:
            graph[role_dir.name] = []

    return graph


def generate_mermaid(graph: dict[str, list[str]]) -> str:
    """Generate a Mermaid diagram string from the dependency graph."""
    edges = []
    for role, deps in sorted(graph.items()):
        if deps:
            edges.extend(f"    {role} -->|depends on| {dep}" for dep in sorted(deps))
        else:
            edges.append(f"    {role}")

    sections = [
        "```mermaid",
        "graph TD",
        "",
        *edges,
        "",
        STYLE_DEFS,
        "    class facts facts",
        "```",
        "",
    ]
    return "\n".join(sections)


def main() -> None:
    if not ROLES_DIR.is_dir():
        sys.exit(f"Error: {ROLES_DIR} directory not found. Run from the repo root.")

    graph = parse_role_dependencies(ROLES_DIR)
    mermaid = generate_mermaid(graph)
    OUTPUT_FILE.write_text(mermaid)

    role_count = len(graph)
    edge_count = sum(len(deps) for deps in graph.values())
    print(f"Generated {OUTPUT_FILE}: {role_count} roles, {edge_count} edges")


if __name__ == "__main__":
    main()
