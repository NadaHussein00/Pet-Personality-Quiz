import json

def load_json_file(filepath):
    try:
        file = open(filepath, "r")
        data = json.load(file)
        file.close()
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_json_file(filepath, data):
    file = open(filepath, "w")
    json.dump(data, file, indent=2)
    file.close()


def hash_password(password):
    ascii_values = []  # List to hold ASCII codes as strings

    for char in password:
        ascii_code = ord(char)       # Get ASCII integer value of the character
        ascii_str = str(ascii_code)  # Convert ASCII code to string
        ascii_values.append(ascii_str)  # Append to the list

    hashed_password = ''.join(ascii_values)  # Concatenate all ASCII strings into one
    return hashed_password

def get_html(page_name):
    templates_folder = "templates"
    file_path = templates_folder + "/" + page_name + ".html" 
    html_file=open(file_path)
    content=html_file.read()
    html_file.close()
    return content
