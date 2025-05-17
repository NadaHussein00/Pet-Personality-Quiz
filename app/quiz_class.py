class Quiz:
    num_questions = None  # To be defined in subclasses

    def __init__(self):
        self.questions = []
        self.descriptions = {}


    def load_questions(self, filename):
        questions_file = open(f"data/text/{filename}", 'r', encoding='utf-8')
        lines = questions_file.readlines()
        questions_file.close()


        question_number = 1
        for line in lines:
            if self.num_questions and question_number > self.num_questions:
                break

            line = line.strip()
            if not line:
                continue

            parts = [p for p in line.split(';') if p.strip()]

            if len(parts) < 2:
                continue

            question_text = parts[0]
            options_raw = parts[1:]
            options = {}

            for opt in options_raw:
                opt = opt.strip()
                if ':' in opt:
                    key, traits_part = opt.split(':', 1)
                    traits = {}
                    for trait_entry in traits_part.split(','):
                        trait_entry = trait_entry.strip()
                        if '=' in trait_entry:
                            trait, weight_str = trait_entry.split('=', 1)
                            try:
                                weight = int(weight_str)
                            except ValueError:
                                weight = 1
                            traits[trait.strip()] = weight
                        else:
                            traits[trait_entry.strip()] = 1
                    options[key.strip()] = traits
                else:
                    options[opt.strip()] = {}

            self.questions.append({
                "id": f"q{question_number}",
                "text": question_text,
                "options": options
            })
            question_number += 1

    def get_questions(self):
        return self.questions
    
    def load_descriptions(self,filename):
        descriptions = {}
        descriptions_file = open(f"data/text/{filename}", 'r', encoding='utf-8')  
        for line in descriptions_file:
            line = line.strip()
            if not line or '=' not in line:
                continue 
            trait, desc = line.split('=', 1)
            descriptions[trait.strip()] = desc.strip()
        descriptions_file.close()  
        self.descriptions = descriptions
        return descriptions
    

    def get_description(self, trait):
        return self.descriptions.get(trait)
