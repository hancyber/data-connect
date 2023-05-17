#!/usr/bin/env bash

if [ -z "$EMBULK_MEM" ]; then
    EMBULK_MEM="128m"
fi

embulk -J-Xmx${EMBULK_MEM} -J-Xms${EMBULK_MEM} run --log $2 $1
