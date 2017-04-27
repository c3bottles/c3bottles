#!/bin/bash

PYTHONPATH=".:${PYTHONPATH}" python -m pytest test -v -s
