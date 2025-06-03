# Dependency Management

This document outlines the dependency management strategy for the FinSight monorepo.

## Tools

- **PNPM Workspaces**: For JavaScript/TypeScript package management
- **UV**: For Python package management
- **Renovate**: For automated dependency updates
- **Dependabot**: For security updates
- **Pre-commit hooks**: For dependency validation

## JavaScript/TypeScript Dependencies

### Adding Dependencies

```bash
# Add to a specific package
cd apps/web-dashboard
pnpm add react

# Add as dev dependency
pnpm add -D typescript

# Add to all packages
pnpm add react --filter=*

# Add shared dependency to root
cd ../..
pnpm add -w turbo
```

### Updating Dependencies

```bash
# Check for outdated packages
pnpm deps:check

# Update dependencies interactively
pnpm deps:update:interactive

# Update patch versions
pnpm deps:update

# Update minor versions
pnpm deps:update:minor

# Update major versions
pnpm deps:update:major
```

## Python Dependencies

### Adding Dependencies

```bash
# Add to a specific package
cd apps/ai-engine
uv pip install numpy

# Add with version specification
uv pip install "numpy>=1.23.0,<2.0.0"

# Add as dev dependency (update pyproject.toml accordingly)
uv pip install pytest --dev
```

### Updating Dependencies

```bash
# Check for outdated packages
pnpm py:deps:check

# Update all dependencies
pnpm py:deps:update

# Update a specific package
tools/scripts/dependencies/manage-python-deps.sh update numpy

# Sync dependencies to requirements.txt
pnpm py:deps:sync
```

## Automated Updates

### Renovate

The repository uses Renovate for automated dependency updates. The configuration is in `renovate.json`.

Renovate will:
- Automatically update minor and patch versions
- Create pull requests for major version updates
- Group related dependency updates
- Run on a weekly schedule

### Dependabot

GitHub's Dependabot is used for security updates. The configuration is in `.github/dependabot.yml`.

## Best Practices

1. **Version Consistency**: Keep versions consistent across packages
2. **Dependency Hoisting**: Use PNPM's hoisting to reduce duplication
3. **Peer Dependencies**: Properly declare peer dependencies
4. **Version Ranges**: Use caret ranges (`^`) for flexibility
5. **Lock Files**: Commit lock files for reproducibility

## Troubleshooting

### Common Issues

1. **Hoisting Issues**: If dependencies aren't properly hoisted, check the `.npmrc` file
2. **Version Conflicts**: Run `pnpm deps:check` to find conflicts
3. **Missing Dependencies**: Ensure all dependencies are declared in each package's package.json

### Resolving Conflicts

If you encounter dependency conflicts:

1. Identify conflicting packages with `pnpm deps:check`
2. Update all instances to the same version with `pnpm up <package>@<version> -r`
3. Test thoroughly after resolution

## Large Dependency Management

For large dependencies:

1. Consider using Git LFS for large binary dependencies
2. Use the cleanup tools to identify and manage large dependencies:
   ```bash
   ./tools/cleanup/clean-large-files.sh
   ```
3. Deduplicate large binary dependencies:
   ```bash
   ./tools/cleanup/consolidate-binaries.sh
   ```

## Python Environment Management

For Python projects:

1. Use UV for consistent dependency resolution
2. Keep a centralized `requirements.txt` for core dependencies
3. Use `pyproject.toml` for package-specific dependencies
4. Maintain separate development and production dependencies
EOF < /dev/null