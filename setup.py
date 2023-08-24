"""
django-cte-stubs.

================.

Type stubs for django-cte, enabling static type checking for the Django package
that provides support for Common Table Expressions (CTE).
"""
from pathlib import Path

from setuptools import find_packages, setup  # type: ignore[import]


def _find_stub_files() -> list[str]:
    stubs_path = Path("django_cte-stubs")
    return [f.relative_to(stubs_path).as_posix() for f in stubs_path.rglob("*.pyi")]


dependencies = [
    "mypy==1.*",
    "django-stubs==4.*",
    "django-cte==1.3.*",
]

setup(
    name="django-cte-stubs",
    version="0.1.0",
    description="Mypy stubs for Django CTE",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    license="BSD-3-Clause",
    license_files=["LICENSE.md"],
    url="https://github.com/moranabadie/django-cte-stubs",
    author="Moran Abadie",
    author_email="moran.abadie@gmail.com",
    maintainer="Moran Abadie",
    maintainer_email="moran.abadie@gmail.com",
    py_modules=[],
    python_requires=">=3.9",
    install_requires=dependencies,
    packages=["django_cte-stubs", *find_packages(exclude=["tests"])],
    package_data={
        "django_cte-stubs": _find_stub_files(),
    },
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
    ],
    project_urls={
        "Release notes": "https://github.com/moranabadie/django-cte-stubs/releases",
    },
)
