# Validate a name field with length constraints and required check.
def validate_name(name_value, label):
    if not name_value:
        return str(label)+" is required."
    if len(name_value) < 2:
        return str(label)+" must be at least 2 characters."
    if len(name_value) > 20:
        return str(label)+" must be less than 20 characters."
    return ""


# Validate email format and required constraints.
def validate_email(email):
    if not email:
        return "Email is required."
    if len(email) < 8:
        return "Email must be at least 8 characters."
    if len(email) > 34:
        return "Email must be less than 35 characters."
    if " " in email:
        return "Email cannot contain spaces."
    if "@" not in email:
        return "Email must contain '@'."
    if email.startswith("@"):
        return "'@' cannot be the first character."
    if email.endswith("@"):
        return "'@' cannot be the last character."
    if email.count("@") != 1:
        return "Email can contain only one '@'."
    if "." not in email:
        return "Email must contain a dot ('.')."
    at_index = email.index("@")
    if "." not in email[at_index:]:
        return "Email must contain a dot ('.') after '@'."
    if not email.endswith(".com"):
        return "Email must end with '.com'."
    return ""


# Validate username with length and space constraints.
def validate_username(username):
    if not username:
        return "Username is required."
    if len(username) < 8:
        return "Username must be at least 8 characters."
    if len(username) > 35:
        return "Username must be less than 35 characters."
    if " " in username:
        return "Username cannot contain spaces."
    return ""


# Validate password with length, space, and special characters requirements.
def validate_password(password):
    if not password:
        return "Password is required."
    if len(password) < 8:
        return "Password must be at least 8 characters."
    if len(password) > 35:
        return "Password must be less than 35 characters."
    if " " in password:
        return "Password cannot contain spaces."
    special_chars = "!@#$%^&*()_+-=[]{}|;:'\",.<>/?`~"
    has_special = any(ch in special_chars for ch in password)
    has_number = any(ch.isdigit() for ch in password)
    has_upper = any(ch.isupper() for ch in password)
    has_lower = any(ch.islower() for ch in password)
    conditions_met = sum([has_special, has_number, has_upper, has_lower])
    if conditions_met < 4:
        return "Password must contain at least 4 of the following: lowercase letters, uppercase letters, numbers, special characters."
    return ""


