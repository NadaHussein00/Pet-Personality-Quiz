from flask import Flask, request, redirect, url_for,jsonify,session, make_response
from urllib.parse import urlencode
import datetime
import html
import json
from app.utils.helpers import get_html,load_json_file,save_json_file,hash_password,generate_quiz_form_html
from app.models.trial_quiz_class import TrialQuiz
from app.models.registered_user_quiz_class import RegisteredUserQuiz
from app.utils.validate_signup_form import validate_name,validate_email,validate_username,validate_password
from app.utils.validate_login_form import validate_login_fields,validate_user_exists,validate_password_login




app=Flask("routes")
app.secret_key = "secret-key"

users_json_file="data/json/users_data.json"
quizzes_json_file="data/json/quizzes.json"
trial_quiz_ques_file="data/text/trial_quiz_questions.txt"
quiz_ques_file="data/text/quiz_questions.txt"
pet_descriptions_file="data/text/pet_description.txt"

trial_quiz = TrialQuiz(trial_quiz_ques_file,pet_descriptions_file)
quiz=RegisteredUserQuiz(users_json_file,quizzes_json_file,quiz_ques_file,pet_descriptions_file)




# Home page route: redirects to user profile if logged in, otherwise shows landing page
@app.route("/")
def homepage():
    if "username" in session:
        return redirect(url_for("get_user_profile", username=session["username"]))
    return get_html("index")


# Signup page: handles user registration via GET and POST methods
@app.route("/petsona/signup", methods=["GET", "POST"])
def signupPage():
    if request.method == "POST":
        signup_form = request.form 
        errors = {}

        firstname = signup_form.get('firstname', '').strip()
        lastname = signup_form.get('lastname', '').strip()
        gender = signup_form.get('gender', '').strip()
        email = signup_form.get('email', '').strip()
        username = signup_form.get('username', '').strip()
        password = signup_form.get('password', '').strip()
        confirm_password = signup_form.get('password-confirm', '').strip()
        bio = signup_form.get('bio', '').strip() 

        users = load_json_file(users_json_file)


        first_name_error = validate_name(firstname, "First name")
        last_name_error = validate_name(lastname, "Last name")
        email_error = validate_email(email)
        username_error = validate_username(username)
        password_error = validate_password(password)
        confirm_password_error = ""
        bio_error = ""

        if bio:
            word_count = len(bio.split())
            if word_count > 100:
                bio_error = "Bio must be less than 100 words."

        if password != confirm_password:
            confirm_password_error = "Passwords do not match."

        if first_name_error:
            errors["firstname"] = first_name_error  
        if last_name_error:
            errors["lastname"] = last_name_error   
        if email_error:
            errors["email"] = email_error
        if username_error:
            errors["username"] = username_error
        if password_error: 
            errors["password"] = password_error
        if confirm_password_error:
            errors["password-confirm"] = confirm_password_error    
        if bio_error:
            errors["bio"] = bio_error               

        
        if not errors:
            for user in users:
                if user['username'].lower() == username.lower():
                    errors["username"] = "Username already exists."
                if user['email'].lower() == email.lower():
                    errors["email"] = "Email already exists."

        if errors:
            signup_html = get_html("signup_page")
            signup_html = signup_html.replace("$$ERROR_EMAIL$$", errors.get("email", ""))
            signup_html = signup_html.replace("$$ERROR_USERNAME$$", errors.get("username", ""))
            signup_html = signup_html.replace("$$FIRSTNAME$$", firstname)
            signup_html = signup_html.replace("$$LASTNAME$$", lastname)
            signup_html = signup_html.replace("$$EMAIL$$", email)
            signup_html = signup_html.replace("$$USERNAME$$", username)
            signup_html = signup_html.replace("$$BIO$$", bio)
            return signup_html

        
        users.append({
            "username": username,
            "email": email,
            "first_name": firstname,
            "last_name": lastname,
            "gender":gender,
            "password": hash_password(password),
            "bio":bio,
            "registered_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "quiz_history": []
        })
        save_json_file(users_json_file,users)
        return redirect(url_for('login', registered=1))

    
    signup_html = get_html("signup_page")
    signup_html = signup_html.replace("$$ERROR_EMAIL$$", "")
    signup_html = signup_html.replace("$$ERROR_USERNAME$$", "")
    signup_html = signup_html.replace("$$FIRSTNAME$$", "")
    signup_html = signup_html.replace("$$LASTNAME$$", "")
    signup_html = signup_html.replace("$$EMAIL$$", "")
    signup_html = signup_html.replace("$$USERNAME$$", "")
    signup_html = signup_html.replace("$$BIO$$", "")
    return signup_html



