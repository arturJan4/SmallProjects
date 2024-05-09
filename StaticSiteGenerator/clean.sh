#!/bin/bash
find ./ -name '*.pyc' -exec rm -f {} \;
find ./ -name '__pycache__' -exec rm -rf {} \;
rm -rf .cache
rm -rf .mypy_cache
rm -rf htmlcov
rm -rf .coverage