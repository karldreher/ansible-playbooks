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

COLORS = {
    "facts": ":::facts",
    "default": "",
}

STYLE_DEFS = """
    classDef facts fill:#4a9eff,stroke:#2b7de9,color:#fff
    classDef role fill:#2d2d2d,stroke:#555,color:#fff
    classDef default fill:#2d2d2d,stroke:#555,color:#fff
"""


def parse_role_dependencies(roles_dir: Path) -> dict[str, list[str]]:
    """Parse all meta/main.yml files and return {role: [dependencies]}."""
    graph: dict[str, list[str]] = {}
    for meta_file in sorted(roles_dir.glob("*/meta/main.yml")):
        role_name = meta_file.parent.parent.name
        with open(meta_file) as f:
            meta = yaml.safe_load(f)
        deps = []
        for dep in meta.get("dependencies", []) or []:
            if isinstance(dep, dict) and "role" in dep:
                deps.append(dep["role"])
            elif isinstance(dep, str):
                deps.append(dep)
        graph[role_name] = deps

    # Include roles that have no meta file (no dependencies)
    for role_dir in sorted(roles_dir.iterdir()):
        if role_dir.is_dir() and role_dir.name not in graph:
            graph[role_dir.name] = []

    return graph


def generate_mermaid(graph: dict[str, list[str]]) -> str:
    """Generate a Mermaid diagram string from the dependency graph."""
    lines = ["```mermaid", "graph TD", ""]

    for role, deps in sorted(graph.items()):
        if deps:
            for dep in sorted(deps):
                lines.append(f"    {role} -->|depends on| {dep}")
        else:
            lines.append(f"    {role}")

    lines.append(STYLE_DEFS.rstrip())

    # Apply class to facts node
    lines.append("    class facts facts")

    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    if not ROLES_DIR.is_dir():
        print(f"Error: {ROLES_DIR} directory not found. Run from the repo root.", file=sys.stderr)
        return 1

    graph = parse_role_dependencies(ROLES_DIR)
    mermaid = generate_mermaid(graph)

    OUTPUT_FILE.write_text(mermaid)

    role_count = len(graph)
    edge_count = sum(len(deps) for deps in graph.values())
    print(f"Generated {OUTPUT_FILE}: {role_count} roles, {edge_count} edges")
    return 0


if __name__ == "__main__":
    sys.exit(main())
