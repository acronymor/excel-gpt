#!/usr/local/env bash

bin=$(dirname "${BASH_SOURCE-$0}")
bin=$(
  cd "$bin" >/dev/null || exit
  pwd
)
cd "$bin" || exit

declare -r cur_path=$(pwd)

function cmd() {
  local name="$1"
  local attr=""
  python -c "from excelgpt.api import cmd; cmd.run('${name}')"
}

function ui() {
  streamlit run excelgpt/api/ui.py --browser.gatherUsageStats=false --server.address=0.0.0.0 --server.port=8090
}

"$@"
