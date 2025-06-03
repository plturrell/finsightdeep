#!/bin/bash

# Script to clean up redundant documentation and consolidate essential docs
# Usage: ./clean-documentation.sh [--no-dry-run] [--no-confirm]

set -e

# Default settings
DRY_RUN=true
CONFIRM=true
DOCS_DIR="docs"
EXCLUDED_EXTENSIONS="md,txt,html"
EXCLUDED_FILES="README.md,LICENSE,CHANGELOG.md,CONTRIBUTING.md,CODE_OF_CONDUCT.md"

# Set colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --no-dry-run) DRY_RUN=false ;;
        --no-confirm) CONFIRM=false ;;
        --help) 
            echo "Usage: ./clean-documentation.sh [--no-dry-run] [--no-confirm]"
            echo ""
            echo "Options:"
            echo "  --no-dry-run      Execute actual file operations (default: dry run only)"
            echo "  --no-confirm      Skip confirmation prompts"
            echo "  --help            Show this help message"
            exit 0
            ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

# Check if we're in the monorepo root
if [ ! -f "package.json" ] || [ ! -d "apps" ] || [ ! -d "packages" ]; then
    echo -e "${RED}Error: This script must be run from the root finsight-monorepo directory${NC}"
    exit 1
fi

# Ensure docs directory exists
if [ ! -d "$DOCS_DIR" ]; then
    if [ "$DRY_RUN" = false ]; then
        mkdir -p "$DOCS_DIR"
        echo -e "${GREEN}Created $DOCS_DIR directory${NC}"
    else
        echo -e "${YELLOW}DRY RUN: Would create $DOCS_DIR directory${NC}"
    fi
fi

# Function to confirm before proceeding
confirm() {
    if [ "$CONFIRM" = true ]; then
        read -p "$1 (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            return 1
        fi
    fi
    return 0
}

# Function to find duplicate documentation files
find_duplicates() {
    echo -e "${BLUE}Finding duplicate documentation files...${NC}"
    
    # Temp file for results
    results_file="duplicate_docs.txt"
    : > "$results_file"
    
    # Find all markdown files except excluded ones
    excluded_files_pattern=$(echo "$EXCLUDED_FILES" | tr ',' '|')
    excluded_dirs="node_modules|.git|dist|build"
    
    find . -type f -name "*.md" | grep -v -E "($excluded_files_pattern)$" | grep -v -E "/($excluded_dirs)/" | sort > all_md_files.txt
    
    # Check for files with similar names
    cat all_md_files.txt | xargs -I{} basename {} | sort | uniq -d > duplicate_names.txt
    
    # Check for files with similar content
    if [ -s duplicate_names.txt ]; then
        while read -r filename; do
            echo -e "${YELLOW}Found files with similar name: $filename${NC}"
            grep -l "$filename$" all_md_files.txt | tee -a "$results_file"
            echo "" >> "$results_file"
        done < duplicate_names.txt
    fi
    
    # Check for very similar content
    while read -r file1; do
        while read -r file2; do
            if [ "$file1" != "$file2" ] && [ -f "$file1" ] && [ -f "$file2" ]; then
                similarity=$(diff -y --suppress-common-lines "$file1" "$file2" | wc -l)
                file1_lines=$(wc -l < "$file1")
                file2_lines=$(wc -l < "$file2")
                max_lines=$(( file1_lines > file2_lines ? file1_lines : file2_lines ))
                
                if [ "$max_lines" -gt 0 ] && [ "$similarity" -lt $(( max_lines / 2 )) ]; then
                    echo -e "${YELLOW}Found files with similar content:${NC}"
                    echo "$file1" | tee -a "$results_file"
                    echo "$file2" | tee -a "$results_file"
                    echo "" >> "$results_file"
                fi
            fi
        done < all_md_files.txt
    done < all_md_files.txt
    
    # Cleanup temp files
    rm all_md_files.txt duplicate_names.txt 2>/dev/null || true
    
    if [ -s "$results_file" ]; then
        echo -e "${YELLOW}Found potentially duplicate documentation. See $results_file for details.${NC}"
    else
        echo -e "${GREEN}No duplicate documentation found.${NC}"
        rm "$results_file" 2>/dev/null || true
    fi
}

