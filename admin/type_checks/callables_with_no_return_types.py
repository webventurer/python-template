"""
A simple script to find all callables in a Python project that do have something
to return, however there is no return type annotation. We can then add return
type annotations to these callables manually. We specifically avoid adding "->
None:" to functions/methods which return nothing as it clutters up the page
while not adding anything helpful.

Note: Also do a manual search for "-> None:" so you can remove them for
readability.

It's easier than running mypy.ini and Pylance doesn't (yet) have a way to report
on missing return type annotations.
"""

import ast
import os
import re

import click


def load_file(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def callables_with_no_return_values(node: ast.FunctionDef) -> bool:
    """Check if a function/method has a return statement that is not None."""

    return any(
        isinstance(subnode, ast.Return) and subnode.value is not None
        for subnode in ast.walk(node)
    )


def no_return_type_annotation(node: ast.FunctionDef) -> bool:
    """Return True if function/method has no return type annotation"""

    return node.returns is None


def get_callables_without_return_type(tree: ast.AST) -> list[str]:
    return [
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)  # Both functions and class methods
        and no_return_type_annotation(node)
        and callables_with_no_return_values(node)
    ]


SKIP_PATTERNS = [
    "^test_.*",
    "^setUp$",
    "^tearDown$",
    "^root$",
]


def skip_callables_that_match_regex(callables: list[str]) -> list[str]:
    return [
        c for c in callables if not any(re.match(r, c) for r in SKIP_PATTERNS)
    ]


def find_missing_return_types(file: str):
    tree = ast.parse(load_file(file))
    callables = get_callables_without_return_type(tree)
    if filtered_callables := skip_callables_that_match_regex(callables):
        print(f"{file:<40} Missing return types: {filtered_callables}")


IGNORE_PATHS = ["venv", ".venv", "type_checks"]


def filter_dirs(dirs: list[str]) -> list[str]:
    return [d for d in dirs if d not in IGNORE_PATHS]


def process_files(directory: str):
    for root, dirs, files in os.walk(directory):
        dirs[:] = filter_dirs(dirs)
        for file in files:
            if file.endswith(".py"):
                find_missing_return_types(os.path.join(root, file))


@click.command()
@click.argument("path", required=True, default=".")
def main(path: str):
    process_files(path)


if __name__ == "__main__":
    main()
