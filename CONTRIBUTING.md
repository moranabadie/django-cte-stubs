# Contributing to django-cte-stubs

First and foremost, thank you for considering contributing to `django-cte-stubs`.

## Getting Started

#### 1. Setting Up Your Environment

To start developing for `django-cte-stubs`, you'll need to set up a local development environment:

1. Fork the repository on GitHub.
2. Clone your fork locally
3. make sure you have a virtualenv with python >= 3.9 
4. Install required dependencies (preferably in a virtual environment): `uv sync --all-groups`

#### 2. Test your environment

- run the linter : ` ruff format ; ruff check --fix`
- run mypy : `PYTHONPATH=tests/project mypy .`

## Contribution Guidelines

### Reporting Bugs

- Check if the bug has already been reported in the Issues tab.
- If not, create a new issue with a clear title and description.
- Provide as much context as possible, including steps to reproduce, expected behavior, and actual behavior.

### Code Style

We aim to maintain a consistent coding style throughout the project. Here are a few key points:

- Make sure dependencies in [requirements.in](tests%2Frequirements.in) are installed
- Call `ruff format ; ruff check` or `ruff format ; ruff check --fix`

### Testing

Before submitting a pull request, ensure that all tests pass:

- Make sure dependencies in [requirements.in](tests%2Frequirements.in) are installed
- Call ` PYTHONPATH=tests/project mypy .`
- Create your own test (for the feature or the bug) in [project](tests%2Fproject)

### Making Changes

1. Create a new branch with a meaningful name: `git checkout -b branch-name`.
2. Make and commit your changes with clear, concise commit messages.
3. Keep your changes focused. If you're fixing a bug, make sure your changes only fix that bug and don't introduce new features. Likewise, if you're adding a feature, focus on that feature.

### Submitting a Pull Request

1. Push your branch to your fork on GitHub.
2. Create a pull request from your fork to the main `django-cte-stubs` repository.
3. In the pull request description, explain your changes and any decisions you made.
4. Make sure your PR passes any continuous integration checks set up on the repository.
