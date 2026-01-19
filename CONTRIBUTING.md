# Contributing to AI Prompt Engineering

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Adding New Features](#adding-new-features)

---

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

---

## Getting Started

1. **Fork the repository**
2. **Clone your fork:**
   ```bash
   git clone https://github.com/your-username/AI-Prompt-Engineering.git
   cd AI-Prompt-Engineering
   ```

3. **Set up development environment:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

---

## How to Contribute

We welcome contributions in many forms:

### Bug Reports

When reporting bugs, please include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Error messages or screenshots

**Template:**
```markdown
## Bug Description
Brief description of the bug

## Steps to Reproduce
1. Step one
2. Step two
3. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Windows 10]
- Python: [e.g., 3.9]
- Version: [e.g., 1.0.0]

## Additional Context
Any other relevant information
```

### Feature Requests

When requesting features, please include:
- Clear description of the feature
- Use case and motivation
- Proposed implementation (if applicable)
- Examples of how it would be used

**Template:**
```markdown
## Feature Description
Brief description of the feature

## Use Case
Why is this feature needed?

## Proposed Implementation
How should this work?

## Examples
Provide examples of usage

## Additional Context
Any other relevant information
```

### Documentation Improvements

- Fix typos or clarify language
- Add missing documentation
- Improve examples
- Translate to other languages

### 🔧 Code Contributions

- Fix bugs
- Implement new features
- Improve performance
- Refactor code
- Add tests

---

## Development Setup

### Prerequisites

- Python 3.8+
- pip or conda
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/ElaMCB/AI-Prompt-Engineering.git
cd AI-Prompt-Engineering

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (if any)
pip install -r requirements-dev.txt
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_validator.py

# Run with coverage
pytest --cov=notebooks tests/
```

### Running the Dashboard

```bash
streamlit run streamlit_app.py
```

---

## Pull Request Process

1. **Update Documentation:**
   - Update README.md if needed
   - Add/update API documentation
   - Include code comments

2. **Test Your Changes:**
   - Ensure all tests pass
   - Test manually if needed
   - Check for linting errors

3. **Commit Messages:**
   - Use clear, descriptive messages
   - Reference issue numbers if applicable
   - Follow conventional commits format:
     ```
     feat: Add new prompt validator feature
     fix: Resolve issue with A/B testing
     docs: Update API reference
     ```

4. **Create Pull Request:**
   - Provide clear description
   - Reference related issues
   - Include screenshots if UI changes
   - Request review from maintainers

5. **Respond to Feedback:**
   - Address review comments
   - Make requested changes
   - Update PR as needed

---

## Coding Standards

### Python Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints where appropriate
- Write docstrings for all functions/classes
- Keep functions focused and small
- Use meaningful variable names

### Code Formatting

```bash
# Use black for formatting (if installed)
black notebooks/

# Use isort for import sorting (if installed)
isort notebooks/
```

### Example Code Style

```python
"""
Clear module/class description.
"""

from typing import Dict, List, Optional


class ExampleClass:
    """Class description."""
    
    def __init__(self, param: str):
        """
        Initialize class.
        
        Args:
            param: Description of parameter
        """
        self.param = param
    
    def example_method(self, input_data: str) -> Dict:
        """
        Method description.
        
        Args:
            input_data: Description of input
        
        Returns:
            Dictionary with results
        
        Raises:
            ValueError: If input is invalid
        """
        if not input_data:
            raise ValueError("Input cannot be empty")
        
        return {"result": "example"}
```

---

## Adding New Features

### 1. Plan Your Feature

- Discuss in issues first (if major change)
- Design the API/interface
- Consider backward compatibility
- Plan tests

### 2. Implement

- Write code following standards
- Add docstrings
- Include type hints
- Add error handling

### 3. Test

- Write unit tests
- Test edge cases
- Test error handling
- Manual testing

### 4. Document

- Update API reference
- Add usage examples
- Update README if needed
- Add to changelog

### 5. Submit

- Create PR with description
- Reference related issues
- Request review

---

## Project Structure

```
AI-Prompt-Engineering/
├── notebooks/           # Core tools and utilities
├── docs/               # Documentation
├── examples/           # Example code and tutorials
├── tools/              # Additional tools
├── streamlit_app.py    # Streamlit dashboard
├── requirements.txt    # Dependencies
└── README.md          # Main documentation
```

### Where to Add Code

- **Core tools**: `notebooks/`
- **Documentation**: `docs/`
- **Examples**: `examples/`
- **Tests**: `tests/` (create if needed)
- **Configuration**: Root directory

---

## Guidelines

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Be specific and clear
- Reference issues: "Fix #123"
- Separate subject from body with blank line

**Good:**
```
feat: Add production validator framework

Implements comprehensive production validation with consistency,
robustness, edge case, and performance testing.

Closes #45
```

**Bad:**
```
update code
```

### Pull Requests

- One logical change per PR
- Keep PRs small and focused
- Provide clear description
- Reference related issues
- Update documentation

---

## Questions?

- Open an issue for questions
- Check existing issues/PRs first
- Be patient and respectful

---

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

Thank you for contributing!
