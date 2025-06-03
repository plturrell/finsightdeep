#!/bin/bash

# Script to set up the project environment
# Usage: ./setup-project-env.sh [--no-confirm]

set -e

# Default settings
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
        --no-confirm) CONFIRM=false ;;
        --help) 
            echo "Usage: ./setup-project-env.sh [--no-confirm]"
            echo ""
            echo "Options:"
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

echo -e "${BLUE}Setting up FinSight project environment...${NC}"

# Create GitHub workflow directory
mkdir -p .github/workflows

# Copy GitHub workflow template
if confirm "Set up CI/CD workflow?"; then
    cp project/ci/github-workflow-template.yml .github/workflows/ci-cd.yml
    echo -e "${GREEN}Created CI/CD workflow at .github/workflows/ci-cd.yml${NC}"
fi

# Create contributing guidelines
if [ ! -f "CONTRIBUTING.md" ] && confirm "Create CONTRIBUTING.md?"; then
    cat << EOF > CONTRIBUTING.md
# Contributing to FinSight

Thank you for your interest in contributing to the FinSight platform!

## Development Process

1. Fork the repository
2. Create your feature branch (\`git checkout -b feature/amazing-feature\`)
3. Commit your changes using conventional commits (\`git commit -m "feat: add amazing feature"\`)
4. Push to the branch (\`git push origin feature/amazing-feature\`)
5. Open a Pull Request

## Development Guidelines

Please refer to our [Development Guidelines](project/docs/guidelines/development.md) for detailed information on:

- Code style and formatting
- Testing requirements
- Documentation standards
- Git workflow

## Pull Request Process

1. Ensure your code follows our style guidelines
2. Update documentation as needed
3. Include tests for new functionality
4. Ensure all tests pass
5. The PR should be reviewed by at least one maintainer

## Code of Conduct

Please be respectful and inclusive when contributing to this project. We expect all contributors to adhere to professional standards of communication and behavior.
EOF
    echo -e "${GREEN}Created CONTRIBUTING.md${NC}"
fi

# Create .editorconfig
if [ ! -f ".editorconfig" ] && confirm "Create .editorconfig?"; then
    cat << EOF > .editorconfig
# EditorConfig helps maintain consistent coding styles
# See: https://editorconfig.org

root = true

[*]
charset = utf-8
end_of_line = lf
indent_size = 2
indent_style = space
insert_final_newline = true
max_line_length = 100
trim_trailing_whitespace = true

[*.md]
trim_trailing_whitespace = false

[*.py]
indent_size = 4

[*.{js,jsx,ts,tsx}]
indent_size = 2

[Makefile]
indent_style = tab
EOF
    echo -e "${GREEN}Created .editorconfig${NC}"
fi

# Set up pre-commit hooks
if confirm "Set up pre-commit hooks?"; then
    cat << EOF > .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files
        args: ['--maxkb=500']
      - id: check-merge-conflict
      - id: mixed-line-ending
        args: ['--fix=lf']

  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.0.0
    hooks:
      - id: prettier
        types_or: [javascript, jsx, ts, tsx, json, css, markdown]

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.0.270
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
EOF
    echo -e "${GREEN}Created .pre-commit-config.yaml${NC}"
    
    if command -v pre-commit &> /dev/null && confirm "Install pre-commit hooks?"; then
        pre-commit install
        echo -e "${GREEN}Installed pre-commit hooks${NC}"
    else
        echo -e "${YELLOW}pre-commit not found. Please install with 'pip install pre-commit' and then run 'pre-commit install'${NC}"
    fi
fi

# Set up VSCode settings
if confirm "Set up VSCode settings?"; then
    mkdir -p .vscode
    cat << EOF > .vscode/settings.json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[python]": {
    "editor.defaultFormatter": "ms-python.python"
  },
  "eslint.validate": [
    "javascript",
    "javascriptreact",
    "typescript",
    "typescriptreact"
  ],
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "typescript.tsdk": "node_modules/typescript/lib",
  "cSpell.words": [
    "finsight",
    "pnpm"
  ],
  "search.exclude": {
    "**/node_modules": true,
    "**/dist": true,
    "**/build": true,
    "**/.venv": true
  }
}
EOF
    echo -e "${GREEN}Created .vscode/settings.json${NC}"
    
    cat << EOF > .vscode/extensions.json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "ms-python.python",
    "ms-python.vscode-pylance",
    "streetsidesoftware.code-spell-checker",
    "editorconfig.editorconfig",
    "mikestead.dotenv",
    "github.vscode-pull-request-github",
    "ms-azuretools.vscode-docker",
    "ms-kubernetes-tools.vscode-kubernetes-tools"
  ]
}
EOF
    echo -e "${GREEN}Created .vscode/extensions.json${NC}"
fi

# Create .npmrc
if [ ! -f ".npmrc" ] && confirm "Create .npmrc?"; then
    cat << EOF > .npmrc
save-exact=false
strict-peer-dependencies=false
auto-install-peers=true
shamefully-hoist=true
link-workspace-packages=true
resolution-mode=highest
EOF
    echo -e "${GREEN}Created .npmrc${NC}"
fi

echo -e "${GREEN}Project environment setup complete!${NC}"
echo -e "${BLUE}Next steps:${NC}"
echo "1. Review and customize the created configuration files"
echo "2. Run 'pnpm install' to install dependencies"
echo "3. Run 'pnpm test' to verify that everything is working"
echo "4. Review the documentation in the project/docs directory"