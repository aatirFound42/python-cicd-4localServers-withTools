## Development Setup

### Install Pre-Commit Hooks

Before making any commits, install the pre-commit hooks:
```bash
pip install pre-commit
pre-commit install
```

This will automatically run Black, isort, Flake8, Pylint, and Mypy before each commit.

### Manual Formatting

To manually format your code:
```bash
black app/ tests/ --line-length=100
isort app/ tests/ --profile black
```

To run all checks manually:
```bash
pre-commit run --all-files
```