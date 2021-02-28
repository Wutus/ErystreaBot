#!/bin/bash

set -x
set +e
timeout $1 $2
EXIT_CODE=$?
set -e

if [[ $EXIT_CODE != 124 ]]; then
    if [[ $EXIT_CODE == 0 ]]; then
        exit 124
    else
        exit $EXIT_CODE
    fi
fi