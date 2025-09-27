#!/bin/bash

# Quick Error Tracking Script
# Usage: ./track_error.sh "SyntaxError" "missing closing bracket" "demo.py" 147

if [ $# -lt 2 ]; then
    echo "Usage: $0 <error_type> <error_message> [file_path] [line_number]"
    echo "Example: $0 'SyntaxError' 'missing closing bracket' 'demo.py' 147"
    exit 1
fi

ERROR_TYPE="$1"
ERROR_MESSAGE="$2"
FILE_PATH="${3:-}"
LINE_NUMBER="${4:-}"

# Build the command
CMD="python simple_error_tracker.py record -t '$ERROR_TYPE' -m '$ERROR_MESSAGE'"

if [ -n "$FILE_PATH" ]; then
    CMD="$CMD -f '$FILE_PATH'"
fi

if [ -n "$LINE_NUMBER" ]; then
    CMD="$CMD -l $LINE_NUMBER"
fi

# Execute the command
eval $CMD

# Show current stats
echo ""
echo "📊 Current Session:"
python simple_error_tracker.py stats | tail -3