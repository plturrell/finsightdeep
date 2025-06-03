#!/bin/bash

# Master script to orchestrate all cleanup operations
# Usage: ./cleanup-project.sh [--no-dry-run] [--skip STEP1,STEP2,...] [--only STEP1,STEP2,...]

set -e

# Default settings
DRY_RUN=true
SKIP_STEPS=""
ONLY_STEPS=""
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
        --skip) SKIP_STEPS="$2"; shift ;;
        --only) ONLY_STEPS="$2"; shift ;;
        --help) 
            echo "Usage: ./cleanup-project.sh [--no-dry-run] [--no-confirm] [--skip STEP1,STEP2,...] [--only STEP1,STEP2,...]"
            echo ""
            echo "Options:"
            echo "  --no-dry-run      Execute actual file operations (default: dry run only)"
            echo "  --no-confirm      Skip confirmation prompts"
            echo "  --skip            Comma-separated list of steps to skip"
            echo "                    Available steps: large-files, dev-artifacts, documentation, duplication"
            echo "  --only            Comma-separated list of steps to run (overrides --skip)"
            echo "                    Available steps: large-files, dev-artifacts, documentation, duplication"
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

# Function to check if a step should be run
should_run_step() {
    step=$1
    
    # If only steps are specified, check if this step is included
    if [ -n "$ONLY_STEPS" ]; then
        if [[ "$ONLY_STEPS" =~ (^|,)$step(,|$) ]]; then
            return 0
        else
            return 1
        fi
    fi
    
    # If skip steps are specified, check if this step is excluded
    if [ -n "$SKIP_STEPS" ]; then
        if [[ "$SKIP_STEPS" =~ (^|,)$step(,|$) ]]; then
            return 1
        else
            return 0
        fi
    fi
    
    # By default, run all steps
    return 0
}

# Function to run a cleanup script
run_cleanup_script() {
    script=$1
    step=$2
    description=$3
    args=$4
    
    if should_run_step "$step"; then
        echo -e "\n${BLUE}=======================================================${NC}"
        echo -e "${BLUE}Running $description...${NC}"
        echo -e "${BLUE}=======================================================${NC}\n"
        
        dry_run_arg=""
        if [ "$DRY_RUN" = false ]; then
            dry_run_arg="--no-dry-run"
        fi
        
        confirm_arg=""
        if [ "$CONFIRM" = false ]; then
            confirm_arg="--no-confirm"
        fi
        
        # Combine args
        combined_args="$dry_run_arg $confirm_arg $args"
        
        # Run the script
        "tools/cleanup/$script" $combined_args
        
        echo -e "\n${GREEN}$description completed.${NC}\n"
    else
        echo -e "\n${YELLOW}Skipping $description.${NC}\n"
    fi
}

# Print header
echo -e "${BLUE}=======================================================${NC}"
echo -e "${BLUE}                FinSight Project Cleanup                ${NC}"
echo -e "${BLUE}=======================================================${NC}\n"

echo -e "${YELLOW}This script will run the following cleanup operations:${NC}"
echo "1. Large files management"
echo "2. Development artifacts cleanup"
echo "3. Documentation cleanup and consolidation"
echo "4. Code duplication analysis"
echo ""

if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}Running in DRY RUN mode. No files will be modified.${NC}"
    echo -e "${YELLOW}To execute actual changes, run with --no-dry-run flag.${NC}\n"
fi

if ! confirm "Do you want to proceed with the cleanup?"; then
    echo -e "${RED}Cleanup aborted.${NC}"
    exit 0
fi

# Create a log directory
mkdir -p logs

# Get timestamp for logs
timestamp=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="logs/cleanup_${timestamp}.log"

echo -e "${BLUE}Logging output to $LOG_FILE${NC}\n"

# Start logging
exec > >(tee -a "$LOG_FILE") 2>&1

# Run each cleanup script
run_cleanup_script "clean-large-files.sh" "large-files" "Large files management" "--min-size-mb 50"
run_cleanup_script "clean-dev-artifacts.sh" "dev-artifacts" "Development artifacts cleanup" ""
run_cleanup_script "clean-documentation.sh" "documentation" "Documentation cleanup" ""
run_cleanup_script "analyze-code-duplication.sh" "duplication" "Code duplication analysis" "--min-lines 10"

# Update .gitignore if it doesn't already include our log directory
if [ "$DRY_RUN" = false ]; then
    if ! grep -q "^logs/" .gitignore 2>/dev/null; then
        echo "logs/" >> .gitignore
        echo -e "${GREEN}Added logs/ to .gitignore${NC}"
    fi
fi

# Create a summary report
cat << EOF > cleanup-summary.md
# Project Cleanup Summary

Date: $(date)

## Actions Performed
EOF

if should_run_step "large-files"; then
    echo "- Large files management: Identified and managed files larger than 50MB" >> cleanup-summary.md
    if [ -f "large-files-report.txt" ]; then
        echo "  - See [large-files-report.txt](large-files-report.txt) for details" >> cleanup-summary.md
    fi
fi

if should_run_step "dev-artifacts"; then
    echo "- Development artifacts cleanup: Removed logs, caches, and temporary files" >> cleanup-summary.md
fi

if should_run_step "documentation"; then
    echo "- Documentation cleanup: Consolidated and organized documentation" >> cleanup-summary.md
    if [ -f "duplicate_docs.txt" ]; then
        echo "  - See [duplicate_docs.txt](duplicate_docs.txt) for details" >> cleanup-summary.md
    fi
fi

if should_run_step "duplication"; then
    echo "- Code duplication analysis: Identified redundant code patterns" >> cleanup-summary.md
    if [ -f "code-duplication-report.md" ]; then
        echo "  - See [code-duplication-report.md](code-duplication-report.md) for details" >> cleanup-summary.md
    fi
fi

cat << EOF >> cleanup-summary.md

## Next Steps

1. Review the generated reports to understand the state of the codebase
2. Address any remaining large files using Git LFS or external storage
3. Consolidate duplicated code into shared libraries
4. Set up automated cleanup as part of CI/CD process

## Log

The complete log of this cleanup operation is available at \`$LOG_FILE\`.
EOF

echo -e "\n${GREEN}Cleanup complete! Summary available in cleanup-summary.md${NC}"
echo -e "${BLUE}Next steps:${NC}"
echo "1. Review the generated reports and summary"
echo "2. Commit the changes if satisfied"
echo "3. Continue developing with a cleaner codebase"
echo ""

if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}This was a dry run. To execute actual changes, run with --no-dry-run flag.${NC}"
fi