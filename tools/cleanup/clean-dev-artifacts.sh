#!/bin/bash

# Script to clean up development artifacts, logs, and temporary files
# Usage: ./clean-dev-artifacts.sh [--no-dry-run] [--no-confirm]

set -e

# Default settings
DRY_RUN=true
CONFIRM=true

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
            echo "Usage: ./clean-dev-artifacts.sh [--no-dry-run] [--no-confirm]"
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

# Function to delete files/directories with confirmation
delete_files() {
    pattern=$1
    description=$2
    
    # Find files/directories matching the pattern
    files=$(find . -path "$pattern" -not -path "*/node_modules/*" -not -path "*/.git/*" | sort)
    
    if [ -z "$files" ]; then
        echo -e "${BLUE}No $description found.${NC}"
        return
    fi
    
    count=$(echo "$files" | wc -l)
    size=$(du -ch $files 2>/dev/null | grep total$ | cut -f1)
    
    echo -e "${YELLOW}Found $count $description (approx. $size)${NC}"
    
    if [ "$DRY_RUN" = true ]; then
        echo -e "${YELLOW}DRY RUN: Would delete the following $description:${NC}"
        echo "$files" | head -n 10
        if [ "$count" -gt 10 ]; then
            echo "... and $(($count - 10)) more files/directories"
        fi
    else
        if confirm "Delete all $description?"; then
            echo -e "${BLUE}Deleting $description...${NC}"
            echo "$files" | xargs rm -rf
            echo -e "${GREEN}Deleted $count $description (approx. $size)${NC}"
        else
            echo -e "${BLUE}Skipping deletion of $description.${NC}"
        fi
    fi
}

echo -e "${BLUE}Starting development artifacts cleanup...${NC}"

# Clean log files
delete_files "*/*.log" "log files"
delete_files "*/logs/*" "log directories"

# Clean IDE/editor specific files
delete_files "*/.vscode/*" "VSCode configuration files"
delete_files "*/.idea/*" "IntelliJ IDEA configuration files"
delete_files "*/.DS_Store" "macOS system files"

# Clean Python cache files
delete_files "*/__pycache__/*" "Python cache files"
delete_files "*.pyc" "Python compiled files"
delete_files "*/.pytest_cache/*" "Pytest cache files"
delete_files "*/.coverage" "Python coverage files"
delete_files "*/htmlcov/*" "HTML coverage reports"

# Clean JavaScript/TypeScript cache and build files
delete_files "*/.nuxt/*" "Nuxt.js build files"
delete_files "*/.next/*" "Next.js build files"
delete_files "*/dist/*" "distribution files"
delete_files "*/build/*" "build files"
delete_files "*/.turbo/*" "Turbo cache files"

# Clean temporary files
delete_files "*/tmp/*" "temporary files"
delete_files "*/.tmp/*" "temporary files"
delete_files "*/temp/*" "temporary files"
delete_files "*/.temp/*" "temporary files"

# Clean npm/yarn cache
delete_files "*/.npm/*" "NPM cache files"
delete_files "*/.yarn/cache/*" "Yarn cache files"

# Clean other common artifacts
delete_files "*/node_modules/.cache/*" "node_modules cache files"
delete_files "*/coverage/*" "test coverage files"
delete_files "*/junit.xml" "JUnit report files"
delete_files "*/tsconfig.tsbuildinfo" "TypeScript build info files"

echo -e "${GREEN}Development artifacts cleanup complete.${NC}"
if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}This was a dry run. To execute file operations, run again with --no-dry-run${NC}"
fi