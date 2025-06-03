# Development Workflow

This document outlines the development workflow for the FinSight platform.

## Development Environment Setup

### Prerequisites

- Node.js 16+
- Python 3.9+
- Docker
- PNPM
- Git

### Initial Setup

```bash
# Clone the monorepo
git clone https://github.com/plturrell/finsight-monorepo.git
cd finsight-monorepo

# Install dependencies
pnpm install

# Set up Python environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Development Workflow

### 1. Feature Planning

1. **Issue Creation**: Create an issue in GitHub with a detailed description
2. **Refinement**: Discuss and refine the requirements
3. **Acceptance Criteria**: Define clear acceptance criteria
4. **Task Breakdown**: Break down the feature into manageable tasks

### 2. Development

1. **Create Branch**: Create a feature branch from `develop`
   ```bash
   git checkout develop
   git pull
   git checkout -b feature/my-feature
   ```

2. **Implement**: Write code, tests, and documentation
   ```bash
   # Make changes to the codebase
   # Run tests locally
   pnpm test
   # Run linting
   pnpm lint
   ```

3. **Commit Changes**: Use conventional commit messages
   ```bash
   git add .
   git commit -m "feat(component): add new feature"
   ```

4. **Push Changes**: Push to the remote repository
   ```bash
   git push -u origin feature/my-feature
   ```

### 3. Code Review

1. **Create Pull Request**: Create a PR against the `develop` branch
2. **CI Checks**: Ensure all CI checks pass
3. **Code Review**: Request reviews from teammates
4. **Address Feedback**: Make changes based on feedback
5. **Approval**: Obtain approvals from reviewers

### 4. Integration

1. **Merge**: Once approved, merge the PR into `develop`
2. **Sync Changes**: Sync changes to individual repositories
   ```bash
   pnpm sync:github
   ```

3. **Verify**: Ensure changes are properly synchronized

### 5. Testing

1. **Integration Testing**: Test the feature in the integrated environment
2. **Regression Testing**: Ensure existing functionality works
3. **Performance Testing**: Check performance impact
4. **Security Testing**: Verify security implications

### 6. Release

1. **Create Release Branch**: When ready for release
   ```bash
   git checkout develop
   git checkout -b release/v1.0.0
   ```

2. **Version Bump**: Update version numbers
3. **Final Testing**: Conduct final tests
4. **Release Notes**: Prepare release notes
5. **Merge to Main**: Merge the release branch into `main`
   ```bash
   git checkout main
   git merge --no-ff release/v1.0.0
   git tag -a v1.0.0 -m "Version 1.0.0"
   git push origin main --tags
   ```

6. **Deploy**: Deploy to production

## Continuous Integration

All pull requests and pushes to main branches trigger CI workflows:

1. **Lint**: Code style and quality checks
2. **Build**: Build all applications and packages
3. **Test**: Run unit and integration tests
4. **Coverage**: Generate code coverage reports
5. **Security**: Run security scans

## Working with the Monorepo

### Adding a New Package

1. Create the package directory in `packages/`
   ```bash
   mkdir -p packages/my-package
   ```

2. Initialize the package
   ```bash
   cd packages/my-package
   pnpm init
   ```

3. Update `pnpm-workspace.yaml` if needed

### Adding a New Application

1. Create the application directory in `apps/`
   ```bash
   mkdir -p apps/my-app
   ```

2. Initialize the application
   ```bash
   cd apps/my-app
   pnpm init
   ```

3. Update `pnpm-workspace.yaml` if needed

### Running a Specific Package

```bash
# Run a script in a specific package
pnpm --filter @finsight/my-package run dev

# Run a script in a specific app
pnpm --filter @finsight/my-app run dev
```

## Troubleshooting

### Common Issues

1. **Dependency Issues**
   ```bash
   # Clean and reinstall dependencies
   pnpm clean
   pnpm install
   ```

2. **Sync Issues**
   ```bash
   # Manually check for sync issues
   ./tools/sync/sync-to-github.sh --verbose
   ```

3. **Build Issues**
   ```bash
   # Clean build artifacts
   pnpm run clean
   # Rebuild
   pnpm run build
   ```

## Project-Specific Workflows

### AI Engine Development

1. Train models locally or on development infrastructure
2. Test inference with sample data
3. Deploy to NVIDIA infrastructure for production

### Web Dashboard Development

1. Develop components with Storybook
2. Implement pages and features
3. Test responsiveness and cross-browser compatibility

### Data Platform Development

1. Develop ETL processes
2. Test with sample datasets
3. Verify data integrity and performance