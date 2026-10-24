#!/usr/bin/env bash
# Bound heavy analysis/build jobs and keep the shared host responsive.
set -euo pipefail
cpu="$(python3 -c 'import os; print(min(os.sched_getaffinity(0)))')"
exec systemd-run --user --scope --quiet \
  -p CPUQuota=35% -p MemoryMax=768M -p MemorySwapMax=0 -p TasksMax=64 \
  taskset -c "$cpu" nice -n 19 "$@"
