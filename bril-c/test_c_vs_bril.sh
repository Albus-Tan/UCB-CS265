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
    echo "Testing $FILE..."
    BASENAME=$(basename "$FILE" .c)
    C_EXEC="$TMP_DIR/${BASENAME}_c_exec"
    BRIL_PROG="$TMP_DIR/${BASENAME}_bril.json"

    # Step 1: Compile and run the C program
    gcc "$FILE" -o "$C_EXEC"
    if [ $? -ne 0 ]; then
        echo "Failed to compile $FILE with gcc."
        continue
    fi
    C_OUTPUT=$("$C_EXEC")

    # Step 2: Use driver.py to convert and run the Bril program
    python3 ./c/driver.py "$FILE" > "$BRIL_PROG"
    BRIL_OUTPUT=$(brili < "$BRIL_PROG" 2>/dev/null)

    # Step 3: Compare outputs
    if [ "$C_OUTPUT" = "$BRIL_OUTPUT" ]; then
        echo "PASS: Output matches"
    else
        echo "FAIL: Output mismatch"
        echo "C Output: $C_OUTPUT"
        echo "Bril Output: $BRIL_OUTPUT"
    fi

    echo "---------------------------------"
done
