#!/bin/bash
set -e
cmd="$@"


>&2 echo "Database is up - continuing..."
exec $cmd
