# FinSight Project Cleanup Tools

This directory contains scripts for cleaning up and optimizing the FinSight monorepo structure.

## Available Tools

### 1. Master Cleanup Script

The main orchestration script that runs all cleanup operations in sequence.

```bash
./cleanup-project.sh [--no-dry-run] [--no-confirm] [--skip STEP1,STEP2,...] [--only STEP1,STEP2,...]
```

Options:
- `--no-dry-run`: Execute actual file operations (default: dry run only)
- `--no-confirm`: Skip confirmation prompts
- `--skip`: Comma-separated list of steps to skip (e.g., `large-files,documentation`)
- `--only`: Comma-separated list of steps to run (overrides `--skip`)

Available steps:
- `large-files`: Large files management
- `dev-artifacts`: Development artifacts cleanup
- `documentation`: Documentation cleanup
- `duplication`: Code duplication analysis

### 2. Large Files Cleanup

Identifies and manages large files in the repository.

```bash
./clean-large-files.sh [--no-dry-run] [--min-size-mb SIZE_IN_MB] [--git-lfs]
```

Options:
- `--no-dry-run`: Execute actual file operations
- `--min-size-mb`: Minimum file size in MB to consider (default: 50MB)
- `--git-lfs`: Use Git LFS for large files

### 3. Development Artifacts Cleanup

Removes development logs, caches, and temporary files.

```bash
./clean-dev-artifacts.sh [--no-dry-run] [--no-confirm]
```

Options:
- `--no-dry-run`: Execute actual file operations
- `--no-confirm`: Skip confirmation prompts

### 4. Documentation Cleanup

Consolidates and organizes documentation.

```bash
./clean-documentation.sh [--no-dry-run] [--no-confirm]
```

Options:
- `--no-dry-run`: Execute actual file operations
- `--no-confirm`: Skip confirmation prompts

### 5. Code Duplication Analysis

Analyzes code duplication across the repository.

```bash
./analyze-code-duplication.sh [--no-dry-run] [--min-lines N] [--language js,ts,py,...]
```

Options:
- `--no-dry-run`: Execute actual file operations
- `--min-lines`: Minimum number of duplicate lines to detect (default: 10)
- `--languages`: Comma-separated list of file extensions to analyze

## Workflow

Recommended workflow for project cleanup:

1. Run a dry run of all tools to assess the state of the repository
   ```bash
   ./cleanup-project.sh
   ```

2. Review the generated reports and summaries

3. Execute actual cleanup operations with specific focus areas
   ```bash
   ./cleanup-project.sh --no-dry-run --only large-files,dev-artifacts
   ```

4. After cleaning up, commit the changes
   ```bash
   git add .
   git commit -m "Project cleanup: Removed large files and development artifacts"
   ```

5. Continue with code duplication analysis and refactoring
   ```bash
   ./cleanup-project.sh --no-dry-run --only duplication
   ```

6. Extract common code to shared libraries based on the duplication report

## Best Practices

1. Always run in dry-run mode first
2. Review reports before executing changes
3. Commit changes after each major cleanup step
4. Update `.gitignore` and `.gitattributes` to prevent future accumulation of unnecessary files
5. Incorporate cleanup into your development workflow