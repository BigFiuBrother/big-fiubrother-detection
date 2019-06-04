#!/usr/bin/env bash

rm -rf build
rm -rf dist
rm -rf big_fiubrother_detection.egg-info
python3 setup.py bdist_wheel
