#!/usr/bin/env bash

APP_DIR=/home/hgb/apitest
APITEST_PORT=8000

if [ -n "$1" ]; then
  APITEST_PORT=${1}
fi

uvicorn main:app --app-dir "${APP_DIR}" --host 0.0.0.0 --port "${APITEST_PORT}"
