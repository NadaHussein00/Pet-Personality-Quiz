
from flask import Flask, request, redirect, url_for,jsonify,session, make_response
from urllib.parse import quote,unquote
import datetime
import html
import json
from app.helpers import get_html,load_json_file,save_json_file,hash_password
from app.trial_quiz_class import TrialQuiz
from app.registered_user_quiz_class import RegisteredUserQuiz
from app.validate_signup_form import validate_name,validate_email,validate_username,validate_password
from app.validate_login_form import validate_login_fields,validate_user_exists,validate_password_login




app=Flask("routes")
app.secret_key = "secret-key"

users_json_file="data/users_data.json"
quizzes_json_file="data/quizzes.json"

trial_quiz = TrialQuiz('trial_quiz_questions.txt',"pet_description.txt")
quiz=RegisteredUserQuiz(users_json_file,quizzes_json_file,'quiz_questions.txt',"pet_description.txt")




@app.route("/")
def homepage():
    if "username" in session:
        return redirect(url_for("get_user_profile", username=session["username"]))
    return get_html("index")

@app.route("/signup", methods=["GET", "POST"])
def signupPage():
    if request.method == "POST":
        print("POST received at /test-post")
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

        # Validation
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

        # Only check for existing username/email if no other errors
        if not errors:
            for user in users:
                if user['username'].lower() == username.lower():
                    errors["username"] = "Username already exists."
                if user['email'].lower() == email.lower():
                    errors["email"] = "Email already exists."

        if errors:
           print("Returning errors to user")
           signup_html = get_html("signupPage")
           signup_html = signup_html.replace("$$ERROR_EMAIL$$", errors.get("email", ""))
           signup_html = signup_html.replace("$$ERROR_USERNAME$$", errors.get("username", ""))
           signup_html = signup_html.replace("$$ERROR_FIRSTNAME$$", errors.get("firstname", ""))
           signup_html =signup_html.replace("$$ERROR_LASTNAME$$", errors.get("lastname", ""))
           signup_html = signup_html.replace("$$ERROR_BIO$$", errors.get("bio", ""))

           signup_html = signup_html.replace("$$EMAIL$$", email)
           signup_html = signup_html.replace("$$USERNAME$$", username)
           signup_html = signup_html.replace("$$FIRSTNAME$$", firstname)
           signup_html = signup_html.replace("$$LASTNAME$$", lastname)
           signup_html = signup_html.replace("$$BIO$$", bio)

           return signup_html

        # If not found, add new user
        print("No errors, proceeding to append user")
        users.append({
            "username": username,
            "email": email,
            "first_name": firstname,
            "last_name": lastname,
            "gender":gender,
            "password": hash_password(password),
            "bio":bio,
            "registered_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),  # store registration time in UTC
            "quiz_history": []  # list to store past quiz attempts
        })
        save_json_file(users_json_file,users)
        print("Users saved after append")
        #return {"success": True, "message": "Registration successful!"}
        return '<script>window.location.href="/login?registered=1";</script>'
        #return redirect(url_for('login', registered=1))

    # For GET requests, serve the HTML page
    signup_html = get_html("signup_page")
    signup_html = signup_html.replace("$$ERROR_EMAIL$$", "")
    signup_html = signup_html.replace("$$ERROR_USERNAME$$", "")
    signup_html = signup_html.replace("$$ERROR_FIRSTNAME$$", "")
    signup_html = signup_html.replace("$$ERROR_LASTNAME$$", "")
    signup_html = signup_html.replace("$$ERROR_BIO$$", "")

    signup_html = signup_html.replace("$$FIRSTNAME$$", "")
    signup_html = signup_html.replace("$$LASTNAME$$", "")
    signup_html = signup_html.replace("$$EMAIL$$", "")
    signup_html = signup_html.replace("$$USERNAME$$", "")
    signup_html = signup_html.replace("$$BIO$$", "")
    return signup_html


@app.route("/login", methods=["GET", "POST"])
def login():
    email_error = ""
    password_error = ""
    if request.method == "POST":
        login_form = request.form 
        email = login_form.get('email', '').strip()
        password = login_form.get('password', '').strip()
        users = load_json_file("data/users_data.json")

        # 1. Validate empty fields (returns a dict of errors)
        field_errors = validate_login_fields(email, password)
        email_error = field_errors.get("email", "")
        password_error = field_errors.get("password", "")

        # 2. Only continue if no field errors
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

        # Show form with errors if any
        html = get_html("login_form")
        html = html.replace("$$ERROR_EMAIL$$", email_error)
        html = html.replace("$$ERROR_PASS$$", password_error)
        return html

    # GET request: show empty form
    html = get_html("login_form")
    html = html.replace("$$ERROR_EMAIL$$", "")
    html = html.replace("$$ERROR_PASS$$", "")
    return html


