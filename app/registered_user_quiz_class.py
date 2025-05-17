from datetime import datetime
from app.quiz_class import Quiz
from app.helpers import load_json_file,save_json_file

class RegisteredUserQuiz(Quiz):
    num_questions = 12  # Registered quiz loads 11 questions

    def __init__(self, users_file,quizzes_file ,questions_file,descriptions_file):
        super().__init__()
        self.users_file = users_file
        self.quizzes_file=quizzes_file
        self.load_questions(questions_file)
        self.load_descriptions(descriptions_file)

    def save_quiz_answers(self, username, answers,submitted_at):
        quizzes = load_json_file(self.quizzes_file)

        quiz_entry = {
            "username": username,
            "submitted_at": submitted_at,
            "answers": answers,
            "is_modified": False,
            "modified_at": None
        }

        quizzes.append(quiz_entry)
        save_json_file(self.quizzes_file,quizzes)

        return submitted_at  # return timestamp for reference


    def calculate_scores(self, answers):
        trait_scores = {}
        for question in self.questions:
            qid = question["id"]
            selected_option = answers.get(qid)
            if not selected_option:
                continue

            # Match selected_option text exactly (case-sensitive)
            traits = question["options"].get(selected_option, {})
            
            if traits is None:
                continue

            for trait, weight in traits.items():
                trait_scores[trait] = trait_scores.get(trait, 0) + weight

 

        return trait_scores

    def get_final_result(self, trait_scores,answers,submitted_at):
        if not trait_scores:
            return "No traits detected."

        top_trait = max(trait_scores, key=trait_scores.get)
        description = self.get_description(top_trait)
        pet_type = answers.get("q1")
        gender_desc = ""
        if answers:
            gender_answer = answers.get("q2")  # or correct key
            if gender_answer:
                gender_trait_map = {
                "female": ["nurturing", "attentive"],
                "male": ["protective", "loyal"]}
            # Build gender traits description independently of scores
                gender_traits = gender_trait_map.get(gender_answer.lower(), [])
            # Remove gender traits if they are already the dominant trait to avoid repetition
                gender_traits = [t for t in gender_traits if t != top_trait]

                if gender_traits:
                    gender_desc = "\n\nAdditional gender-related traits:\n"
                    for trait in gender_traits:
                        desc = self.get_description(trait)
                        if desc:
                            gender_desc += f"- {trait.capitalize()}: {desc}\n"

        full_description = f"{description}{gender_desc}"
        return {
        "pet_type": pet_type.capitalize() if pet_type else "",
        "dominant_trait": top_trait.capitalize(),
        "description": full_description,
        "submitted_at": submitted_at,
        "is_modified":False,
        "modified_at":None
    }

    def save_result(self, username, answers, trait_scores,submitted_at):

        users=load_json_file(self.users_file)

        # Find user
        user = None
        for u in users:
            if u['username'].lower() == username.lower():
                user = u
                break
        if not user:
            raise ValueError("User not found")

        quiz_entry = self.get_final_result(trait_scores, answers,submitted_at)

        # Append to quiz_history
        if "quiz_history" not in user:
            user["quiz_history"] = []

    # Append quiz entry to quiz_history
        user["quiz_history"].append(quiz_entry)

    # Save back to file
        save_json_file(self.users_file,users)

        return True
		

    def update_quiz_answers(self, username, submitted_at, updated_answers):
        quizzes = load_json_file(self.quizzes_file) 
        quiz = None
        for q in quizzes:
            if q.get('username') == username and q.get('submitted_at') == submitted_at:
                quiz = q
                break
        if not quiz:
            raise ValueError("Quiz not found")

        quiz['answers'].update(updated_answers)
        quiz['is_modified'] = True
        quiz['modified_at'] = datetime.utcnow().isoformat() + 'Z'
        # Now update user's quiz history in users.json
        trait_scores = self.calculate_scores(quiz['answers'])
        new_final_result = self.get_final_result(trait_scores, quiz['answers'], submitted_at)

    # 3. Update user's quiz history with new final result
        users = load_json_file(self.users_file)
        user = None
        # Find user with nested loop instead of next()
        for u in users:
            if u['username'].lower() == username.lower():
                user = u
                break
        if not user:
            raise ValueError("User not found")

        if 'quiz_history' not in user:
            user['quiz_history'] = []

    # 4. Find quiz entry in quiz_history by submitted_at
        user_quiz_entry = None
        for entry in user['quiz_history']:
            if entry.get('submitted_at') == submitted_at:
                user_quiz_entry = entry
                break

        if user_quiz_entry:
            user_quiz_entry.update(new_final_result)
            user_quiz_entry['is_modified'] = quiz.get('is_modified')
            user_quiz_entry['modified_at'] = quiz.get('modified_at')
        else:
            new_final_result['is_modified'] = quiz.get('is_modified', False)
            new_final_result['modified_at'] = quiz.get('modified_at')
            user['quiz_history'].append(new_final_result)
        
        print("Existing entry:", user_quiz_entry)
        print("New final result:", new_final_result)
    # 6. Save updated users file
        save_json_file(self.users_file, users)
