#!/bin/bash

# Function to normalize C output for boolean context
normalize_bool_output() {
    local c_output=$1
    local bril_output=$2

    # Split outputs line by line
    IFS=$'\n' read -d '' -r -a c_lines <<< "$c_output"
    IFS=$'\n' read -d '' -r -a bril_lines <<< "$bril_output"

    # Normalize only boolean contexts
    for i in "${!c_lines[@]}"; do
        if [[ "${bril_lines[$i]}" == "true" || "${bril_lines[$i]}" == "false" ]]; then
            if [[ "${c_lines[$i]}" == "1" ]]; then
                c_lines[$i]="true"
            elif [[ "${c_lines[$i]}" == "0" ]]; then
                c_lines[$i]="false"
            fi
        fi
    done

    # Join lines back
    printf "%s\n" "${c_lines[@]}"
}

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

ALL_PASSED=true  # Flag to check if all tests pass

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
    python3 ./core/driver.py "$FILE" > "$BRIL_PROG"
    BRIL_OUTPUT=$(brili < "$BRIL_PROG" 2>/dev/null)

    # Step 3: Normalize and compare outputs
    NORMALIZED_C_OUTPUT=$(normalize_bool_output "$C_OUTPUT" "$BRIL_OUTPUT")

    if [ "$NORMALIZED_C_OUTPUT" = "$BRIL_OUTPUT" ]; then
        echo "PASS: Output matches"
    else
        echo "FAIL: Output mismatch"
        echo "C Output: "
        echo "$C_OUTPUT"
        echo "C Output (bool replaced): "
        echo "$NORMALIZED_C_OUTPUT"
        echo "Bril Output: "
        echo "$BRIL_OUTPUT"
        ALL_PASSED=false
    fi

    echo "---------------------------------"
done

# Final summary
if [ "$ALL_PASSED" = true ]; then
    echo "All tests passed."
else
    echo "Some tests failed."
fi