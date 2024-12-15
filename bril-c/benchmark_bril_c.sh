#!/bin/bash

# Check arguments
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <c-file-or-directory>"
    exit 1
fi

# Get input path
INPUT_PATH=$1

# Create a temporary directory for intermediate files
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT  # Remove the temporary directory when the script exits

# Process file or directory
if [ -d "$INPUT_PATH" ]; then
    FILES=$(find "$INPUT_PATH" -name "*.c")
elif [ -f "$INPUT_PATH" ]; then
    FILES=$INPUT_PATH
else
    echo "Invalid input path: $INPUT_PATH"
    exit 1
fi

# Iterate over each C file
for FILE in $FILES; do
    BASENAME=$(basename "$FILE" .c)
    BRIL_PROG="$TMP_DIR/${BASENAME}_bril.json"

    # Step 1: Use driver.py to convert and run the Bril program
    python3 ./core/driver.py "$FILE" > "$BRIL_PROG"
    BRIL_OUTPUT=$(brili -p < "$BRIL_PROG" 2>&1)

    # Step 2: Extract the total_dyn_inst from the Bril output
    BRIL_INST=$(echo "$BRIL_OUTPUT" | grep -oP 'total_dyn_inst: \K\d+')

    echo "${BASENAME},$BRIL_INST"
done
