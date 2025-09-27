# Error Tracking System

A lightweight, file-based error tracking system that keeps count of how many times you fix the same errors during development.

## Features

- **Error Counting**: Tracks how many times each unique error has been fixed
- **Session Management**: Maintains session statistics across development sessions
- **File-based Storage**: Uses JSON files for simple, portable data storage
- **CLI Interface**: Easy-to-use command-line interface
- **Quick Tracking**: Bash script for rapid error recording

## Files

- `simple_error_tracker.py` - Main error tracking system
- `track_error.sh` - Quick bash script for recording errors
- `error_tracking_data.json` - Data storage file (auto-created)

## Usage

### Recording Errors

```bash
# Using the Python CLI
python simple_error_tracker.py record -t "SyntaxError" -m "Missing closing bracket" -f "demo.py" -l 42

# Using the quick script
./track_error.sh "TypeError" "Type annotation error" "myfile.py" 123
```

### Viewing Statistics

```bash
# Current session stats
python simple_error_tracker.py stats

# Detailed report
python simple_error_tracker.py report

# Most frequent errors
python simple_error_tracker.py frequent
```

### Starting New Sessions

```bash
python simple_error_tracker.py session
```

## Command Reference

### Record Command
```bash
python simple_error_tracker.py record [OPTIONS]

Options:
  -t, --type TEXT         Error type (required)
  -m, --message TEXT      Error message (required)
  -f, --file TEXT         File path (optional)
  -l, --line INTEGER      Line number (optional)
  -d, --description TEXT  Fix description (optional)
```

### Quick Script
```bash
./track_error.sh <error_type> <error_message> [file_path] [line_number]
```

## Example Workflow

1. Start a new development session:
   ```bash
   python simple_error_tracker.py session
   ```

2. As you encounter and fix errors, record them:
   ```bash
   ./track_error.sh "ImportError" "Module not found" "main.py" 15
   ./track_error.sh "SyntaxError" "Missing comma" "utils.py" 42
   ```

3. Check your progress:
   ```bash
   python simple_error_tracker.py stats
   python simple_error_tracker.py report
   ```

## Data Storage

The system stores data in `error_tracking_data.json` with the following structure:

```json
{
  "session": {
    "start_time": "2025-09-15T21:19:01.040265",
    "total_fixes": 2,
    "unique_errors": 2
  },
  "errors": {
    "error_hash": {
      "type": "ImportError",
      "message": "Import could not be resolved",
      "file_path": "error_tracker_cli.py",
      "line_number": 13,
      "count": 1,
      "first_seen": "2025-09-15T21:19:01.040294",
      "last_seen": "2025-09-15T21:19:01.040294",
      "fixes": []
    }
  }
}
```

## Benefits

- **Pattern Recognition**: Identify recurring issues in your codebase
- **Learning Tool**: Track your progress in fixing common errors
- **Development Insights**: Understand which types of errors you encounter most
- **Session Tracking**: Monitor productivity across development sessions
- **Lightweight**: No database setup required, just JSON files

## Getting Started

1. Make the quick script executable:
   ```bash
   chmod +x track_error.sh
   ```

2. Start your first session:
   ```bash
   python simple_error_tracker.py session
   ```

3. Begin tracking errors as you fix them!

Happy debugging! 🐛➡️✅