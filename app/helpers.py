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

#This file contains the made-from-scratch hash function.
#First, each character is mapped to its ascii value
#Second, each ascii value is then multiplied to 16
#Third, each number that is processed from the second step, is mapped to its hexa digits that represent it
#and then the final produced hexa number is reversed.

def int_to_hex_char(n):
    if 0 <= n <= 9:
        return chr(ord('0') + n)
    elif 10 <= n <= 15:
        return chr(ord('a') + (n - 10))
    else:
        return '?'

def to_hex(num):
    if num == 0:
        return '0'
    hex_digits = []
    while num > 0:
        remainder = num % 16
        hex_digits.append(int_to_hex_char(remainder))
        num = num // 16
    hex_digits.reverse()
    return ''.join(hex_digits)

def hash_password(s):
    result = []
    for ch in s:
        ascii_val = ord(ch)          
        multiplied = ascii_val * 16  
        hex_str = to_hex(multiplied) 
        result.append(hex_str)
    return ''.join(result)	



def get_html(page_name):
    templates_folder = "templates"
    file_path = templates_folder + "/" + page_name + ".html" 
    html_file=open(file_path)
    content=html_file.read()
    html_file.close()
    return content
