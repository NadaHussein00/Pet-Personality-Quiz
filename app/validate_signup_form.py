
#instead of makeing two separate functions for the first name and last name field
# then it is better to make one function that has the same logic. DRY concept.
def validate_name(name_value, label):
    if not name_value:
        return str(label)+" is required."
    if len(name_value) < 2:
        return str(label)+" must be at least 2 characters."
    if len(name_value) > 20:
        return str(label)+" must be less than 20 characters."
    return ""


#This function is for validating the email, it checks the following:
#1- check if the field is empty.
#2- check if the email is less than 8 characters long
#3- check if the email is more than 35 characters long
#4- check if the email contains any spaces
#5- check if the email does not contain the @ character
#6- check if the email contains the character @ at the start of it
#7- check if the email contains the character @ at the end of it
#8- check if the email contains the character @ more than one time
#9- check if the email does not contain the character . at all
#10- check if the email does not contain the character . AFTER the @ character 
#11- check if the email does not end with the .com substring
#12- if the email passes all these checks then return an empty string as the error message

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


#This function is for validating the username, it checks the following:
#1- check if the field is empty.
#2- check if the username is less than 8 characters long
#3- check if the username is more than 35 characters long
#4- check if the username contains any spaces
#5- if the username passes all these checks then return an empty string as the error message

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


#This function is for validating the password, it checks the following:
#1- check if the field is empty.
#2- check if the password is less than 8 characters long
#3- check if the password is more than 35 characters long
#4- check if the password contains any spaces
#5- check if the password does not contain any special character,
#along with any numbers, any lower or upper case letters
#6- if the password passes all these checks then return an empty string as the error message

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



