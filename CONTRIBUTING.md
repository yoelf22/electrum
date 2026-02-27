# Contributing to Electrum

Thank you for your interest in contributing to **Electrum** — an AI-assisted toolkit for defining hardware products that have software inside.

We welcome contributions of all kinds: new phase templates, example outputs, script improvements, documentation fixes, and ideas.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Submitting Pull Requests](#submitting-pull-requests)
- [Development Setup](#development-setup)
- [Style Guidelines](#style-guidelines)
- [Commit Message Convention](#commit-message-convention)

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code. Please report unacceptable behavior to **yoelf22**.

## Getting Started

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/electrum.git
   cd electrum
   ```
3. **Create a branch** for your contribution:
   ```bash
   git checkout -b feat/my-improvement
   ```

## How to Contribute

### Reporting Bugs

Before opening a bug report, please search existing [Issues](https://github.com/yoelf22/electrum/issues) to avoid duplicates.

When filing a bug, include:
- A clear, descriptive title
- Steps to reproduce the problem
- Expected vs. actual behavior
- Phase or template involved (if applicable)
- Environment details (OS, Node version, AI model used)

### Suggesting Enhancements

Feature requests are welcome! Open an issue with the `enhancement` label and describe:
- The problem you are trying to solve
- Your proposed solution
- Any alternative approaches you considered

### Submitting Pull Requests

1. Ensure your branch is up to date with `master`.
2. Follow the [Style Guidelines](#style-guidelines) below.
3. Add or update relevant documentation and examples.
4. Open a Pull Request using the provided template.
5. Link the PR to any related issue (e.g., `Closes #42`).

A maintainer will review your PR as soon as possible. Please be patient and responsive to review feedback.

## Development Setup

Electrum is primarily composed of Markdown templates and scripts. No special build step is required.

```bash
# Run a phase script (example)
node scripts/run_phase.js --phase 1 --product "Smart Dispenser"
```

For AI-assisted phases, ensure your Claude API key is set:
```bash
export ANTHROPIC_API_KEY=your_key_here
```

## Style Guidelines

- **Markdown**: Use ATX-style headings (`##`), wrap lines at ~100 characters.
- **Templates**: Follow the existing 8-phase structure in `templates/`.
- **Scripts**: Use Node.js (ESM or CommonJS consistent with the project). Add JSDoc comments for exported functions.
- **Examples**: Place new examples under `examples/` with a descriptive folder name.

## Commit Message Convention

Use the format: `type(scope): short description`

| Type | When to use |
|------|-------------|
| `feat` | New feature or template |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code restructure without behavior change |
| `chore` | Build process or tooling changes |

Examples:
```
feat(templates): add Phase 9 go-to-market template
fix(scripts): handle missing product name gracefully
docs(readme): update quick-start instructions
```

---

Thank you for helping make Electrum better for hardware product teams everywhere!