@app.route("/trial_quiz",methods=["GET","POST"])
def trial_quiz_page():
    if request.method == 'POST':
        # Collect answers
        answer_q1 = request.form.get('q1')
        answer_q2 = request.form.get('q2')
        answer_q3 = request.form.get('q3')
        answer_q4 = request.form.get('q4')
        answer_q5 = request.form.get('q5')
        answer_q6 = request.form.get('q6')

    # Put them into a dictionary for processing
        answers = {
        'q1': answer_q1,
        'q2': answer_q2,
        'q3': answer_q3,
        'q4': answer_q4,
        'q5': answer_q5,
        'q6': answer_q6
    }

        # Process answers
        scores = trial_quiz.calculate_scores(answers)
        final_result = trial_quiz.get_final_result(scores)

        # Store result in session
        encoded_result = quote(final_result)

        # Redirect to result page with result in URL
        return redirect(url_for('quiz_result', result=encoded_result))

    # For GET requests, serve the static quiz page
    return get_html("trial_quiz_page") #your static quiz HTML loader

@app.route("/quiz_result")
def quiz_result():
    encoded_result = request.args.get('result', 'No result found.')
    print(f"Raw encoded_result from URL: {encoded_result!r}")

    username = request.args.get('username', None)  # Username from URL

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

    if not user:
        # No user found, so no quiz history
        return "No quiz results found", 404

    quiz_history = user.get("quiz_history", [])
    if not quiz_history:
        return "No quiz results found", 404


    # URL-decode the result text
    result = unquote(encoded_result)
    latest_quiz = quiz_history[-1]

    # Extract raw data
    pet_type = latest_quiz.get("pet_type", "Unknown")
    dominant_trait = latest_quiz.get("dominant_trait", "Unknown")
    description = latest_quiz.get("description", "")


    safe_first_name = html.escape(first_name)
    pet_type_safe = html.escape(pet_type)
    dominant_trait_safe = html.escape(dominant_trait)
    description_safe = html.escape(description).replace('\n', '<br>')

    if is_guest:
        button_html = '''
        <a href="/signup">
          <button id="sign-up-btn" class="nav-btn">Sign Up Now!</button>
        </a>
        '''
    else:
        button_html = f'''
        <a href="/profile/{username}">
          <button id="profile-btn" class="nav-btn">Go Back to Profile</button>
        </a>
        '''

    # Load your static HTML template
    html_content = get_html("quiz_result_page")
    # Replace placeholders
    html_content = html_content.replace('$$PET_TYPE$$', pet_type_safe)
    html_content = html_content.replace('$$DOMINANT_TRAIT$$', dominant_trait_safe)
    html_content = html_content.replace('$$DESCRIPTION$$', description_safe)
    """ html_content = html_content.replace('$$RESULT$$', result) """
    html_content = html_content.replace('$$FIRSTNAME$$', safe_first_name)
    html_content = html_content.replace('$$USERNAME$$', username)
    html_content = html_content.replace('$$BUTTON$$', button_html)

    return html_content


@app.route("/profile/<username>")
def get_user_profile(username):
    if 'username' not in session:
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



    #return html_content
    #return get_html("userProfile")
	

@app.route("/quiz",methods=["GET","POST"])    
def quiz_page():
    username = request.args.get("username")  # Get username from URL params

    submitted_at = datetime.datetime.utcnow().isoformat() + 'Z'

    if not username:
        return "Username is required", 400

    if request.method == "POST":
        # Process quiz submission here
        answer_q1 = request.form.get('q1')
        answer_q2 = request.form.get('q2')
        answer_q3 = request.form.get('q3')
        answer_q4 = request.form.get('q4')
        answer_q5 = request.form.get('q5')
        answer_q6 = request.form.get('q6')
        answer_q7 = request.form.get('q7')
        answer_q8 = request.form.get('q8')
        answer_q9 = request.form.get('q9')
        answer_q10 = request.form.get('q10')
        answer_q11 = request.form.get('q11')
        answer_q12 = request.form.get('q12')

    # Put them into a dictionary for processing
        answers = {
        'q1': answer_q1,
        'q2': answer_q2,
        'q3': answer_q3,
        'q4': answer_q4,
        'q5': answer_q5,
        'q6': answer_q6,
        'q7': answer_q7,
        'q8': answer_q8,
        'q9': answer_q9,
        'q10': answer_q10,
        'q11': answer_q11,
        'q12': answer_q12
    }
        scores = quiz.calculate_scores(answers)
        quiz_result_data = quiz.get_final_result(scores, answers,submitted_at)
        quiz.save_result(username, answers, scores,submitted_at)
        quiz.save_quiz_answers(username, answers, submitted_at)

        # Store result in session
        quiz_result_html = quiz.get_final_result(scores, answers,submitted_at)

        # Encode HTML string for URL
        #encoded_result = quote(quiz_result_html)

        # Redirect to result page with result in URL
        #return redirect(url_for('quiz_result', result=encoded_result,username=username))
        return redirect(url_for('quiz_result', username=username))

    # GET request: render quiz page
    html_content = get_html("quiz_page")
    html_content = html_content.replace("$$USERNAME$$", html.escape(username))
    return html_content


   


