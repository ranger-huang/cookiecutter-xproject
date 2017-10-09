#!/bin/bash
set -e
cmd="$@"


# clean up test reports
rm -f /app/.noseids /app/.coverage
rm -rf /app/test-reports
mkdir -p /app/test-reports /app/test-reports/allure-reports

>&2 echo "Database is up - continuing..."
exec $cmd
