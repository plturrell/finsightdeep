# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |

## Reporting a Vulnerability

The AIQToolkit NVIDIA team takes security seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Where to Report

**Please DO NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to: **security@aiqtoolkit.ai**

### What to Include

Please include the following information in your report:

- **Description** of the vulnerability
- **Steps to reproduce** the issue
- **Potential impact** of the vulnerability
- **Suggested fix** (if you have one)
- **Your contact information** for follow-up

### Response Timeline

- **Initial Response**: Within 24 hours
- **Status Update**: Within 72 hours
- **Fix Timeline**: Varies based on severity, typically 7-30 days

### Security Best Practices

When using AIQToolkit NVIDIA:

1. **Environment Variables**: Never commit sensitive data like API keys to the repository
2. **HTTPS Only**: Always use HTTPS in production environments
3. **Input Validation**: Validate all user inputs before processing
4. **Regular Updates**: Keep dependencies up to date
5. **Access Control**: Implement proper authentication and authorization

### Disclosure Policy

- We follow responsible disclosure practices
- Security researchers will be credited for their findings (if desired)
- We will provide updates on the status of your report
- Once a fix is released, we may publicly acknowledge the issue

### Security Headers

This application implements the following security measures:

- **CORS**: Configured for secure cross-origin requests
- **Content Security Policy**: Prevents XSS attacks
- **Input Sanitization**: All user inputs are validated
- **Environment Isolation**: Sensitive configuration is environment-based

Thank you for helping keep AIQToolkit NVIDIA and our users safe!