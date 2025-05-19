import json

# Load JSON data from a file.
def load_json_file(filepath):
    file = open(filepath, "r")
    data = json.load(file)
    file.close()
    return data
   
# Saves JSON data from a file.
def save_json_file(filepath, data):
    file = open(filepath, "w")
    json.dump(data, file, indent=2)
    file.close()

# Shashing a password by simply turning it into ASCII values and the reverse it.
def hash_password(password):
    ascii_values = []  

    for char in password:
        ascii_code = ord(char)      
        ascii_str = str(ascii_code) 
        ascii_values.append(ascii_str)  

    hashed_password = ''.join(ascii_values) 
    reversed_hashed_password = ''

    for char in hashed_password:
        reversed_hashed_password = char + reversed_hashed_password
    return reversed_hashed_password


# Generate HTML for a quiz form based on the user type. By default the user is a guest and there are no existing answers.
def generate_quiz_form_html(lines, form_action, is_trial=True, username=None,existing_answers=None):
    if existing_answers is None:
        existing_answers = {}
    html = []

    if is_trial:
        html.append('<div id="trial-quiz-form">')
        html.append('<h1>Trial Quiz</h1>')
    else:
        html.append('<div id="quiz-form">')
        html.append('<h1>Quiz</h1>')
    
    html.append(f'<form id="edit-quiz-form" action="{form_action}" method="POST">')

    valid_lines = [line for line in lines if len(line.split(";")) >= 2]
    total_questions = len(valid_lines)
    
    question_number = 1  
    
    for line in valid_lines:
        parts = line.split(";")
        question = parts[0].strip()
        options = parts[1:]
        
        html.append(f'<p>{question}</p>')
        
        for opt in options:
            opt_clean = opt.split(":")[0].split(",")[0].strip()
            display_text = opt_clean.capitalize()
            
            checked_attr = ''
            saved_answer = existing_answers.get(f'q{question_number}')
            if saved_answer and saved_answer == opt_clean:
                checked_attr = ' checked'
            print(f"Question {question_number}, saved answer: {saved_answer}, option: {opt_clean}")
            html.append(
    f'<label><input type="radio" name="q{question_number}" value="{opt_clean}"{checked_attr} required /> {display_text}</label><br />'
)

        
        
        if question_number < total_questions:
            html.append('<hr />')
        
        question_number += 1
    
    html.append('<div id="submit-trial-quiz">')
    html.append('<button type="submit" id="submit-quiz-btn">Submit</button>')
    

    if is_trial:
        html.append('<a href="/" id="cancel"> Cancel </a>')
    else:
        if username:
            cancel_href = f"/petsona/profile/{username}"
        else:
            cancel_href = "/petsona/profile"
        html.append(f'<a href="{cancel_href}" id="go-back-profile-btn">Cancel</a>')
    
    html.append('</div>')  
    html.append('</form>')
    html.append('</div>')  
   
    return "\n".join(html)



def get_html(page_name):
    templates_folder = "templates"
    file_path = templates_folder + "/" + page_name + ".html" 
    html_file=open(file_path,'r',encoding='utf-8')
    content=html_file.read()
    html_file.close()
    return content