"""
Solution 3: Handle Data Validation and Missing/Unexpected Fields

This script validates user records, handles missing fields with defaults,
and removes unexpected fields to ensure data consistency.

Please read the README for details.
"""

import json
from datetime import datetime, timezone
from typing import Dict, Any, List, Tuple


class UserValidator:
    """Validate and sanitize user records."""
    
    # Define the expected schema
    REQUIRED_FIELDS = {
        'first_name', 'last_name', 'email', 'user_id'
    }
    
    OPTIONAL_FIELDS = {
        'role', 'address', 'phone', 'is_active', 'last_login'
    }
    
    ALLOWED_FIELDS = REQUIRED_FIELDS | OPTIONAL_FIELDS

    # Preserve deterministic output order for cleaned records.
    FIELD_ORDER = [
        'user_id',
        'first_name',
        'last_name',
        'email',
        'role',
        'address',
        'phone',
        'is_active',
        'last_login',
    ]
    
    @staticmethod
    def validate_user(user: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate a single user record against the schema.
        
        Args:
            user: User dictionary to validate
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        
        Example:
            >>> user = {"first_name": "John", "email": "john@xyz.com"}
            >>> is_valid, errors = UserValidator.validate_user(user)
            >>> print(errors)
            ['Missing required field: \'user_id\'', 'Missing required field: \'last_name\'']
        """
        errors = []
        
        # Check for missing required fields
        for field in UserValidator.REQUIRED_FIELDS:
            if field not in user:
                errors.append(f"Missing required field: '{field}'")
        
        # Validate email format (simple check)
        if 'email' in user:
            if '@' not in user['email'] or '.' not in user['email']:
                errors.append(f"Invalid email format: {user['email']}")
        
        # Validate user_id is numeric
        if 'user_id' in user and not isinstance(user['user_id'], int):
            errors.append(f"user_id must be an integer, got {type(user['user_id'])}")
        
        # Validate is_active is boolean
        if 'is_active' in user and not isinstance(user['is_active'], bool):
            errors.append(f"is_active must be boolean, got {type(user['is_active'])}")
        
        return len(errors) == 0, errors

    @staticmethod
    def get_cleanup_changes(user: Dict[str, Any], sanitized: Dict[str, Any]) -> List[str]:
        """Describe fixable cleanup changes for an otherwise valid record."""
        changes = []

        unexpected_fields = set(user.keys()) - UserValidator.ALLOWED_FIELDS
        if unexpected_fields:
            changes.append(f"Remove unexpected fields: {sorted(unexpected_fields)}")

        if 'role' not in user:
            changes.append("Add default role='User'")

        if 'is_active' not in user:
            changes.append("Add default is_active=True")

        if 'last_login' not in user:
            changes.append("Add default last_login timestamp")

        if user != sanitized and not changes:
            changes.append("Normalize record structure")

        return changes
    
    @staticmethod
    def sanitize_user(user: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean and normalize user record.
        
        Removes unexpected fields and applies defaults for missing optional fields.
        
        Args:
            user: User dictionary to sanitize
            
        Returns:
            Cleaned user dictionary with only allowed fields and defaults applied
        
        Example:
            >>> user = {"user_id": 1, "first_name": "John", "last_name": "Doe", 
            ...         "email": "john@xyz.com", "extra_field": "should_be_removed"}
            >>> cleaned = UserValidator.sanitize_user(user)
            >>> "extra_field" in cleaned
            False
            >>> cleaned["is_active"]
            True
        """
        sanitized = {}
        
        # Keep only allowed fields, using fixed field order.
        for field in UserValidator.FIELD_ORDER:
            if field in user:
                sanitized[field] = user[field]
        
        # Apply defaults for missing optional fields
        if 'is_active' not in sanitized:
            sanitized['is_active'] = True
        
        if 'role' not in sanitized:
            sanitized['role'] = 'User'
        
        if 'last_login' not in sanitized:
            sanitized['last_login'] = datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
        
        return sanitized
    
    @staticmethod
    def validate_and_load_json(
        json_file: str,
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Load JSON file and validate/sanitize all user records.
        
        Args:
            json_file: Path to userData.json file
            
        Returns:
            Tuple of (valid_users_sanitized, invalid_users_with_details, cleanup_candidates)
        
        Example:
            >>> valid, invalid = UserValidator.validate_and_load_json('userData.json')
            >>> print(f"Valid: {len(valid)}, Invalid: {len(invalid)}")
            Valid: 3, Invalid: 0
        """
        valid_users = []
        invalid_users = []
        cleanup_candidates = []
        
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            users = data.get('users', [])
            
            for idx, user in enumerate(users):
                is_valid, errors = UserValidator.validate_user(user)
                
                if is_valid:
                    sanitized = UserValidator.sanitize_user(user)
                    valid_users.append(sanitized)
                    cleanup_changes = UserValidator.get_cleanup_changes(user, sanitized)
                    if cleanup_changes:
                        cleanup_candidates.append({
                            'index': idx,
                            'original': user,
                            'cleaned': sanitized,
                            'changes': cleanup_changes,
                        })
                else:
                    invalid_users.append({
                        'index': idx,
                        'user': user,
                        'errors': errors
                    })
            
            return valid_users, invalid_users, cleanup_candidates
            
        except FileNotFoundError:
            print(f"✗ Error: File '{json_file}' not found.")
            return [], [], []
        except json.JSONDecodeError as e:
            print(f"✗ JSON parsing error: {e}")
            return [], [], []
        except Exception as e:
            print(f"✗ Error loading file: {e}")
            return [], [], []


def save_cleaned_users(json_file: str, valid_users: List[Dict[str, Any]]) -> bool:
    """
    Save validated and sanitized users back to JSON file.
    
    Args:
        json_file: Path to userData.json file
        valid_users: List of cleaned user records
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(json_file, 'w') as f:
            json.dump({'users': valid_users}, f, indent=4)
        print(f"✓ Saved {len(valid_users)} cleaned records back to {json_file}")
        return True
    except Exception as e:
        print(f"✗ Error saving file: {e}")
        return False


def print_validation_report(
    valid_users: List[Dict[str, Any]],
    invalid_users: List[Dict[str, Any]],
    cleanup_candidates: List[Dict[str, Any]],
) -> None:
    """Print a detailed validation report."""
    
    print("=" * 60)
    print("Data Validation Report")
    print("=" * 60)
    print()
    
    # Summary
    print(f"✓ Valid records: {len(valid_users)}")
    print(f"✗ Invalid records: {len(invalid_users)}")
    print(f"⚠ Records needing cleanup: {len(cleanup_candidates)}")
    print()
    
    # Details of invalid records
    if invalid_users:
        print("-" * 60)
        print("Invalid Records Details:")
        print("-" * 60)
        
        for invalid in invalid_users:
            print(f"\nRecord #{invalid['index']}:")
            user_name = f"{invalid['user'].get('first_name', 'Unknown')} {invalid['user'].get('last_name', 'Unknown')}"
            print(f"  User: {user_name}")
            print(f"  Errors:")
            for error in invalid['errors']:
                print(f"    • {error}")
    
    if cleanup_candidates:
        print("-" * 60)
        print("Records That Can Be Auto-Cleaned:")
        print("-" * 60)
        for candidate in cleanup_candidates:
            original = candidate['original']
            user_name = f"{original.get('first_name', 'Unknown')} {original.get('last_name', 'Unknown')}"
            print(f"\nRecord #{candidate['index']}: {user_name}")
            for change in candidate['changes']:
                print(f"  • {change}")
        print()

    print("=" * 60)


def main():
    """Demo script for data validation and cleanup."""
    
    json_file = 'userData.json'
    
    print("\n")
    print("=" * 60)
    print("Solution 3: Handle Data Validation and Field Consistency")
    print("=" * 60)
    print()
    
    # Load and validate all users
    print("Loading and validating user records...")
    print()
    
    valid_users, invalid_users, cleanup_candidates = UserValidator.validate_and_load_json(json_file)
    
    # Print validation report
    print_validation_report(valid_users, invalid_users, cleanup_candidates)

    if not invalid_users and not cleanup_candidates:
        print("No problems found. Data is already clean, so no changes were made.")
        print("\n" + "=" * 60)
        return

    if invalid_users:
        print("Invalid records need manual fixes before saving cleaned data.")

    if cleanup_candidates and not invalid_users:
        response = input("\nAuto-fix cleanable records and save changes? (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            save_cleaned_users(json_file, valid_users)
            print("\nCleaned data saved successfully!")
        else:
            print("\nNo changes were saved.")

    if cleanup_candidates:
        print("\n" + "-" * 60)
        print("Sample of cleaned record (first user):")
        print("-" * 60)
        print(json.dumps(valid_users[0], indent=2))
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
