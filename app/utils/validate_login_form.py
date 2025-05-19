from app.utils.helpers import hash_password

#This function is to check if the entered password matches the stored hashed password
def check_password(stored_hash, password_attempt):
    return stored_hash == hash_password(password_attempt)


# Find a user by email in the users list, return user if found or None if not found
def find_user_by_email(email, users):
    for user in users:
        if user.get('email', '').lower() == email.lower(): 
            return user
    return None

# Validate that email and password fields are not empty, return errors if any
def validate_login_fields(email, password):
    errors = {}
    if not email:
        errors['email'] = "Email is required."
    if not password:
        errors['password'] = "Password is required."
    return errors


# Check if user exists by the email, return user if found and error message if not found
def validate_user_exists(email, users):
    user = find_user_by_email(email, users)
    if not user:
        return None, "No account with that email."
    return user, ""


# Validate if the entered password matches the user's stored password
def validate_password_login(user, password):
    if not check_password(user['password'], password):
        return "Incorrect password."
    return ""
