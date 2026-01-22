# Contributing to API Log Viewer

Thank you for your interest in contributing to API Log Viewer! This document provides guidelines and instructions for contributing.

## 🤝 How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Log samples** that demonstrate the issue
- **Python version** and OS information
- **Screenshots** if applicable

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title and description**
- **Use case** - why is this enhancement needed?
- **Proposed solution** - how would it work?
- **Alternative solutions** you've considered
- **Examples** of similar features in other tools

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following our coding standards
3. **Add tests** if applicable
4. **Update documentation** if needed
5. **Ensure code passes** style checks
6. **Submit the pull request**

## 🏗️ Development Setup

### Prerequisites

- Python 3.7 or higher
- pip
- git

### Setup Instructions

```bash
# Fork and clone the repository
git clone https://github.com/setyuth/api-log-viewer.git
cd api-log-viewer

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=api_log_viewer

# Run specific test file
pytest tests/test_log_parser.py
```

### Code Style

We use several tools to maintain code quality:

```bash
# Format code with Black
black api_log_viewer.py

# Check style with flake8
flake8 api_log_viewer.py

# Type checking with mypy
mypy api_log_viewer.py
```

## 📝 Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use meaningful variable and function names
- Maximum line length: 100 characters
- Use type hints where appropriate

### Documentation

- Add docstrings to all functions and classes
- Use Google-style docstrings format
- Update README.md for user-facing changes
- Comment complex logic

Example docstring:
```python
def parse_log_entry(line: str) -> LogEntry:
    """Parse a single log line into a LogEntry object.
    
    Args:
        line: Raw log line string to parse
        
    Returns:
        LogEntry object with parsed fields
        
    Raises:
        ValueError: If line format is invalid
    """
```

### Git Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- First line should be 50 characters or less
- Reference issues and pull requests after the first line

Example:
```
Add filtering by response time

- Implement response time range filter
- Add tests for time-based filtering
- Update documentation

Fixes #123
```

## 🏷️ Branch Naming

- `feature/` - New features
- `bugfix/` - Bug fixes
- `hotfix/` - Urgent fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring

Examples:
- `feature/add-regex-search`
- `bugfix/fix-json-parsing`
- `docs/update-readme`

## 🧪 Testing Guidelines

### Writing Tests

- Write tests for all new features
- Maintain or improve code coverage
- Test edge cases and error conditions
- Use descriptive test names

Example:
```python
def test_parse_json_log_with_all_fields():
    """Test parsing JSON log with all expected fields present."""
    line = '{"timestamp": "2024-01-20T10:30:45Z", "level": "INFO", "method": "GET"}'
    entry = LogEntry(line, 1)
    assert entry.level == "INFO"
    assert entry.method == "GET"
```

### Test Structure

```
tests/
├── __init__.py
├── test_log_parser.py      # Parser tests
├── test_filtering.py        # Filter tests
├── test_export.py           # Export functionality tests
└── fixtures/                # Sample log files
    ├── sample_json.log
    └── sample_text.log
```

## 📋 Feature Development Process

1. **Discuss** - Open an issue to discuss the feature
2. **Design** - Plan the implementation approach
3. **Implement** - Write the code following our standards
4. **Test** - Add comprehensive tests
5. **Document** - Update relevant documentation
6. **Review** - Submit PR for code review

## 🔍 Code Review Process

### For Reviewers

- Be respectful and constructive
- Review for logic, style, and maintainability
- Test the changes locally if possible
- Approve or request changes with clear feedback

### For Contributors

- Respond to all review comments
- Make requested changes in new commits
- Re-request review after making changes
- Be patient and professional

## 📚 Resources

- [Python Style Guide (PEP 8)](https://www.python.org/dev/peps/pep-0008/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [Git Best Practices](https://git-scm.com/book/en/v2)

## 🎯 Priority Areas for Contribution

We especially welcome contributions in these areas:

1. **Performance optimization** for large log files
2. **Additional log format parsers**
3. **Real-time log tailing** feature
4. **Web-based UI** alternative
5. **Plugin system** for custom parsers
6. **Comprehensive test coverage**
7. **Documentation improvements**

## 💬 Communication

- **GitHub Issues** - Bug reports and feature requests
- **GitHub Discussions** - General questions and ideas
- **Pull Request comments** - Implementation discussions

## 📄 License

By contributing to API Log Viewer, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be acknowledged in:
- README.md contributors section
- Release notes
- GitHub contributors page

Thank you for contributing to API Log Viewer! 🎉