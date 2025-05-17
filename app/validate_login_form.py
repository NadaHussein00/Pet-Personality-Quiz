
from app.helpers import hash_password

#This function is to check if the hashed passwords, one is the hashed password from the password field in 
#the login form, and the hashed password from the stored hashed password in the json file
def check_password(stored_hash, password_attempt):
    return stored_hash == hash_password(password_attempt)


#This function is to check if the user is found in the user's email is in the json file
#and if it doesn't exist, it returns none (falsey value??)
def find_user_by_email(email, users):
    for user in users:
        if user.get('email', '').lower() == email.lower(): 
            return user
    return None

#This function is to check whether one of the fields of the login form is empty
#and if both of them are provided, then it returns the errors dictionary empty
def validate_login_fields(email, password):
    errors = {}
    if not email:
        errors['email'] = "Email is required."
    if not password:
        errors['password'] = "Password is required."
    return errors


#This function is to check if the user exists by checking if the email is found or not
#if it is found, then the user is returned
#and if it is not found, then it returns an error message (why returning two value??)
def validate_user_exists(email, users):
    user = find_user_by_email(email, users)
    if not user:
        return None, "No account with that email."
    return user, ""


#This function is to check if the user's password entered (hashed) in the login field
#is matching with the hashed password that's stored in the json file.
def validate_password_login(user, password):
    if not check_password(user['password'], password):
        return "Incorrect password."
    return ""

