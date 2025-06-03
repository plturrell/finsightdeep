#!/bin/bash

# Script to analyze code duplication across the monorepo
# Usage: ./analyze-code-duplication.sh [--no-dry-run] [--min-lines N] [--language js,ts,py,...]

set -e

# Default settings
DRY_RUN=true
MIN_LINES=10
LANGUAGES="js,ts,jsx,tsx,py,java,cpp,c,sh"
REPORT_FILE="code-duplication-report.md"

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
        --min-lines) MIN_LINES="$2"; shift ;;
        --language|--languages) LANGUAGES="$2"; shift ;;
        --help) 
            echo "Usage: ./analyze-code-duplication.sh [--no-dry-run] [--min-lines N] [--language js,ts,py,...]"
            echo ""
            echo "Options:"
            echo "  --no-dry-run      Execute actual file operations (default: dry run only)"
            echo "  --min-lines       Minimum number of duplicate lines to detect (default: 10)"
            echo "  --languages       Comma-separated list of file extensions to analyze"
            echo "                    Default: js,ts,jsx,tsx,py,java,cpp,c,sh"
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

# Check for required tools
if ! command -v jq &> /dev/null; then
    echo -e "${RED}Error: jq is required but not installed. Please install it first.${NC}"
    echo "Brew: brew install jq"
    echo "Ubuntu: apt-get install jq"
    exit 1
fi

# Create language pattern for find
lang_pattern=$(echo "$LANGUAGES" | sed 's/,/\\|/g')

echo -e "${BLUE}Analyzing code duplication with minimum $MIN_LINES lines...${NC}"
echo -e "${BLUE}Languages: ${LANGUAGES}${NC}"

