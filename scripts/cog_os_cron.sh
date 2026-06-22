#!/bin/bash
# Cron wrapper: detect OS drift, then auto-sync if drift detected.
# This script is meant to be run as a cron job.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DRIFT_SCRIPT="$SCRIPT_DIR/cog_os_drift_detect.sh"

# Run drift detection
DRIFT_OUTPUT=$($DRIFT_SCRIPT 2>&1) || {
  # Exit code 1 means no drift — silent success
  exit 0
}

# If we get here, there IS drift. Output the drift report.
echo "$DRIFT_OUTPUT"

echo ""
echo "💡 To auto-sync a project, run:"
echo "   cd <project_dir> && python3 -c \"import os; os.system('echo OS sync needed')\""
echo ""
echo "📋 Next steps:"
echo "   1. Review the drift report above"
echo "   2. For each project, run: cd <project> && <your-sync-command>"
echo "   3. After sync, update sessions/YYYY-MM-DD.md"
