#!/bin/bash
# cognition-os drift detection: check if projects have code updates
# newer than their latest OS session. Output projects that need sync.
# Exit 0 with output = needs attention; exit 1 silently = all OK.
set -uo pipefail

DRIFT_THRESHOLD_DAYS=1
NEED_SYNC=()

for rco in /home/huangrui/program/*/research-cognition-os /home/huangrui/Data/*/research-cognition-os; do
  [ -d "$rco" ] || continue
  proj=$(dirname "$rco")
  proj_name=$(basename "$proj")

  # Skip if no sessions directory
  if [ ! -d "$rco/sessions" ]; then
    NEED_SYNC+=("$proj_name:NO_SESSIONS_DIR")
    continue
  fi

  # Get latest session date (from filename: YYYY-MM-DD.md)
  latest_session=$(ls -1 "$rco/sessions/"*.md 2>/dev/null | sort | tail -1)
  if [ -z "$latest_session" ]; then
    NEED_SYNC+=("$proj_name:NO_SESSION_FILES")
    continue
  fi
  session_date=$(basename "$latest_session" .md)
  session_epoch=$(date -d "$session_date" +%s 2>/dev/null || echo 0)

  # Get latest code modification time (Python files, notebooks, scripts)
  latest_code=$(find "$proj" -maxdepth 4 -type f \( -name '*.py' -o -name '*.ipynb' -o -name '*.sh' \) \
    -not -path '*/research-cognition-os/*' \
    -not -path '*/.git/*' \
    -not -path '*/__pycache__/*' \
    -not -path '*/venv/*' \
    -not -path '*/.venv/*' \
    -not -path '*/.hermes/*' \
    -printf '%T@\t%p\n' 2>/dev/null | sort -rn | head -1)
  
  if [ -z "$latest_code" ]; then
    continue
  fi
  
  code_epoch=$(echo "$latest_code" | cut -f1 | cut -d. -f1)
  code_file=$(echo "$latest_code" | cut -f2-)
  
  # Calculate drift in days
  drift_days=$(( (code_epoch - session_epoch) / 86400 ))
  
  if [ "$drift_days" -gt "$DRIFT_THRESHOLD_DAYS" ]; then
    NEED_SYNC+=("$proj_name:${drift_days}d_drift|latest=$(basename "$code_file")|session=$session_date")
  fi
done

if [ ${#NEED_SYNC[@]} -gt 0 ]; then
  echo "⚠️ OS Drift: ${#NEED_SYNC[@]} project(s) need sync:"
  for item in "${NEED_SYNC[@]}"; do
    echo "  - $item"
  done
  exit 0
else
  exit 1
fi
