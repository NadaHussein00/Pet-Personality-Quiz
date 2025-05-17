from app.quiz_class import Quiz

class TrialQuiz(Quiz):
    num_questions = 6  # For example, trial quiz loads 6 questions

    def __init__(self, questions_file,descriptions_file):
        super().__init__()
        self.load_questions(questions_file)
        self.load_descriptions(descriptions_file)

    def calculate_scores(self, answers):
        trait_scores = {}
        for question in self.questions:
            qid = question["id"]
            if qid == "q1":  # Skip pet kind question for scoring
                continue

            selected_option = answers.get(qid)
            if not selected_option:
                continue

            traits = question["options"].get(selected_option, {})
            for trait, weight in traits.items():
                trait_scores[trait] = trait_scores.get(trait, 0) + weight

        return trait_scores

    def get_final_result(self, trait_scores,answers):
        if not trait_scores:
            return "No traits detected."

        top_trait = max(trait_scores, key=trait_scores.get)
        description = self.get_description(top_trait)
        pet_type = answers.get("q1")
        return {
            "dominant_trait": top_trait.capitalize(),
            "description": description,
            "pet_type":pet_type.capitalize()
        }


        description = self.get_description(top_trait)
        #return f"Dominant trait: {top_trait.capitalize()}\n\n{description}"
        #return f"Dominant trait: {top_trait.capitalize()}<br><br>{description}"
        return f"<h3>Dominant trait: {top_trait.capitalize()}</h3><p>{description}</p>"

