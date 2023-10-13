#!/usr/bin/env bash

set -e

# Copyright 2023 Free World Certified -- all rights reserved.

if (("$#" != 1)); then
    echo "Usage: $1 <directory to purge>"
    exit 1
fi

dir="$1"

if [[ ! -d "${dir}" ]]; then
    echo "${dir} does not exist"
    exit 1
fi

echo "startup deleting files in ${dir}..."
find ${dir} -mindepth 1 -delete -print

# cleanup files on exit
term_handler() {
    echo "shutdown deleting files in ${dir}..."
    find ${dir} -mindepth 1 -delete -print

    exit 0
}

# setup trap
trap 'kill ${!}; term_handler' SIGTERM SIGINT

# wait forever
while true; do
    tail -f /dev/null &
    wait ${!}
done
