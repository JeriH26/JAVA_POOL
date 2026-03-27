"""
Solution 1: Add a New User to the User Records

This script demonstrates how to add a new user to the JSON user database.
If a user with the same first name, last name, and email already exists,
the existing record is updated instead of creating a duplicate.

Please read the README for details.
"""

import json
from datetime import datetime, timezone
from typing import Dict, Any


def _normalize_text(value: Any) -> str:
    return str(value or '').strip().lower()


def _build_user_record(user_id: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'user_id': user_id,
        'first_name': user_data.get('first_name'),
        'last_name': user_data.get('last_name'),
        'email': user_data.get('email'),
        'role': user_data.get('role', 'User'),
        'address': user_data.get('address'),
        'phone': user_data.get('phone'),
        'is_active': user_data.get('is_active', True),
        'last_login': user_data.get('last_login'),
    }


def add_new_user(json_file: str, new_user: Dict[str, Any]) -> bool:
    """
    Add a new user or update an existing matching user in the JSON file.
    
    Args:
        json_file: Path to the userData.json file
        new_user: Dictionary containing user data
        
    Returns:
        True if successful, False otherwise
    
    Example:
        >>> new_user = {
        ...     "first_name": "Bob",
        ...     "last_name": "Wilson",
        ...     "email": "bobwilson@xyz.com",
        ...     "role": "User",
        ...     "phone": "+1-252-9999",
        ...     "is_active": True
        ... }
        >>> add_new_user('userData.json', new_user)
        ✓ User Bob updated successfully with ID 46
    """
    try:
        # Load existing data
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Initialize users list if it doesn't exist
        if not data.get('users'):
            data['users'] = []

        first_name = _normalize_text(new_user.get('first_name'))
        last_name = _normalize_text(new_user.get('last_name'))
        email = _normalize_text(new_user.get('email'))
        
        # Find next user_id (max existing ID + 1)
        max_id = max([u.get('user_id', 0) for u in data['users']], default=0)
        next_user_id = max_id + 1
        
        # Add a default last_login timestamp if not provided
        if 'last_login' not in new_user:
            new_user['last_login'] = datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')

        existing_index = next(
            (
                index for index, user in enumerate(data['users'])
                if _normalize_text(user.get('first_name')) == first_name
                and _normalize_text(user.get('last_name')) == last_name
                and _normalize_text(user.get('email')) == email
            ),
            None,
        )

        if existing_index is not None:
            existing_user_id = data['users'][existing_index].get('user_id', next_user_id)
            user_record = _build_user_record(existing_user_id, new_user)
            data['users'][existing_index] = user_record
            action = 'updated'
        else:
            user_record = _build_user_record(next_user_id, new_user)
            data['users'].append(user_record)
            action = 'added'
        
        # Write back to file
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)
        
        print(f"✓ User {user_record.get('first_name')} {action} successfully with ID {user_record['user_id']}")
        return True
        
    except FileNotFoundError:
        print(f"✗ Error: File '{json_file}' not found.")
        return False
    except json.JSONDecodeError:
        print(f"✗ Error: Invalid JSON format in '{json_file}'")
        return False
    except Exception as e:
        print(f"✗ Error adding user: {e}")
        return False


def main():
    """Demo script to add a new user."""
    
    json_file = 'userData.json'
    
    # Define a new user
    new_user = {
        "first_name": "Bob",
        "last_name": "Wilson",
        "email": "bobwilson@xyz.com",
        "role": "User",
        "address": {
            "street": "999 Oak Ave",
            "city": "Boston",
            "state": "MA",
            "zip_code": "02101"
        },
        "phone": "+1-252-9999",
        "is_active": True
    }
    
    print("=" * 60)
    print("Solution 1: Adding a New User")
    print("=" * 60)
    print(f"\nAdding user: {new_user['first_name']} {new_user['last_name']}")
    print(f"Email: {new_user['email']}")
    print(f"Role: {new_user['role']}\n")
    
    # Add the user
    success = add_new_user(json_file, new_user)
    
    # Display result
    if success:
        print("\nSaved user record:")
        with open(json_file, 'r') as f:
            data = json.load(f)
            saved_user = next(
                (
                    user for user in data['users']
                    if _normalize_text(user.get('first_name')) == _normalize_text(new_user.get('first_name'))
                    and _normalize_text(user.get('last_name')) == _normalize_text(new_user.get('last_name'))
                ),
                None,
            )
            if saved_user:
                print(json.dumps(saved_user, indent=2))
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