# Login page route: handles user login via GET and POST methods
@app.route("/petsona/login", methods=["GET", "POST"])
def login():
    email_error = ""
    password_error = ""
    if request.method == "POST":
        login_form = request.form 
        email = login_form.get('email', '').strip()
        password = login_form.get('password', '').strip()
        users = load_json_file(users_json_file)
        
        field_errors = validate_login_fields(email, password)
        email_error = field_errors.get("email", "")
        password_error = field_errors.get("password", "")

        
        if not field_errors:
            user, user_error = validate_user_exists(email, users)
            if user_error:
                email_error = user_error
            else:
                pw_error = validate_password_login(user, password)
                if pw_error:
                    password_error = pw_error
                else:
                    username = user['username']
                    session["username"] = username
                    return redirect(url_for('get_user_profile', username=username))

        html = get_html("login_form")
        html = html.replace("$$ERROR_EMAIL$$", email_error)
        html = html.replace("$$ERROR_PASS$$", password_error)
        html = html.replace("$$EMAIL$$", email)
        html = html.replace("$$PASSWORD$$", password)
        return html

    
    html = get_html("login_form")
    html = html.replace("$$ERROR_EMAIL$$", "")
    html = html.replace("$$ERROR_PASS$$", "")
    html = html.replace("$$EMAIL$$", "")
    html = html.replace("$$PASSWORD$$", "")
    return html


# Quiz page route: serves quiz form and handles quiz submissions for registered and guest users
@app.route("/petsona/quiz", methods=["GET", "POST"])
def quiz_page():
    username = request.args.get("username", None)  

    is_registered = bool(username)

    if is_registered:
        quiz_questions_file = quiz_ques_file
        quiz_title = "Quiz"
        form_action = f"/petsona/quiz?username={username}"
    else:
        quiz_questions_file = trial_quiz_ques_file
        quiz_title = "Trial Quiz"
        form_action = "/petsona/quiz"  

    with open(quiz_questions_file, "r", encoding="utf-8") as f:
        lines = f.read().strip().splitlines()

    if request.method == "POST":
        answers = {}
        question_number = 1
        for line in lines:
            q_key = f'q{question_number}'
            answers[q_key] = request.form.get(q_key)
            question_number += 1
        
        if is_registered:
            scores = quiz.calculate_scores(answers)
            submitted_at = datetime.datetime.utcnow().isoformat() + 'Z'
            quiz.save_result(username, answers, scores, submitted_at)
            quiz.save_quiz_answers(username, answers, submitted_at)
            return redirect(url_for('quiz_result', username=username))
        else:
            scores = trial_quiz.calculate_scores(answers)
            final_result = trial_quiz.get_final_result(scores, answers)
            encoded_result = urlencode(final_result)
            return redirect(url_for('quiz_result') + '?' + encoded_result + '&username=guest')

    quiz_form_html = generate_quiz_form_html(lines, form_action, is_trial=not is_registered, username=username)

    html_content = get_html("generic_quiz")
    html_content = html_content.replace("$$QUIZ_TITLE$$", quiz_title)
    html_content = html_content.replace("$$QUIZ_FORM$$", quiz_form_html)

    return html_content




