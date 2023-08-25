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

Once installed, setup https://github.com/typeddjango/django-stubs if not already, and add `mypy_django_cte_plugin` :

```
plugins =
    mypy_django_plugin.main,
    mypy_django_cte_plugin.main,
```


## Typing Examples

We have provided a few examples of how typing is implemented using these stubs. Explore the following modules in our test suite for more insights:

- [simple.py](./tests/project/examples/simple.py) simple CTE typing
- [simple_typed.py](./tests/project/examples/simple_typed.py) simple CTE with strong typing
- [as_manager.py](./tests/project/examples/as_manager.py) with as_manager()
- [raw.py](./tests/project/examples/raw.py) With raw sql code
- [recursive_example.py](./tests/project/tests/recursive_example.py) With a recursive CTE.

## Feedback & Contributions

We encourage feedback, bug reports, and contributions:

1. **Issues**: If you find any issues or areas of improvement, please raise an issue in our GitHub repository.
2. **Contributions**: Check out our [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on how to provide contributions.
