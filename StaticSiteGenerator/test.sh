#!/bin/bash
python -m coverage run -m unittest discover -s tests/
coverage html --omit="*/tests*"