# Quiz result page route: displays the result of the most recent or trial quiz
@app.route("/petsona/quiz_result")
def quiz_result():
    username = request.args.get('username', None) 

    first_name = "Guest"
    is_guest = True
    user = None

    if username:
        users = load_json_file(users_json_file)
        for u in users:
            if u['username'].lower() == username.lower():
                user = u
                first_name = user.get('first_name', 'Guest')
                is_guest = False
                break

    if user is None:
        dominant_trait = request.args.get('dominant_trait', 'Unknown')
        description = request.args.get('description', '')
        pet_type = request.args.get('pet_type', 'Unknown')
    else:
        quiz_history = user.get("quiz_history", [])
        if not quiz_history:
            return "No quiz results found", 404

        latest_quiz = quiz_history[-1]
        dominant_trait = latest_quiz.get("dominant_trait", "Unknown")
        description = latest_quiz.get("description", "")
        pet_type = latest_quiz.get("pet_type", "Unknown")


    safe_first_name = html.escape(first_name)
    pet_type_safe = html.escape(pet_type)
    dominant_trait_safe = html.escape(dominant_trait)

    if is_guest:
        button_html = '''
        <a href="/petsona/signup">
          <button id="sign-up-btn" class="nav-btn">Sign Up Now!</button>
        </a>
        '''
        safe_username = ""
    else:
        button_html = f'''
        <a href="/petsona/profile/{username}">
          <button id="profile-btn" class="nav-btn">Go Back to Profile</button>
        </a>
        '''
        safe_username = username

    html_content = get_html("quiz_result_page")
    html_content = html_content.replace('$$PET_TYPE$$', pet_type_safe)
    html_content = html_content.replace('$$DOMINANT_TRAIT$$', dominant_trait_safe)
    html_content = html_content.replace('$$DESCRIPTION$$', description)
    html_content = html_content.replace('$$FIRSTNAME$$', safe_first_name)
    html_content = html_content.replace('$$USERNAME$$', safe_username)
    html_content = html_content.replace('$$BUTTON$$', button_html)

    return html_content


# User profile page route: displays the profile and quiz history for a user
@app.route("/petsona/profile/<username>")
def get_user_profile(username):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if session['username'].lower() != username.lower():
        return redirect(url_for('login'))
    users = load_json_file(users_json_file)

    user = None
    first_name=None
    
    
    for u in users:
        if u['username'].lower() == username.lower():
            user = u
            first_name=user["first_name"]
            break
    bio_text = user.get('bio')
    if bio_text is None:
        bio_text = ""    

    if user is None:
        return "User not found", 404

    quiz_history = user.get('quiz_history', [])

    html_content = get_html('user_profile')

    safe_username = html.escape(username)
    quiz_history_json = html.escape(json.dumps(quiz_history))

    html_content = html_content.replace('$$USERNAME$$', safe_username)
    html_content = html_content.replace('$$BIO$$', bio_text)
    html_content = html_content.replace('$$QUIZ_HISTORY_JSON$$', quiz_history_json)
    html_content = html_content.replace('$$FIRSTNAME$$', first_name)

    response = make_response(html_content)
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


# Quiz history page route: shows all previous quizzes for the user
@app.route("/petsona/quiz_history")
def quiz_history():
    username = request.args.get("username")
    if not username:
        return "Username is required", 400  

    users = load_json_file(users_json_file)
    user = None

    for u in users:
        if u['username'].lower() == username.lower():
            user = u
            break

    if not user:
        return "User not found", 404

    quiz_history = user.get("quiz_history", [])

    html_content = get_html("show_previous_quizzes")

    quiz_history_json = html.escape(json.dumps(quiz_history))
    first_name = user.get("first_name", "Guest")

    html_content = html_content.replace("$$FIRSTNAME$$", html.escape(first_name))
    html_content = html_content.replace("$$USERNAME$$", html.escape(username))
    html_content = html_content.replace("$$QUIZ_HISTORY_JSON$$", quiz_history_json)

    return html_content
    

# Edit profile page route: serves and updates user profile info via GET and PATCH methods
@app.route("/petsona/edit_profile",methods=["GET","PATCH"])
def edit_profile():
    username=request.args.get("username")
    users = load_json_file(users_json_file)
    user = None
    for u in users:
        if u['username'].lower() == username.lower():
            user = u
            break
    if not user:
        return jsonify({"error": "User not found"}), 404

    if request.method == 'GET':
        accept = request.headers.get('Accept', '')
        if 'application/json' in accept:
            profile_data = {
                "first_name": user.get("first_name", ""),
                "last_name": user.get("last_name", ""),
                "password": user.get("password", ""),
                "bio-edit": user.get("bio", "")
            }
            return jsonify(profile_data)
        else:
            html_content = get_html('edit_profile_page')  
            html_content = html_content.replace("$$USERNAME$$", html.escape(username))
            return html_content 

    if request.method == 'PATCH':
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        key_map = {
        "first-name": "first_name",
        "last-name": "last_name",
        "bio-edit": "bio",
        "password": "password"
        }
        
        for frontend_key, user_key in key_map.items():
            if frontend_key in data:
                if frontend_key == "password":
                    hashed_password = hash_password(data["password"])
                    user["password"] = hashed_password
                else:
                    user[user_key] = data[frontend_key]

        save_json_file(users_json_file, users)
        return jsonify({"message": "Profile updated successfully"})
    