@app.route("/quiz_history")
def quiz_history():
    # 1. Get the username from the URL, e.g. /quiz_history?username=johndoe
    username = request.args.get("username")
    if not username:
        return "Username is required", 400  # If no username, return error

    # 2. Load all users from your data source (JSON file)
    users = load_json_file(users_json_file)

    # 3. Find the user with the matching username (case-insensitive)
    user = None
    for u in users:
        if u['username'].lower() == username.lower():
            user = u
            break

    if not user:
        return "User not found", 404  # If user not found, return error

    # 4. Get the user's quiz history or empty list if none
    quiz_history = user.get("quiz_history", [])

    # 5. Load the HTML template for showing quiz history
    html_content = get_html("show_previous_quizzes")

    # 6. Convert quiz history to JSON string and escape it for safety

    quiz_history_json = html.escape(json.dumps(quiz_history))

    # 7. Replace placeholders in the HTML template:
    #    - Replace $$USERNAME$$ with the user's first name (or "Guest" if missing)
    #    - Replace $$QUIZ_HISTORY_JSON$$ with the JSON string of quiz history
    first_name = user.get("first_name", "Guest")
    html_content = html_content.replace("$$FIRSTNAME$$", html.escape(first_name))
    html_content = html_content.replace("$$USERNAME$$", html.escape(username))
    html_content = html_content.replace("$$QUIZ_HISTORY_JSON$$", quiz_history_json)

    # 8. Return the final HTML page to the browser
    return html_content
    

@app.route("/edit_profile",methods=["GET","PATCH"])
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
            # Return JSON data for API calls
            profile_data = {
                "first_name": user.get("first_name", ""),
                "last_name": user.get("last_name", ""),
                "password": user.get("password", ""),
                "bio-edit": user.get("bio", "")
            }
            return jsonify(profile_data)
        else:
            # Return HTML page for normal browser requests
            html_content = get_html('edit_profile_page')  # your custom function
            html_content = html_content.replace("$$USERNAME$$", html.escape(username))
            return html_content  # Flask serves as text/html

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

        load_json_file(users_json_file)
        return jsonify({"message": "Profile updated successfully"})
    
@app.route('/edit_quiz', methods=['GET', 'PATCH'])
def edit_quiz():
    username = request.args.get('username')
    submitted_at = request.args.get('submitted_at')

    if not username or not submitted_at:
        return jsonify({"error": "Missing username or submitted_at query parameter"}), 400

    quizzes = load_json_file(quizzes_json_file)

    try:
        norm_submitted_at = datetime.datetime.fromisoformat(submitted_at.replace('Z', '+00:00')).replace(microsecond=0)
    except Exception:
        return jsonify({"error": "Invalid submitted_at format"}), 400

    quiz_enry = None
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
        # Check if client expects JSON (e.g., your frontend fetch)
        accept_header = request.headers.get('Accept', '')
        if 'application/json' in accept_header:
            # Return JSON answers only
            return jsonify({"answers": quiz_entry.get('answers', {})})

        # Otherwise, return the full quiz page HTML with injected answers
        html_content = get_html("quiz_page")  # your quiz HTML template as string

        # Inject username safely
        html_content = html_content.replace("$$USERNAME$$", html.escape(username))

        # Inject answers JSON safely for JS to read and pre-fill form
        answers_json = html.escape(json.dumps(quiz_entry.get('answers', {})))
        html_content = html_content.replace("$$ANSWERS_JSON$$", answers_json)

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

@app.route("/delete_quiz",methods=["DELETE"])
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

# Store the original length of the quiz history
    original_len = len(quiz_history)

# Create a new list excluding the quiz with the matching quiz_id
    new_quiz_history = []
    for quiz in quiz_history:
        if quiz.get("submitted_at") != quiz_id:
            new_quiz_history.append(quiz)

    if len(new_quiz_history) == original_len:
        return jsonify({"error": "Quiz not found"}), 404        

# Assign the filtered list back to user's quiz_history
    user["quiz_history"] = new_quiz_history

    save_json_file(users_json_file,users)

    return jsonify({"message": "Quiz deleted successfully."}), 200

	
	
	
	
@app.route("/logout")
def logout():
    session.clear()  # Clears all data in the session, effectively logging out the user
    return redirect(url_for("login"))