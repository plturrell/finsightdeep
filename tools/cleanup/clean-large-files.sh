#!/bin/bash

# Script to identify and manage large files in the finsight-monorepo
# Usage: ./clean-large-files.sh [--dry-run] [--min-size-mb SIZE_IN_MB]

set -e

# Default settings
DRY_RUN=true
MIN_SIZE_MB=50
GIT_LFS_ENABLED=false
REPORT_FILE="large-files-report.txt"

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
        --min-size-mb) MIN_SIZE_MB="$2"; shift ;;
        --git-lfs) GIT_LFS_ENABLED=true ;;
        --help) 
            echo "Usage: ./clean-large-files.sh [--no-dry-run] [--min-size-mb SIZE_IN_MB] [--git-lfs]"
            echo ""
            echo "Options:"
            echo "  --no-dry-run      Execute actual file operations (default: dry run only)"
            echo "  --min-size-mb     Minimum file size in MB to consider (default: 50MB)"
            echo "  --git-lfs         Use Git LFS for large files"
            echo "  --help            Show this help message"
            exit 0
            ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

# Check if we're in the monorepo root or at least a git repository
if [ ! -d ".git" ] && [ ! -f "package.json" ]; then
    echo -e "${RED}Error: This script must be run from the repository root${NC}"
    exit 1
fi

echo -e "${BLUE}Scanning for files larger than ${MIN_SIZE_MB}MB...${NC}"

# Create report file
echo "Large Files Report (>${MIN_SIZE_MB}MB)" > "$REPORT_FILE"
echo "Generated on $(date)" >> "$REPORT_FILE"
echo "-----------------------------------" >> "$REPORT_FILE"