# Edit quiz page route: serves and updates a specific quiz entry via GET and PATCH methods
@app.route('/petsona/edit_quiz', methods=['GET', 'PATCH'])
def edit_quiz():
    print("edit_quiz route called, method:", request.method)

    username = request.args.get('username')
    submitted_at = request.args.get('submitted_at')

    if not username or not submitted_at:
        return jsonify({"error": "Missing username or submitted_at query parameter"}), 400

    quizzes = load_json_file(quizzes_json_file)

    try:
        norm_submitted_at = datetime.datetime.fromisoformat(submitted_at.replace('Z', '+00:00')).replace(microsecond=0)
    except Exception:
        return jsonify({"error": "Invalid submitted_at format"}), 400

    quiz_entry = None
    for q in quizzes:
        q_username = q.get('username', '').lower()
        q_submitted_at_str = q.get('submitted_at', '')

        try:
            q_submitted_at = datetime.datetime.fromisoformat(q_submitted_at_str.replace('Z', '+00:00')).replace(microsecond=0)
        except Exception:
            continue

        if q_username == username.lower() and q_submitted_at == norm_submitted_at:
            quiz_entry = q
            break

    if not quiz_entry:
        return jsonify({"error": "Quiz not found"}), 404

    if request.method == 'GET':
        print("Accept header:", request.headers.get('Accept'))
        answers = quiz_entry.get('answers', {})
        accept_header = request.headers.get('Accept', '')
        if 'application/json' in accept_header:
            print("Returning JSON answers:", answers) 
            return jsonify({"answers": answers})

        html_content = get_html("generic_quiz")

        html_content = html_content.replace("$$USERNAME$$", html.escape(username))
        html_content = html_content.replace("$$QUIZ_TITLE$$", "Quiz")


        quiz_questions_file = quiz_ques_file 
        with open(quiz_questions_file, "r", encoding="utf-8") as file:
            file_lines = file.read().strip().splitlines()

        form_action = f"/petsona/edit_quiz?username={username}&submitted_at={submitted_at}"

        quiz_form_html = generate_quiz_form_html(
            file_lines,
            form_action,
            is_trial=False,
            username=username,
            existing_answers=answers 
        )

        html_content = html_content.replace("$$QUIZ_FORM$$", quiz_form_html)

        response = make_response(html_content)
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response

    elif request.method == 'PATCH':
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        quiz_entry['answers'].update(data)
        quiz.update_quiz_answers(username, submitted_at, data)

        return jsonify({"message": "Quiz updated successfully","redirect_url": url_for('quiz_result', username=username)})



# Delete quiz route: deletes a specific quiz history via DELETE method
@app.route("/petsona/delete_quiz",methods=["DELETE"])
def delete_quiz():
    username = request.args.get('username')
    quiz_id = request.args.get('quiz_id')

    if not username:
        return jsonify({"error": "Username required"}), 400
    if not quiz_id:
        return jsonify({"error": "Quiz ID required"}), 400


    users = load_json_file(users_json_file)
    user = None
    for u in users:
        if u['username'].lower() == username.lower():
            user = u
            break
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    quiz_history = user.get("quiz_history", [])
    original_len = len(quiz_history)
    new_quiz_history = []

    for quiz in quiz_history:
        if quiz.get("submitted_at") != quiz_id:
            new_quiz_history.append(quiz)

    if len(new_quiz_history) == original_len:
        return jsonify({"error": "Quiz not found"}), 404        


    user["quiz_history"] = new_quiz_history

    save_json_file(users_json_file,users)

    return jsonify({"message": "Quiz deleted successfully."}), 200

	
# logout route: logs out the user and cleans the session
@app.route("/petsona/logout")
def logout():
    session.clear()  
    return redirect(url_for("login"))
