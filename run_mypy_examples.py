"""Run mypy on example files and compare the output with expected results."""

import difflib
import os
import subprocess
import sys
from pathlib import Path

EXAMPLES: list[str] = [
    "tests/project/examples/join.py",
    "tests/project/examples/custom_query_set.py",
    "tests/project/examples/raw.py",
    "tests/project/examples/recursive_example.py",
    "tests/project/examples/simple.py",
    "tests/project/examples/named_common_table.py",
]


def run_install() -> None:
    """Install the package using uv pip to ensure mypy can find the stubs."""
    print("Installing package with uv pip...")
    subprocess.run(["uv", "pip", "install", "."], capture_output=True, text=True, check=True)  # noqa: S607,S603


def compare_output(example_file: str, output: str) -> bool:
    """Compare the output of mypy on the example file with the expected output."""
    example_path = Path(example_file)
    txt_file = example_path.with_suffix(".txt")
    if not txt_file.exists():
        msg = f"No expected output file found for {example_file} (looked for {txt_file})"
        raise ValueError(msg)
    with txt_file.open() as f:
        expected = f.read()

    # Remove "Success: no issues found in 1 source file" from both outputs before comparing
    def strip_success(text: str) -> str:
        return "\n".join(line for line in text.strip().splitlines() if not line.startswith("Success: no issues found in"))

    output_clean = strip_success(output)
    expected_clean = strip_success(expected)
    if output_clean.strip() != expected_clean.strip():
        print(f"Output for {example_file} does not match {txt_file}:")
        diff = difflib.unified_diff(
            expected_clean.splitlines(),
            output_clean.splitlines(),
            fromfile=str(txt_file),
            tofile=example_file + " (actual)",
            lineterm="",
        )
        print("\n".join(diff))
        raise AssertionError("\n".join(diff))
    return True


def run_mypy(example_file: str) -> bool:
    """Run mypy on the given example file and compare the output with the expected output."""
    print(f"Running mypy on {example_file}...")
    env = os.environ.copy()
    env["PYTHONPATH"] = "tests/project"
    result = subprocess.run(  # noqa: S603
        ["mypy", example_file],  # noqa: S607
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        return False
    return compare_output(example_file, result.stdout)


def run_based_pytest() -> bool:
    """Run basedpyright on the django_cte-stubs/ directory."""
    print("Running basedpyright on django_cte-stubs/ ...")
    result = subprocess.run(  # noqa: S603
        ["basedpyright", "django_cte-stubs/"],  # noqa: S607
        capture_output=True,
        text=True,
        check=False,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        return False
    return True


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run mypy on example files and compare output.")
    parser.add_argument("--file", type=str, help="Run mypy only on the given example file (path relative to project root).")
    args = parser.parse_args()

    if not run_based_pytest():
        sys.exit(1)
    run_install()
    all_ok = True

    files_to_test = [args.file] if args.file else EXAMPLES

    for example in files_to_test:
        ok = run_mypy(example)
        if not ok:
            all_ok = False
    if not all_ok:
        sys.exit(1)
    print("All mypy checks passed.")
