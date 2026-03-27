"""
Solution 2: Find the Last Person to Access the System

This script finds the user who accessed the system most recently
by comparing all last_login timestamps.

Please read the README for details.
"""

import json
from datetime import datetime, timezone
from typing import Dict, Any, Optional


def _parse_last_login(raw_value: Any) -> datetime:
    """Return a timezone-aware UTC datetime for robust comparisons/sorting."""
    if not raw_value:
        return datetime.min.replace(tzinfo=timezone.utc)

    value = str(raw_value)
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        return datetime.min.replace(tzinfo=timezone.utc)

    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def get_last_accessed_user(json_file: str) -> Optional[Dict[str, Any]]:
    """
    Find the user who accessed the system most recently.
    
    Args:
        json_file: Path to the userData.json file
        
    Returns:
        Dictionary containing the user's information, or None if no users found
    
    Example:
        >>> user = get_last_accessed_user('userData.json')
        >>> print(f"Last accessed: {user['first_name']} {user['last_name']}")
        Last accessed: Jane Smith
    """
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        users = data.get('users', [])
        
        if not users:
            print("No users found in the database.")
            return None
        
        # Find user with the latest last_login timestamp
        latest_user = max(
            users,
            key=lambda u: _parse_last_login(u.get('last_login'))
        )
        
        return latest_user
        
    except FileNotFoundError:
        print(f"✗ Error: File '{json_file}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"✗ Error: Invalid JSON format in '{json_file}'")
        return None
    except Exception as e:
        print(f"✗ Error retrieving last accessed user: {e}")
        return None


def print_user_info(user: Dict[str, Any]) -> None:
    """Pretty print user information."""
    print(f"✓ Last accessed user: {user.get('first_name')} {user.get('last_name')}")
    print(f"  User ID: {user.get('user_id')}")
    print(f"  Email: {user.get('email')}")
    print(f"  Role: {user.get('role', 'N/A')}")
    print(f"  Phone: {user.get('phone', 'N/A')}")
    print(f"  Active: {user.get('is_active', 'N/A')}")
    print(f"  Last login: {user.get('last_login', 'N/A')}")


def get_all_users_sorted_by_access(json_file: str) -> list:
    """
    Get all users sorted by last access time (most recent first).
    
    Args:
        json_file: Path to the userData.json file
        
    Returns:
        List of users sorted by last login (descending)
    """
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        users = data.get('users', [])
        
        # Sort by last_login in descending order (most recent first)
        sorted_users = sorted(
            users,
            key=lambda u: _parse_last_login(u.get('last_login')),
            reverse=True
        )
        
        return sorted_users
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return []


def main():
    """Demo script to find the last accessed user."""
    
    json_file = 'userData.json'
    
    print("=" * 60)
    print("Solution 2: Find the Last Person to Access the System")
    print("=" * 60)
    print()
    
    # Get the last accessed user
    last_user = get_last_accessed_user(json_file)
    
    if last_user:
        print_user_info(last_user)
    else:
        print("No valid last accessed user found.")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
