#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <IssueScope-release.tar.gz>" >&2
  exit 2
fi

archive="$1"
if [[ ! -f "$archive" ]]; then
  echo "Release archive not found: $archive" >&2
  exit 2
fi

if ! build_info="$(tar -xOzf "$archive" ./BUILD_INFO.json 2>/dev/null)"; then
  echo "BUILD_INFO.json is missing from the release archive" >&2
  exit 1
fi

printf '%s\n' "$build_info" | python3 -c '
import json
import sys

data = json.load(sys.stdin)
for key in ("version", "build", "commit"):
    value = data.get(key)
    if not value:
        raise SystemExit(f"missing {key} in BUILD_INFO.json")
    print(f"{key}={value}")
'
