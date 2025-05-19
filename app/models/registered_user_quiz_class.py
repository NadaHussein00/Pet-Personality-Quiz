from datetime import datetime
from app.models.quiz_class import Quiz
from app.utils.helpers import load_json_file,save_json_file


# This class represents the registered user quiz.
# It inherets from the Quiz class.
# It is responsible for saving quiz answers, calculating the scores for each trait, getting and saving the final result, 
# and updating the quiz answers.  

class RegisteredUserQuiz(Quiz):
    num_questions = 12  

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

        return submitted_at  



    def calculate_scores(self, answers):
        trait_scores = {}
        for question in self.questions:
            qid = question["id"]
            selected_option = answers.get(qid)
            if not selected_option:
                continue

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
        emoji = self.trait_emojis.get(top_trait)
        
        gender_desc = ""
        if answers:
            gender_answer = answers.get("q2")  
            if gender_answer:
                gender_trait_map = {
                "female": ["nurturing", "attentive"],
                "male": ["protective", "loyal"]}
                gender_traits = gender_trait_map.get(gender_answer.lower(), [])
                gender_traits = [t for t in gender_traits if t != top_trait]

                if gender_traits:
                    gender_desc = '<h3>Additional gender-related traits:</h3><ul>'
                    for trait in gender_traits:
                        desc = self.get_description(trait)
                        if desc:
                            gender_desc += f'<li><strong>{trait.capitalize()}:</strong> {desc}</li>'
                    gender_desc += '</ul>'
                else:
                    gender_desc = ""

        full_description = f"{description}{gender_desc}"
        return {
        "pet_type": pet_type.capitalize() if pet_type else "",
        "dominant_trait": f"{emoji} {top_trait.capitalize()}",
        "description": full_description,
        "submitted_at": submitted_at,
        "is_modified":False,
        "modified_at":None
    }



    def save_result(self, username, answers, trait_scores,submitted_at):
        users=load_json_file(self.users_file)
        user = None

        for u in users:
            if u['username'].lower() == username.lower():
                user = u
                break
        if not user:
            raise ValueError("User not found")

        quiz_entry = self.get_final_result(trait_scores, answers,submitted_at)
        if "quiz_history" not in user:
            user["quiz_history"] = []
        user["quiz_history"].append(quiz_entry)

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

        save_json_file(self.quizzes_file, quizzes)
        trait_scores = self.calculate_scores(quiz['answers'])
        new_final_result = self.get_final_result(trait_scores, quiz['answers'], submitted_at)

        users = load_json_file(self.users_file)
        user = None

        for u in users:
            if u['username'].lower() == username.lower():
                user = u
                break
        if not user:
            raise ValueError("User not found")

        if 'quiz_history' not in user:
            user['quiz_history'] = []


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
        
        save_json_file(self.users_file, users)