#!/bin/bash
# formatter part
isort src/
isort tests/
black -l 119 src/
black -l 119 tests/

# linter part
flake8 src/
black -l 119 --check src/
black -l 119 --check tests/
mypy --python-version=3.12 --ignore-missing-imports src/