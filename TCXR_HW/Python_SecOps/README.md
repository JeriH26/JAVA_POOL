# User Records Management System

This folder contains solutions for managing user records stored in JSON format.

## Problem Overview

Given a website's user records in a JSON file, we need to handle three key operations using Python:

1. How would you add a new user to our records?
2. Who was the last person to access our system?
3. What will you do if our records contain unexpected fields or are missing fields?

---

## Data Structure

The `userData.json` file contains a list of user objects with the following schema:

```json
{
  "users": [
    {
      "user_id": 1,
      "first_name": "John",
      "last_name": "Doe",
      "email": "johndoe@xyz.com",
      "role": "User",
      "address": {
        "street": "123 Main St",
        "city": "New York",
        "state": "NY",
        "zip_code": 10001
      },
      "phone": "+1-252-1234",
      "is_active": true,
      "last_login": "2025-03-28T08:30:00Z"
    }
  ]
}
```

---

## Solution 1: Adding a New User

### Approach

When adding a new user, we need to:
- Find the next available `user_id` (max existing ID + 1)
- Validate required fields
- Append the new user to the list
- Search for first name and last name, and email, if user are the same, then update information for same users.
- Write back to the JSON file

**Implementation:** see `solution1_add_user.py`

```bash
python solution1_add_user.py
```

---

## Solution 2: Finding the Last Person to Access the System

### Approach

To find who accessed the system most recently, we need to:
- Parse all `last_login` timestamps
- Compare them to find the maximum (most recent) timestamp
- Return the user information

**Implementation:** see `solution2_last_accessed.py`

```bash
python solution2_last_accessed.py
```

**Sample output (will vary based on current `userData.json`):**
```
✓ Last accessed user: Bob Brown
    User ID: 4
    Email: bobbrown@xyz.com
    Role: User
    Phone: +1-252-4321
    Active: True
    Last login: 2026-09-27T16:00:00Z
```

---

## Solution 3: Handling Data Validation and Missing/Unexpected Fields

### Approach

To handle data quality issues, we implement:
- **Validate first**: Check every record and report whether data is clean.
- **No-op when clean**: If no errors and no cleanup candidates are found, do not modify or save anything.
- **Fix only when needed**: If cleanup issues are found (unexpected fields, missing optional values, structure normalization), offer auto-fix and then save.
- **Manual-fix path for invalid data**: If hard validation errors exist (missing required fields, invalid types/formats), report them for manual correction before saving.

**Implementation:** see `solution3_validation.py`

```bash
python solution3_validation.py
```

---

## Key Takeaways

| Question | Solution |
|---|---|
| **Add new user** | Load JSON → Find max ID → Append new user → Save |
| **Last accessed user** | Parse all timestamps → Find max → Return user |
| **Handle bad data** | Validate schema → Sanitize fields → Apply defaults → Log errors |

## Best Practices

### 1. Always validate before processing
Check required fields exist before doing anything with the data.

```python
# ❌ Bad - directly access fields without checking
def process_user(user):
    print(user["email"])  # crashes with KeyError if email is missing

# ✅ Good - validate first
def process_user(user):
    if "email" not in user:
        print("Skipping: missing email")
        return
    print(user["email"])
```

---

### 2. Use defaults for missing fields
Prevent `KeyError` by filling in sensible defaults when optional fields are absent.

```python
# ❌ Bad - crashes if 'role' is not in the record
print(user["role"])  # KeyError!

# ✅ Good - provide a default value
print(user.get("role", "User"))  # returns "User" if missing

# ✅ Also good - fill in before saving
if "is_active" not in user:
    user["is_active"] = True
```

---

### 3. Remove unexpected fields
Strip fields that don't belong to keep data clean and prevent injection attacks.

```python
# Suppose a bad actor sends this record:
bad_user = {
    "user_id": 5,
    "first_name": "Hacker",
    "last_name": "X",
    "email": "hack@xyz.com",
    "admin_override": True,   # ← unexpected! should not be saved
    "injected_script": "<script>alert(1)</script>"  # ← dangerous!
}

ALLOWED_FIELDS = {"user_id", "first_name", "last_name", "email", "role",
                  "address", "phone", "is_active", "last_login"}

# ✅ Good - whitelist filter strips anything not allowed
cleaned = {k: v for k, v in bad_user.items() if k in ALLOWED_FIELDS}
# Result: admin_override and injected_script are gone
```

---

### 4. Log validation errors
Don't silently skip bad records — record what went wrong so you can fix it later.

```python
# ❌ Bad - silently ignores bad data
for user in users:
    if "email" not in user:
        continue  # you'll never know this record was skipped

# ✅ Good - log the problem
for idx, user in enumerate(users):
    if "email" not in user:
        print(f"Record #{idx} skipped: missing 'email' field")
        invalid_users.append({"index": idx, "user": user, "error": "missing email"})
```

---

### 5. Atomic writes
Load the whole file, modify in memory, then save once. Never write partially.

```python
# ❌ Bad - opens file for writing immediately, data is lost if crash happens mid-way
with open("userData.json", "w") as f:
    for user in users:
        f.write(json.dumps(user))  # if this crashes halfway, file is corrupted

# ✅ Good - modify in memory first, write once at the end
with open("userData.json", "r") as f:
    data = json.load(f)          # 1. load everything

data["users"].append(new_user)   # 2. modify in memory

with open("userData.json", "w") as f:
    json.dump(data, f, indent=4) # 3. write back all at once
```

---

### 6. Error handling
Catch specific errors so the program doesn't crash and users get a clear message.

```python
# ❌ Bad - no error handling, crashes with ugly traceback
with open("userData.json", "r") as f:
    data = json.load(f)

# ✅ Good - handle expected failure cases
try:
    with open("userData.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    print("Error: userData.json not found. Please check the file path.")
except json.JSONDecodeError:
    print("Error: userData.json is corrupted or not valid JSON.")
except Exception as e:
    print(f"Unexpected error: {e}")
```
