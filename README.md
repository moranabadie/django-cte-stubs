# django-cte-stubs

Type stubs for the `django-cte` package,
enabling static type checking and improved IDE experiences for Django developers.

## Key Features

- Comprehensive type stubs for the `django-cte` package.
- Better type hinting and autocompletions in supported IDEs.
- Compatible with Python 3.9 and above.
- Compatible with django-stubs 4.*
- Compatible with django-cte 1.3.* for now.

## Installation

To get started with `django-cte-stubs`, simply install the package via pip:

```bash
pip install django-cte-stubs
```

Once installed, setup https://github.com/typeddjango/django-stubs if not already.


## Typing Examples

We have provided a few examples of how typing is implemented using these stubs. Explore the following modules in our test suite for more insights:

- [cte_example.py](./tests/project/tests/cte_example.py) simple CTE typing
- [as_manager.py](./tests/project/tests/as_manager.py) with as_manager()
- [named.py](./tests/project/tests/named.py)  with named CTE objects
- [raw.py](./tests/project/tests/raw.py) With raw sql code
- [recursinve_example.py](./tests/project/tests/recursive_example.py) With a recursive CTE.

## Feedback & Contributions

We encourage feedback, bug reports, and contributions:

1. **Issues**: If you find any issues or areas of improvement, please raise an issue in our GitHub repository.
2. **Contributions**: Check out our [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on how to provide contributions.
