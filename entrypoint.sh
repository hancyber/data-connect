#!/usr/bin/env bash

if [ -n "$1" ]; then
  CONF_FILE=${1}
fi

python /home/hgb/main.py "${CONF_FILE}"