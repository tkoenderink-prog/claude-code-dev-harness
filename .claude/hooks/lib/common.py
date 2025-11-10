"""
Common utilities for hook system.

Provides:
- File locking for concurrent access
- JSON read/write helpers
- Error logging
- Session ID extraction
- Timestamp formatting
"""

import json
import os
import fcntl
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
from contextlib import contextmanager

# Global paths
PROJECT_DIR = Path(os.environ.get('CLAUDE_PROJECT_DIR', '.')).resolve()
STATE_DIR = PROJECT_DIR / '.claude-state'
LOGS_DIR = STATE_DIR / 'logs'
ERROR_LOG = LOGS_DIR / 'hook-errors.log'

# Ensure directories exist
LOGS_DIR.mkdir(parents=True, exist_ok=True)


@contextmanager
def file_lock(file_path: Path, timeout: float = 1.0):
    """
    Context manager for file locking.

    Args:
        file_path: Path to file to lock
        timeout: Maximum time to wait for lock (seconds)

    Yields:
        File handle

    Raises:
        TimeoutError: If lock cannot be acquired within timeout
    """
    lock_file = Path(str(file_path) + '.lock')
    lock_file.parent.mkdir(parents=True, exist_ok=True)

    start_time = time.time()
    f = None

    try:
        # Create or open lock file
        f = open(lock_file, 'w')

        # Try to acquire lock with timeout
        while True:
            try:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except IOError:
                if time.time() - start_time >= timeout:
                    raise TimeoutError(f"Could not acquire lock on {file_path}")
                time.sleep(0.01)

        yield f

    finally:
        if f:
            try:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                f.close()
            except:
                pass

            # Clean up lock file
            try:
                lock_file.unlink()
            except:
                pass


def log_error(message: str, level: str = "ERROR"):
    """
    Log error message to hook error log.

    Args:
        message: Error message
        level: Log level (ERROR, WARNING, INFO)
    """
    try:
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] [{level}] {message}\n"

        # Append to error log
        with open(ERROR_LOG, 'a') as f:
            f.write(log_entry)

        # Also print to stderr for debugging
        print(log_entry, file=sys.stderr, end='')

    except Exception as e:
        # Silent failure - don't let logging break the hook
        print(f"Failed to log error: {e}", file=sys.stderr)


def load_json(file_path: Path, default: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Load JSON file with error handling.

    Args:
        file_path: Path to JSON file
        default: Default value if file doesn't exist or is invalid

    Returns:
        Parsed JSON data or default value
    """
    try:
        if not file_path.exists():
            return default if default is not None else {}

        with open(file_path, 'r') as f:
            content = f.read().strip()

            # Handle empty file
            if not content:
                return default if default is not None else {}

            return json.loads(content)

    except json.JSONDecodeError as e:
        log_error(f"Invalid JSON in {file_path}: {e}")
        return default if default is not None else {}

    except Exception as e:
        log_error(f"Error loading {file_path}: {e}")
        return default if default is not None else {}


def save_json(file_path: Path, data: Dict[str, Any], indent: int = 2):
    """
    Save JSON file with error handling.

    Args:
        file_path: Path to JSON file
        data: Data to save
        indent: JSON indentation level
    """
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=indent)

    except Exception as e:
        log_error(f"Error saving {file_path}: {e}")
        raise


def get_session_id(hook_input: Dict[str, Any]) -> str:
    """
    Extract session ID from hook input.

    Args:
        hook_input: Hook input dictionary

    Returns:
        Session ID or 'unknown'
    """
    return hook_input.get('session_id',
           hook_input.get('sessionId',
           hook_input.get('parent_session_id', 'unknown')))


def get_month_dir() -> str:
    """
    Get current month directory name (YYYY-MM format).

    Returns:
        Month directory name
    """
    return datetime.now().strftime('%Y-%m')


def format_timestamp() -> str:
    """
    Format current timestamp for filenames.

    Returns:
        Timestamp in YYYY-MM-DD_HH-MM-SS format
    """
    return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


def ensure_permissions(file_path: Path, is_dir: bool = False):
    """
    Set secure permissions on file or directory.

    Args:
        file_path: Path to file or directory
        is_dir: True if path is a directory
    """
    try:
        if is_dir:
            file_path.chmod(0o700)  # rwx------
        else:
            file_path.chmod(0o600)  # rw-------
    except Exception as e:
        log_error(f"Failed to set permissions on {file_path}: {e}", level="WARNING")


# Import sys for stderr logging
import sys
