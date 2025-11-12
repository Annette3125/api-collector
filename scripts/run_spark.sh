#!/usr/bin/env bash
set -euo pipefail
export JAVA_HOME="$(/usr/libexec/java_home -v 17)"
export SPARK_LOCAL_IP=127.0.0.1

# activate venv, if want automate way:
# source .venv/bin/activate

python -m api_collector.databricks_etl