# Function to consolidate documentation
consolidate_docs() {
    echo -e "${BLUE}Consolidating documentation...${NC}"
    
    # Find all markdown files in subprojects that aren't README.md
    docs_to_consolidate=$(find apps packages -type f -name "*.md" | grep -v -E "(README.md|LICENSE|CHANGELOG.md|CONTRIBUTING.md|CODE_OF_CONDUCT.md)$" | grep -v -E "/(node_modules|.git|dist|build)/")
    
    if [ -z "$docs_to_consolidate" ]; then
        echo -e "${BLUE}No additional documentation files to consolidate.${NC}"
        return
    fi
    
    count=$(echo "$docs_to_consolidate" | wc -l)
    echo -e "${YELLOW}Found $count documentation files that could be consolidated.${NC}"
    
    if [ "$DRY_RUN" = true ]; then
        echo -e "${YELLOW}DRY RUN: Would consolidate these files into $DOCS_DIR:${NC}"
        echo "$docs_to_consolidate" | head -n 10
        if [ "$count" -gt 10 ]; then
            echo "... and $(($count - 10)) more files"
        fi
    else
        if confirm "Consolidate all documentation into $DOCS_DIR?"; then
            echo -e "${BLUE}Consolidating documentation...${NC}"
            
            while read -r file; do
                # Create subdirectory based on project
                rel_path=$(echo "$file" | sed 's|^[^/]*/[^/]*/||')
                dir_path=$(dirname "$rel_path")
                target_dir="$DOCS_DIR/$dir_path"
                
                # Create target directory
                mkdir -p "$target_dir"
                
                # Copy file to target directory
                cp "$file" "$target_dir/"
                
                # Create symlink to the original file
                ln -sf "$(pwd)/$target_dir/$(basename "$file")" "$file"
                
                echo "Consolidated: $file -> $target_dir/$(basename "$file")"
            done <<< "$docs_to_consolidate"
            
            echo -e "${GREEN}Documentation consolidation complete.${NC}"
        else
            echo -e "${BLUE}Skipping documentation consolidation.${NC}"
        fi
    fi
}

# Function to remove non-essential documentation formats
remove_non_essential() {
    echo -e "${BLUE}Identifying non-essential documentation formats...${NC}"
    
    # Find documentation in formats other than the excluded extensions
    excluded_exts_pattern=$(echo "$EXCLUDED_EXTENSIONS" | tr ',' '|')
    excluded_dirs="node_modules|.git|dist|build"
    
    non_essential=$(find . -type f -path "*/docs/*" | grep -v -E "\.($excluded_exts_pattern)$" | grep -v -E "/($excluded_dirs)/")
    
    if [ -z "$non_essential" ]; then
        echo -e "${BLUE}No non-essential documentation formats found.${NC}"
        return
    fi
    
    count=$(echo "$non_essential" | wc -l)
    echo -e "${YELLOW}Found $count files in non-essential formats.${NC}"
    
    if [ "$DRY_RUN" = true ]; then
        echo -e "${YELLOW}DRY RUN: Would remove these non-essential documentation files:${NC}"
        echo "$non_essential" | head -n 10
        if [ "$count" -gt 10 ]; then
            echo "... and $(($count - 10)) more files"
        fi
    else
        if confirm "Remove all non-essential documentation formats?"; then
            echo -e "${BLUE}Removing non-essential documentation formats...${NC}"
            echo "$non_essential" | xargs rm -f
            echo -e "${GREEN}Removed $count non-essential documentation files.${NC}"
        else
            echo -e "${BLUE}Skipping removal of non-essential documentation formats.${NC}"
        fi
    fi
}

# Find duplicate documentation
find_duplicates

# Consolidate documentation
consolidate_docs

# Remove non-essential documentation formats
remove_non_essential

# Create documentation index if not in dry run mode
if [ "$DRY_RUN" = false ]; then
    echo -e "${BLUE}Creating documentation index...${NC}"
    
    # Create index.md
    cat << EOF > "$DOCS_DIR/index.md"
# FinSight Documentation Index

This is the consolidated documentation for the FinSight platform. 

## Project Structure

- [Development](development/)
  - [Dependency Management](development/dependency-management.md)
  - [Git Workflow](development/git-workflow.md)
  - [Testing](development/testing.md)
  
- [Deployment](deployment/)
  - [Kubernetes](deployment/kubernetes.md)
  - [Docker](deployment/docker.md)
  - [NVIDIA Deployment](deployment/nvidia-deployment.md)
  
- [APIs](apis/)
  - [REST API](apis/rest-api.md)
  - [GraphQL API](apis/graphql-api.md)
  
- [Security](security/)
  - [Authentication](security/authentication.md)
  - [Authorization](security/authorization.md)
  
- [Apps](apps/)
  - [AI Engine](apps/ai-engine.md)
  - [Data Platform](apps/data-platform.md)
  - [Web Dashboard](apps/web-dashboard.md)
  - [Utils](apps/utils.md)

## Common Tasks

- [Getting Started](getting-started.md)
- [Contributing](contributing.md)
- [FAQ](faq.md)
EOF
    
    echo -e "${GREEN}Created documentation index at $DOCS_DIR/index.md${NC}"
fi

echo -e "${GREEN}Documentation cleanup complete.${NC}"
if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}This was a dry run. To execute file operations, run again with --no-dry-run${NC}"
fi