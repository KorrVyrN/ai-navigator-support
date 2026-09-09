# Contributing to AI Navigator Support

Thank you for your interest in contributing to the AI Navigator Support project! We welcome contributions from the community and appreciate your effort to improve this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

## Code of Conduct

This project adheres to the Contributor Covenant Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment tool (venv or virtualenv)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-navigator-support.git
   cd ai-navigator-support
   ```
3. Add upstream remote:
   ```bash
   git remote add upstream https://github.com/KorrVyrN/ai-navigator-support.git
   ```

## Development Setup

### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Environment Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Update `.env` with your configuration (API keys, database URLs, etc.)

## Making Changes

### Create a Feature Branch

1. Update your local main branch:
   ```bash
   git checkout main
   git pull upstream main
   ```

2. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

   Use the following naming convention:
   - `feature/` for new features
   - `bugfix/` for bug fixes
   - `docs/` for documentation updates
   - `refactor/` for code refactoring
   - `test/` for adding tests

### Make Your Changes

- Write clean, readable code
- Follow the project's coding style (see [Code Standards](#code-standards))
- Add or update tests as needed
- Update documentation if your changes affect user-facing functionality

## Commit Guidelines

We follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that don't affect code meaning (formatting, missing semicolons, etc.)
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `perf`: Code change that improves performance
- `test`: Adding or updating tests
- `chore`: Changes to build process, dependencies, or tooling

### Examples

```
feat(auth): add JWT token validation

Implement JWT token validation for API endpoints.
This ensures that only authenticated users can access protected resources.

Closes #123
```

```
fix(api): handle null responses from external service

The API was throwing errors when the external service returned null.
Added proper null checking and error handling.

Fixes #456
```

## Pull Request Process

1. **Ensure your branch is up-to-date:**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push your changes:**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request:**
   - Go to the GitHub repository
   - Click "New Pull Request"
   - Select your branch and fill in the PR template
   - Link related issues using "Closes #123" syntax

4. **PR Requirements:**
   - Must have a clear title and description
   - Must pass all CI/CD checks
   - Must have at least one approval from maintainers
   - Must have tests for new functionality
   - Must update documentation if needed

5. **Review Process:**
   - Address review comments promptly
   - Re-request review after making changes
   - Be open to feedback and suggestions

## Code Standards

### Python Code Style

We follow PEP 8 and use the following tools:

- **Black** for code formatting
- **Flake8** for linting
- **isort** for import sorting

### Format Your Code

```bash
# Format with Black
black src/ tests/

# Sort imports
isort src/ tests/

# Check linting
flake8 src/ tests/
```

### Naming Conventions

- Classes: `PascalCase` (e.g., `UserService`)
- Functions/methods: `snake_case` (e.g., `get_user_by_id`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES`)
- Private members: prefix with underscore (e.g., `_internal_method`)

### Documentation

- Write docstrings for all public functions and classes
- Use Google-style docstrings:
  ```python
  def calculate_sum(a: int, b: int) -> int:
      """Calculate the sum of two numbers.
      
      Args:
          a: The first number
          b: The second number
          
      Returns:
          The sum of a and b
          
      Raises:
          TypeError: If inputs are not integers
      """
      return a + b
  ```

## Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_example.py

# Run tests matching pattern
pytest -k "test_pattern"
```

### Writing Tests

- Write tests for new features
- Maintain test coverage above 80%
- Use descriptive test names: `test_<function>_<scenario>_<expected_result>`
- Follow the Arrange-Act-Assert pattern:
  ```python
  def test_user_creation_with_valid_data():
      # Arrange
      user_data = {"name": "John", "email": "john@example.com"}
      
      # Act
      user = create_user(user_data)
      
      # Assert
      assert user.name == "John"
      assert user.email == "john@example.com"
  ```

## Reporting Bugs

When reporting bugs, please include:

1. **Description**: Clear description of the bug
2. **Steps to Reproduce**: Step-by-step instructions
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**: Python version, OS, dependencies
6. **Screenshots/Logs**: If applicable, include error messages or screenshots

Use the bug report issue template when creating a new issue.

## Suggesting Enhancements

When suggesting enhancements:

1. **Description**: Clear description of the enhancement
2. **Motivation**: Why this enhancement would be useful
3. **Implementation Details**: Your ideas for implementation (optional)
4. **Examples**: Use cases and examples (if applicable)

Use the feature request issue template when creating a new issue.

## Additional Notes

- Check existing issues and PRs before starting work
- Keep PRs focused on a single feature or fix
- Don't commit sensitive information (API keys, passwords, etc.)
- Follow the project's license requirements

## Questions?

If you have any questions, feel free to:
- Open an issue for discussion
- Check existing documentation
- Contact the maintainers

Thank you for contributing! 🎉
