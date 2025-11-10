"""
Sensitive data sanitizer.

Removes API keys, passwords, tokens, and other sensitive data from content.
"""

import re
from typing import Dict, Pattern

# Sensitive data patterns
SENSITIVE_PATTERNS: Dict[str, Pattern] = {
    'api_key': re.compile(
        r'(api[_-]?key|apikey)\s*[:=]\s*[\'"]?([a-zA-Z0-9_-]{20,})[\'"]?',
        re.IGNORECASE
    ),
    'password': re.compile(
        r'(password|passwd|pwd)\s*[:=]\s*[\'"]?([^\'"\\s]{8,})[\'"]?',
        re.IGNORECASE
    ),
    'token': re.compile(
        r'(token|auth|bearer)\s*[:=]\s*[\'"]?([a-zA-Z0-9._-]{20,})[\'"]?',
        re.IGNORECASE
    ),
    'email': re.compile(
        r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
    ),
    'ssh_key': re.compile(
        r'-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----[\s\S]+?-----END \1 PRIVATE KEY-----'
    ),
    'aws_key': re.compile(
        r'\bAKIA[0-9A-Z]{16}\b'
    ),
    'github_token': re.compile(
        r'\bgh[pousr]_[A-Za-z0-9_]{36,255}\b'
    ),
    'jwt': re.compile(
        r'\beyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b'
    ),
    'private_key_hex': re.compile(
        r'\b[0-9a-fA-F]{64}\b'  # Common for crypto private keys
    ),
    'connection_string': re.compile(
        r'(mongodb|postgresql|mysql|redis)://[^\\s]+:[^\\s]+@[^\\s]+',
        re.IGNORECASE
    ),
}


def sanitize_content(content: str) -> str:
    """
    Remove sensitive data from content.

    Args:
        content: Text content to sanitize

    Returns:
        Sanitized content with sensitive data replaced
    """
    sanitized = content

    for name, pattern in SENSITIVE_PATTERNS.items():
        sanitized = pattern.sub('***REDACTED***', sanitized)

    return sanitized


def sanitize_dict(data: dict) -> dict:
    """
    Recursively sanitize dictionary values.

    Args:
        data: Dictionary to sanitize

    Returns:
        Sanitized dictionary
    """
    result = {}

    for key, value in data.items():
        # Check if key itself is sensitive
        key_lower = key.lower()
        if any(sensitive in key_lower for sensitive in ['password', 'token', 'key', 'secret', 'auth']):
            result[key] = '***REDACTED***'
        elif isinstance(value, str):
            result[key] = sanitize_content(value)
        elif isinstance(value, dict):
            result[key] = sanitize_dict(value)
        elif isinstance(value, list):
            result[key] = [
                sanitize_dict(item) if isinstance(item, dict)
                else sanitize_content(item) if isinstance(item, str)
                else item
                for item in value
            ]
        else:
            result[key] = value

    return result


def is_sensitive(text: str) -> bool:
    """
    Check if text contains sensitive data.

    Args:
        text: Text to check

    Returns:
        True if sensitive data detected
    """
    for pattern in SENSITIVE_PATTERNS.values():
        if pattern.search(text):
            return True

    return False
