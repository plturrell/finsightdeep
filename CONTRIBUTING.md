# Contributing to AIQToolkit NVIDIA

Thank you for your interest in contributing to AIQToolkit NVIDIA! We welcome contributions from everyone.

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- Python 3.8+
- Git
- GitHub account

### Development Setup

1. **Fork and clone the repository**
   ```bash
   gh repo fork plturrell/aiqtoolkit-nvidia --clone
   cd aiqtoolkit-nvidia
   ```

2. **Install dependencies**
   ```bash
   npm install
   pip install -r requirements.txt
   ```

3. **Set up environment**
   ```bash
   cp .env.example .env.local
   # Add your NVIDIA_ENDPOINT
   ```

4. **Start development server**
   ```bash
   vercel dev
   # or
   python -m http.server 3000
   ```

## 📝 How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/plturrell/aiqtoolkit-nvidia/issues)
2. If not, create a new issue with:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details

### Suggesting Features

1. Check [Discussions](https://github.com/plturrell/aiqtoolkit-nvidia/discussions) for existing suggestions
2. Create a new discussion or issue with:
   - Clear description of the feature
   - Use case and benefits
   - Possible implementation approach

### Code Contributions

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow our coding standards
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
   ```bash
   npm run test
   npm run lint
   ```

4. **Commit your changes**
   ```bash
   git commit -m "feat: add amazing new feature"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📋 Coding Standards

### JavaScript/HTML/CSS
- Use modern ES6+ JavaScript
- Follow semantic HTML structure
- Use CSS Grid/Flexbox for layouts
- Maintain accessibility standards (WCAG 2.1)

### Python
- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions and classes
- Handle errors gracefully

### Commit Messages
Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation changes
- `style:` formatting changes
- `refactor:` code refactoring
- `test:` adding tests
- `chore:` maintenance tasks

## 🔍 Code Review Process

1. All contributions require review
2. Maintainers will review PRs within 48 hours
3. Address feedback promptly
4. Ensure CI checks pass
5. Squash commits before merge

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🤝 Code of Conduct

Please note that this project is released with a [Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## 🆘 Need Help?

- Join our [Discussions](https://github.com/plturrell/aiqtoolkit-nvidia/discussions)
- Check the [Documentation](https://docs.aiqtoolkit.ai)
- Reach out to maintainers