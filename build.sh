#!/usr/bin/env bash

set -e

case $1 in
    "setup")
        rm -rf venv
        python3 -m venv venv | python -m venv venv
        source venv/bin/activate | source venv/Scripts/activate
        pip install --upgrade pip
        pip install .[TEST]
        python setup.py develop
        ;;
    "test")
        pytest
        coverage-badge -f -o coverage.svg
        ;;
    *) echo "Unknown option $1";;
esac
