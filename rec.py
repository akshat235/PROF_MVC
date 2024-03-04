import random
import pymongo

class Rec:
    def __init__(self, user_id):
        self.user_id = user_id
        
        self.db_client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.db_client['your_database_name']
        self.collection = self.db['your_collection_name']


    def get_user_scores_from_db(self):
        # Query the database to retrieve user scores based on user_id
        # Example implementation:

        self.collection = self.db['your_collection_name'] #change this
        user_scores = {
            'Section A': {'easy': 0, 'medium': 0, 'difficult': 0},
            'Section B': {'easy': 0, 'medium': 0, 'difficult': 0}
        }
        return user_scores

    def update_user_scores_in_db(self):
       
       self.collection = self.db['your_collection_name'] #change this
       for section, scores in self.user_scores.items():
            for difficulty, score in scores.items():
                # Example query to update user scores in MongoDB
                # Replace 'your_collection_name' with the actual collection name
                self.collection.update_one(
                    {'user_id': self.user_id, 'section': section, 'difficulty': difficulty},
                    {'$set': {'score': score}},
                    upsert=True  
                )

    def select_questions(self, section, rem, temp):
        # Calculate the weights based on user's performance scores
        weights = [max(0, self.user_scores[section][difficulty]) for difficulty in ['easy', 'medium', 'difficult']]
        total_weight = sum(weights)
        normalized_weights = [weight / total_weight if total_weight > 0 else 1/3 for weight in weights]

        selected_questions = []
        for _ in range(rem):
            difficulty = random.choices(['easy', 'medium', 'difficult'], weights=normalized_weights)[0]
            eligible_questions = self.collection.find({'section': section, 'difficulty': difficulty, 'questionID': {'$nin': temp}})
            if eligible_questions.count() > 0:
                question_id = random.choice([doc['questionID'] for doc in eligible_questions])
                selected_questions.append(question_id)
                temp.append(question_id)
        return selected_questions

    def process_responses(self, section, responses):
        for response in responses:
            _, row = response
            self.update_scores(section, row['difficulty'], row['response'])

    def get_previous_responses_from_db(self):

        self.collection = self.db['your_collection_name'] #change this
        # Query the database to retrieve previous responses based on user_id
        # Example implementation:
        previous_responses = self.collection.find({'user_id': self.user_id})
        return previous_responses

    def get_selected_question_ids(self, section):
        temp = []
        section_df = self.get_previous_responses_from_db().filter({'section': section})
        wrong_responses_section = section_df.filter({'response': 'wrong'})
        wrong_question_ids = [doc['questionID'] for doc in wrong_responses_section]
        total_questions = 10
        rem = total_questions - len(wrong_question_ids)
        selected_correct_question_ids = self.select_questions(section, rem, temp)
        return wrong_question_ids + selected_correct_question_ids

    def get_selected_question_ids_by_section(self):
        selected_question_ids_by_section = {}
        for section in ['Section A', 'Section B']: 
            selected_question_ids_by_section[section] = self.get_selected_question_ids(section)
        return selected_question_ids_by_section

    def close_db_connection(self):
        self.db_client.close()


# Example usage:
# rec_system = Rec(user_id='your_user_id')
# selected_question_ids = rec_system.get_selected_question_ids_by_section()
# rec_system.close_db_connection()