# Find large files
find . -type f -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/build/*" -not -path "*/dist/*" -size +${MIN_SIZE_MB}M | sort -r -n | while read file; do
    size=$(du -h "$file" | cut -f1)
    echo "$size $file" >> "$REPORT_FILE"
done

echo -e "${GREEN}Found $(grep -c "^" "$REPORT_FILE" | awk '{print $1-3}') large files. Report saved to $REPORT_FILE${NC}"

# Categorize large files
echo -e "${BLUE}Categorizing large files...${NC}"

declare -A categories
categories["BINARIES"]="\.(exe|dll|so|dylib|bin)$"
categories["ARCHIVES"]="\.(zip|tar|gz|tgz|rar|7z|jar|war)$"
categories["MEDIA"]="\.(jpg|jpeg|png|gif|mp4|mp3|avi|mov|flv|webm|wav|ogg)$"
categories["UNITY"]="\.(unity|unitypackage|asset)$"
categories["DOCUMENTATION"]="\.(pdf|docx|pptx|xlsx)$"
categories["LARGE_TEXT"]="\.(log|sql|json|xml)$"
categories["NODE_BINARIES"]="node_modules/.+\.(node|exe|dll|so|dylib)$"
categories["PYTHON_LIBRARIES"]="(site-packages|dist-packages)/.+\.(so|dylib|dll)$"
categories["OTHER"]=".*"

for category in "${!categories[@]}"; do
    pattern=${categories[$category]}
    count=$(grep -E "$pattern" "$REPORT_FILE" | wc -l)
    if [ "$count" -gt 0 ]; then
        echo -e "${YELLOW}$category: $count files${NC}"
    fi
done

# Create .gitattributes and .gitignore if Git LFS is enabled
if [ "$GIT_LFS_ENABLED" = true ]; then
    echo -e "${BLUE}Setting up Git LFS for large files...${NC}"
    
    # Check if git-lfs is installed
    if ! command -v git-lfs &> /dev/null; then
        echo -e "${RED}Error: git-lfs is not installed. Please install it first.${NC}"
        echo "Brew: brew install git-lfs"
        echo "Ubuntu: apt-get install git-lfs"
        exit 1
    fi
    
    # Initialize Git LFS
    if [ "$DRY_RUN" = false ]; then
        git lfs install
        
        # Create or update .gitattributes
        cat << EOF > .gitattributes
# Archives
*.zip filter=lfs diff=lfs merge=lfs -text
*.tar.gz filter=lfs diff=lfs merge=lfs -text
*.tgz filter=lfs diff=lfs merge=lfs -text
*.rar filter=lfs diff=lfs merge=lfs -text
*.7z filter=lfs diff=lfs merge=lfs -text

# Binaries
*.exe filter=lfs diff=lfs merge=lfs -text
*.dll filter=lfs diff=lfs merge=lfs -text
*.so filter=lfs diff=lfs merge=lfs -text
*.dylib filter=lfs diff=lfs merge=lfs -text
*.bin filter=lfs diff=lfs merge=lfs -text

# Media
*.png filter=lfs diff=lfs merge=lfs -text
*.jpg filter=lfs diff=lfs merge=lfs -text
*.jpeg filter=lfs diff=lfs merge=lfs -text
*.gif filter=lfs diff=lfs merge=lfs -text
*.mp4 filter=lfs diff=lfs merge=lfs -text
*.mp3 filter=lfs diff=lfs merge=lfs -text
*.wav filter=lfs diff=lfs merge=lfs -text

# Unity assets
*.unity filter=lfs diff=lfs merge=lfs -text
*.unitypackage filter=lfs diff=lfs merge=lfs -text
*.asset filter=lfs diff=lfs merge=lfs -text

# Documents
*.pdf filter=lfs diff=lfs merge=lfs -text
*.psd filter=lfs diff=lfs merge=lfs -text
EOF
        
        echo -e "${GREEN}Created .gitattributes for Git LFS${NC}"
    else
        echo -e "${YELLOW}DRY RUN: Would create .gitattributes for Git LFS${NC}"
    fi
fi

# Create a script to deduplicate large binaries
if [ "$DRY_RUN" = false ]; then
    cat << 'EOF' > tools/cleanup/consolidate-binaries.sh
#!/bin/bash

# Script to deduplicate large binary files by replacing them with symbolic links
# Usage: ./consolidate-binaries.sh [--no-dry-run]

DRY_RUN=true

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --no-dry-run) DRY_RUN=false ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

# Create centralized storage for binaries
mkdir -p .shared/binaries

# Find duplicate binary files
echo "Finding duplicate binary files..."
find . -type f -not -path "*/node_modules/*" -not -path "*/.git/*" \
    \( -name "*.exe" -o -name "*.dll" -o -name "*.so" -o -name "*.dylib" -o -name "*.bin" \) \
    -exec md5sum {} \; | sort | uniq -w32 -d --all-repeated=separate > duplicates.txt

if [ ! -s duplicates.txt ]; then
    echo "No duplicate binary files found."
    rm duplicates.txt
    exit 0
fi

# Process duplicates
echo "Processing duplicate files..."
while read -r hash file; do
    # Skip empty lines
    [ -z "$hash" ] && continue
    
    # Get base filename
    filename=$(basename "$file")
    target_dir=$(dirname "$file")
    
    # Check if this hash is already processed
    if [ -f ".shared/binaries/${hash}_${filename}" ]; then
        echo "Replacing $file with symbolic link"
        if [ "$DRY_RUN" = false ]; then
            rm "$file"
            ln -s "$(pwd)/.shared/binaries/${hash}_${filename}" "$file"
        else
            echo "DRY RUN: Would replace $file with symbolic link"
        fi
    else
        echo "Moving $file to shared storage"
        if [ "$DRY_RUN" = false ]; then
            mv "$file" ".shared/binaries/${hash}_${filename}"
            ln -s "$(pwd)/.shared/binaries/${hash}_${filename}" "$file"
        else
            echo "DRY RUN: Would move $file to shared storage"
        fi
    fi
done < duplicates.txt

rm duplicates.txt
echo "Binary file deduplication complete."
EOF
    chmod +x tools/cleanup/consolidate-binaries.sh
    echo -e "${GREEN}Created script to deduplicate binary files: tools/cleanup/consolidate-binaries.sh${NC}"
else
    echo -e "${YELLOW}DRY RUN: Would create script to deduplicate binary files${NC}"
fi

# Add commonly large directories to .gitignore
if [ "$DRY_RUN" = false ]; then
    # Update .gitignore if it exists, otherwise create it
    if [ -f ".gitignore" ]; then
        # Append to .gitignore if entries don't exist
        cat << EOF >> .gitignore

# Large directories to ignore
.shared/binaries/
**/*.log
**/logs/
**/coverage/
**/tmp/
**/.tmp/
**/temp/
**/.temp/
**/build/
**/dist/
**/.nuxt/
**/.next/
**/.output/
**/node_modules/
**/venv/
**/.venv/
**/env/
**/.env/
**/__pycache__/
**/*.pyc
**/*.pyo
**/*.pyd
**/.DS_Store
**/.idea/
**/.vscode/
EOF
        echo -e "${GREEN}Updated .gitignore with large directories${NC}"
    else
        # Create new .gitignore
        cat << EOF > .gitignore
# Large directories to ignore
.shared/binaries/
**/*.log
**/logs/
**/coverage/
**/tmp/
**/.tmp/
**/temp/
**/.temp/
**/build/
**/dist/
**/.nuxt/
**/.next/
**/.output/
**/node_modules/
**/venv/
**/.venv/
**/env/
**/.env/
**/__pycache__/
**/*.pyc
**/*.pyo
**/*.pyd
**/.DS_Store
**/.idea/
**/.vscode/
EOF
        echo -e "${GREEN}Created .gitignore for large directories${NC}"
    fi
else
    echo -e "${YELLOW}DRY RUN: Would update .gitignore for large directories${NC}"
fi

echo -e "${GREEN}Large files analysis complete.${NC}"
echo ""
echo -e "${BLUE}Recommendations:${NC}"
echo "1. Review $REPORT_FILE to identify unnecessary large files"
echo "2. Consider moving large media files to external storage or CDN"
echo "3. Use Git LFS for tracking large files that must be versioned (--git-lfs option)"
echo "4. Run consolidate-binaries.sh to deduplicate binary files"
echo "5. Remove large log files and build artifacts"
echo "6. Add large generated files to .gitignore"
echo ""
echo -e "${YELLOW}To execute file operations, run again with --no-dry-run${NC}"