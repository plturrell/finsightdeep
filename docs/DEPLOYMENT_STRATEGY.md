# FinSight Deployment Strategy

This document outlines the deployment strategy for the FinSight platform, with special focus on preserving compatibility with NVIDIA launchable configurations while leveraging the benefits of a monorepo structure.

## Overview

The FinSight platform uses a hybrid approach that combines:

1. **Monorepo Development**: A unified codebase for development efficiency
2. **Separate GitHub Repositories**: Individual repositories for specific deployments
3. **NVIDIA Launchable Preservation**: Dedicated storage for NVIDIA deployment configurations

## Monorepo Structure

The monorepo is structured as follows:

```
finsight-monorepo/
├── apps/                     # Application packages (symbolic links)
│   ├── ai-engine/            # AI/ML capabilities (link to finsightdeep)
│   ├── data-platform/        # Data processing (link to finsightdata)
│   ├── web-dashboard/        # Web UI (link to finsightexperience)
│   └── utils/                # Utilities (link to finsightutils)
├── packages/                 # Shared packages
│   ├── api-client/           # API client library
│   ├── config/               # Shared configuration
│   ├── ui-components/        # Shared UI components
│   ├── utils/                # Shared utilities
│   └── testing/              # Testing utilities
├── launchables/              # NVIDIA launchable configurations
│   ├── finsightdeep-launchable.yaml
│   ├── finsightdata-launchable.yaml
│   ├── finsightexperience-launchable.yaml
│   └── finsightutils-launchable.yaml
└── tools/                    # Development tooling
    ├── sync/                 # Scripts for syncing with GitHub repositories in @plturrell's Finsight V3 Project
    ├── cleanup/              # Project cleanup and optimization tools
    └── scripts/              # General development scripts
```

## Symbolic Link Strategy

The monorepo uses symbolic links to maintain the existing repository structure:

1. The `apps/` directory contains symbolic links to the actual repositories
2. Changes made in the monorepo are reflected in the original repositories
3. The original repository structure is preserved for compatibility with existing build and deployment pipelines

## NVIDIA Launchable Configurations

NVIDIA launchable configurations are preserved as follows:

1. Original configuration files are stored in the `launchables/` directory
2. During synchronization, these configurations are copied back to their original locations
3. This ensures that the NVIDIA deployment process can continue to work without modification

## Deployment Process

### 1. Development in Monorepo

Developers work in the monorepo for:
- Feature development
- Bug fixes
- Testing
- Shared code management

### 2. Synchronization to GitHub Repositories

When changes are ready for deployment:

```bash
# Sync changes to individual repositories
pnpm sync:github
```

This process:
- Copies changes to the individual repositories
- Preserves NVIDIA launchable configurations
- Updates GitHub workflow files

### 3. Deployment to NVIDIA Platform

Deployment to the NVIDIA platform:
- Uses the original repository structure
- Leverages preserved launchable configurations
- Maintains compatibility with existing deployment pipelines

## CI/CD Integration

The CI/CD process is adapted to work with this hybrid approach:

1. **Monorepo CI**:
   - Runs checks on the entire codebase
   - Ensures cross-package compatibility
   - Performs comprehensive testing

2. **Individual Repository CI**:
   - Triggered after synchronization
   - Focuses on deployment-specific checks
   - Prepares for NVIDIA deployment

## Special Considerations

### Large File Handling

Large files are managed through:
- Git LFS for large binary files
- Deduplication using shared storage and symbolic links
- Cleanup scripts to remove unnecessary large files

### Dependency Management

Dependencies are managed centrally:
- PNPM workspaces for JavaScript/TypeScript
- Shared Python dependencies through requirements.txt
- Automated dependency updates via Renovate

### Documentation

Documentation is:
- Consolidated into the `docs/` directory
- Linked from individual repositories when needed
- Focused on specific deployment configurations where appropriate

## Troubleshooting

### Sync Issues

If synchronization fails:
1. Check for uncommitted changes in the target repositories
2. Verify that symbolic links are intact
3. Run `./tools/sync/sync-to-github.sh --verbose` for detailed logging

### NVIDIA Deployment Issues

If NVIDIA deployment fails:
1. Verify that launchable configurations are properly preserved
2. Check that all dependencies are properly synced
3. Ensure that binary files and large assets are properly handled

## Future Improvements

1. Automate synchronization as part of CI/CD
2. Implement versioned releases across all repositories
3. Improve dependency sharing between Python and JavaScript/TypeScript code
4. Enhance documentation with cross-repository references
EOF < /dev/null