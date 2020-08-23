#!/usr/bin/env bash
case $1 in
    "pylint")
        pylint `ls -R setup.py tests tv_temp_report|grep .py$|xargs`
        ;;
    *) echo "Unknown option $1";;
esac