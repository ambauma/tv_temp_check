#!/usr/bin/env bash
case $1 in
    "setup")
        rm -rf venv
        python3 -m venv venv
        source venv/bin/activate
        pip install --upgrade pip
        pip install .[TEST]
        python setup.py develop
        ;;
    "test")
        pytest
        ;;
    *) echo "Unknown option $1";;
esac