# Function to find duplicate code blocks
find_duplicates() {
    # Create directory to store temporary files
    mkdir -p .tmp_duplication
    
    # Find all code files
    echo -e "${BLUE}Finding code files...${NC}"
    find . -type f -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/dist/*" -not -path "*/build/*" | grep -E "\.(${lang_pattern})$" > .tmp_duplication/all_files.txt
    
    total_files=$(wc -l < .tmp_duplication/all_files.txt)
    echo -e "${GREEN}Found $total_files files to analyze${NC}"
    
    # Initialize report file
    echo "# Code Duplication Analysis Report" > "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "Generated on: $(date)" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "## Summary" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    
    # Split languages for separate analysis
    IFS=',' read -ra LANG_ARRAY <<< "$LANGUAGES"
    
    total_duplicates=0
    
    for lang in "${LANG_ARRAY[@]}"; do
        echo -e "${BLUE}Analyzing $lang files...${NC}"
        
        # Find all files of this language
        find . -type f -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/dist/*" -not -path "*/build/*" -name "*.$lang" > .tmp_duplication/files_${lang}.txt
        
        lang_files=$(wc -l < .tmp_duplication/files_${lang}.txt)
        
        if [ "$lang_files" -eq 0 ]; then
            echo -e "${YELLOW}No $lang files found, skipping${NC}"
            continue
        fi
        
        echo -e "${GREEN}Found $lang_files $lang files${NC}"
        
        # Create a temporary JSON structure for analysis
        echo "[" > .tmp_duplication/files_${lang}.json
        first=true
        
        while read -r file; do
            if [ "$first" = true ]; then
                first=false
            else
                echo "," >> .tmp_duplication/files_${lang}.json
            fi
            
            # Escape file path for JSON
            escaped_file=$(echo "$file" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g')
            
            # Add file content to JSON
            echo "{\"path\":\"$escaped_file\",\"content\":\"$(cat "$file" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g' | sed 's/\n/\\n/g')\"}" >> .tmp_duplication/files_${lang}.json
        done < .tmp_duplication/files_${lang}.txt
        
        echo "]" >> .tmp_duplication/files_${lang}.json
        
        # Simple n^2 comparison for duplication
        duplicate_count=0
        echo "" >> "$REPORT_FILE"
        echo "## $lang Files" >> "$REPORT_FILE"
        echo "" >> "$REPORT_FILE"
        
        # Analyze file pairs
        while read -r file1; do
            while read -r file2; do
                if [ "$file1" != "$file2" ]; then
                    # Extract common lines
                    common_lines=$(comm -12 <(sort "$file1") <(sort "$file2") | wc -l)
                    
                    if [ "$common_lines" -ge "$MIN_LINES" ]; then
                        duplicate_count=$((duplicate_count + 1))
                        total_duplicates=$((total_duplicates + 1))
                        
                        rel_file1=$(echo "$file1" | sed "s|^./||")
                        rel_file2=$(echo "$file2" | sed "s|^./||")
                        
                        echo "### Duplication #$duplicate_count: $rel_file1 and $rel_file2" >> "$REPORT_FILE"
                        echo "" >> "$REPORT_FILE"
                        echo "Found $common_lines common lines" >> "$REPORT_FILE"
                        echo "" >> "$REPORT_FILE"
                        echo "#### Sample of common code:" >> "$REPORT_FILE"
                        echo "" >> "$REPORT_FILE"
                        echo '```'"$lang" >> "$REPORT_FILE"
                        comm -12 <(sort "$file1") <(sort "$file2") | head -n 20 >> "$REPORT_FILE"
                        echo "..." >> "$REPORT_FILE"
                        echo '```' >> "$REPORT_FILE"
                        echo "" >> "$REPORT_FILE"
                    fi
                fi
            done < .tmp_duplication/files_${lang}.txt
        done < .tmp_duplication/files_${lang}.txt
        
        echo "Found $duplicate_count duplications in $lang files" >> "$REPORT_FILE"
    done
    
    # Update summary
    sed -i.bak "s/## Summary/## Summary\n\nTotal files analyzed: $total_files\nTotal duplications found: $total_duplicates\nMinimum lines threshold: $MIN_LINES\nLanguages analyzed: $LANGUAGES/" "$REPORT_FILE"
    rm "$REPORT_FILE.bak"
    
    # Clean up temporary files
    rm -rf .tmp_duplication
    
    echo -e "${GREEN}Duplication analysis complete. Results saved to $REPORT_FILE${NC}"
}

# Function to create a deduplicated shared library
create_shared_library() {
    if [ "$DRY_RUN" = false ]; then
        echo -e "${BLUE}Creating shared library structure...${NC}"
        
        # Create shared library directories
        mkdir -p packages/utils/src/js
        mkdir -p packages/utils/src/python
        
        # Create README files
        cat << EOF > packages/utils/README.md
# Shared Utilities Library

This package contains shared utilities extracted from duplicate code across the monorepo.

## Usage

### JavaScript/TypeScript
\`\`\`js
import { formatDate } from '@finsight/utils/js/date';
\`\`\`

### Python
\`\`\`python
from finsight.utils.date import format_date
\`\`\`

## Contributing

When you identify duplicate code, extract it to this library and replace the duplicates
with imports from this shared library.
EOF
        
        # Create package.json
        cat << EOF > packages/utils/package.json
{
  "name": "@finsight/utils",
  "version": "1.0.0",
  "description": "Shared utility functions for FinSight",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "test": "jest",
    "lint": "eslint src"
  },
  "dependencies": {},
  "devDependencies": {
    "typescript": "^5.1.6",
    "jest": "^29.5.0",
    "@types/jest": "^29.5.0",
    "eslint": "^8.46.0"
  }
}
EOF
        
        # Create Python setup.py
        cat << EOF > packages/utils/setup.py
from setuptools import setup, find_packages

setup(
    name="finsight-utils",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    description="Shared utility functions for FinSight",
    author="FinSight Team",
    python_requires=">=3.8",
)
EOF
        
        echo -e "${GREEN}Created shared library structure in packages/utils${NC}"
        echo -e "${YELLOW}Review $REPORT_FILE and move common code to the shared library${NC}"
    else
        echo -e "${YELLOW}DRY RUN: Would create shared library structure in packages/utils${NC}"
    fi
}

# Find duplicate code
find_duplicates

# Create shared library structure
create_shared_library

echo -e "${GREEN}Code duplication analysis complete.${NC}"
echo -e "${BLUE}Next steps:${NC}"
echo "1. Review $REPORT_FILE to identify common code patterns"
echo "2. Extract common functionality to shared packages"
echo "3. Replace duplicate code with imports from shared packages"
echo "4. Run this analysis again to verify improvement"
echo ""

if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}This was a dry run. To create the shared library structure, run again with --no-dry-run${NC}"
fi