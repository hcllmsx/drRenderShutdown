#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE="$SCRIPT_DIR/RenderShutdown-hcllmsx.py"
TARGET="$HOME/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Deliver"

if [ ! -f "$SOURCE" ]; then
    echo "ERROR: RenderShutdown-hcllmsx.py was not found next to this installer."
    echo "Expected: $SOURCE"
    read -r -p "Press Return to close this window. "
    exit 1
fi

if ! mkdir -p "$TARGET"; then
    echo "ERROR: Could not create the DaVinci Resolve script folder."
    echo "Target: $TARGET"
    read -r -p "Press Return to close this window. "
    exit 1
fi

if ! cp -f "$SOURCE" "$TARGET/RenderShutdown-hcllmsx.py"; then
    echo "ERROR: Could not copy the script."
    echo "Target: $TARGET"
    read -r -p "Press Return to close this window. "
    exit 1
fi
echo "Installation complete."
echo "Script: $TARGET/RenderShutdown-hcllmsx.py"
echo "Restart DaVinci Resolve, then choose this script and set the trigger to End."
read -r -p "Press Return to close this window. "
