#!/bin/bash
#
# Generates a Mermaid DAG diagram of Ansible role dependencies.
#
set -e

OUTPUT_FILE="DAG.md"

# Check if yq is installed
if ! command -v yq &> /dev/null
then
    echo "yq could not be found, please install it to continue."
    exit 1
fi

# Start the Mermaid diagram
echo "\`\`\`mermaid" > "$OUTPUT_FILE"
echo "graph TD" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Find all meta/main.yml files and process them
for meta_file in $(find roles -path '*/meta/main.yml'); do
    role_path=$(dirname $(dirname "$meta_file"))
    role_name=$(basename "$role_path")

    # Use yq to parse dependencies
    dependencies=$(yq e '.dependencies[].role' "$meta_file" 2>/dev/null || true)

    if [ -n "$dependencies" ]; then
        for dep in $dependencies; do
            echo "    $role_name -->|depends on| $dep" >> "$OUTPUT_FILE"
        done
    else
        # If a role has no dependencies, just list it
        echo "    $role_name" >> "$OUTPUT_FILE"
    fi
done
echo "\`\`\`" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "Diagram generated in $OUTPUT_FILE"
