import random
from pymongo import MongoClient
import pandas as pd


class rec:

    def __init__(self, user_id) -> None:
        
        self.user_id = user_id
        self.threshold_easy = 25
        self.threshold_medium = 25
        self.penalty = 1
        self.sections = ['section1','section2','section3']
        db_name = 'sd'#change this
        self.mongo_client = MongoClient() # add URL here
        self.db = self.mongo_client[db_name]#add db name here


    def get_prev(self):

        # prev_responses = self.db.user_responses.find_one({'user_id': self.user_id})
        # if prev_responses:
        #     # List to store question information with section
        #     questions_with_section = []
        #     # Iterate through previous responses
        #     for question_id, response in prev_responses.items():
        #         # Query MongoDB to get section for the question_id
        #         question_details = self.db.questions.find_one({'QID': question_id})
        #         if question_details:
        #             # Include question_id, response, and section in the result
        #             questions_with_section.append({'question_id': question_id, 'response': response, 'section': question_details['section']})
        #     return questions_with_section
        # else:
        #     return []

        response = [
                {'question_id': '1', 'response': 'correct', 'section': 'section1'},
                {'question_id': '2', 'response': 'wrong', 'section': 'section2'},
                {'question_id': '3', 'response': 'wrong', 'section': 'section3'},
                {'question_id': '4', 'response': 'correct', 'section': 'section1'},
                {'question_id': '5', 'response': 'wrong', 'section': 'section2'},
                {'question_id': '6', 'response': 'correct', 'section': 'section3'},
                {'question_id': '7', 'response': 'wrong', 'section': 'section1'},
                {'question_id': '8', 'response': 'wrong', 'section': 'section2'},
                {'question_id': '9', 'response': 'correct', 'section': 'section3'},
                {'question_id': '10', 'response': 'correct', 'section': 'section3'}
        ]
        return response

    def get_user_score(self):

        # user_scores = self.db.user_scores.find_one({'user_id': self.user_id})
        # if user_scores:
        #     return user_scores
        # else:
        #     # Initialize user scores if not present
        #     user_scores = {section: {'easy': 0, 'medium': 0, 'difficult': 0} for section in self.sections}
        #     self.db.user_scores.insert_one({'user_id': self.user_id, 'scores': user_scores})
        #     return user_scores

        user_scores = {section: {'easy': 0, 'medium': 25, 'difficult': 25} for section in self.sections}

        return user_scores

    #should be called 1st    
    def get_questions(self): #gets recommendations for each section

        selected_question_ids_by_section = {}
        for section in self.sections: 
            selected_question_ids_by_section[section] = self.get_selection_question_ids(section)
        return selected_question_ids_by_section
    
    #2
    def get_selection_question_ids(self,section): #gives the recommendation for each section

        
        responses = self.get_prev()
        wrong_responses_section = [entry['question_id'] for entry in responses if entry['section'] == section and entry['response'] == 'wrong']
        wrong_question_ids = wrong_responses_section # [doc['questionID'] for doc in wrong_responses_section]
        total_questions = 4
        rem = total_questions - len(wrong_question_ids)

        #choosing correct reponses
        correct_responses = [entry['question_id'] for entry in responses if entry['section'] == section and entry['response'] == 'correct']
        corr_ids = correct_responses#[doc['questionID'] for doc in correct_responses]
        corr_num = min(rem//2, len(corr_ids))
        selected_correct_question_ids = random.sample(corr_ids,corr_num)

        repeat_qid = wrong_question_ids + selected_correct_question_ids

        rem = total_questions - len(repeat_qid)

        rec_qid = self.rec_questions(rem,section)

        final_questions = repeat_qid + rec_qid        

        return final_questions
    
    #3
    def rec_questions(self,rem,section):

        self.user_scores = self.get_user_score()

        easy_score = self.user_scores[section]['easy']
        medium_score = self.user_scores[section]['medium']
        

        recommended_questions = []

        if easy_score < self.threshold_easy:
            # Recommend easy questions
            recommended_questions.extend(self.get_questions_by_difficulty(section, 'easy', rem))
        elif easy_score < self.threshold_medium and easy_score >= self.treshold_easy:
            # Recommend mix of easy and medium questions
            easy_count = min(rem // 2, len(self.get_questions_by_difficulty(section, 'easy')))
            medium_count = rem - easy_count
            recommended_questions.extend(self.get_questions_by_difficulty(section, 'easy', easy_count))
            recommended_questions.extend(self.get_questions_by_difficulty(section, 'medium', medium_count))
        elif medium_score < self.threshold_medium:
            # Recommend mix of medium and difficult questions
            medium_count = min(rem // 2, len(self.get_questions_by_difficulty(section, 'medium')))
            difficult_count = rem - medium_count
            recommended_questions.extend(self.get_questions_by_difficulty(section, 'medium', medium_count))
            recommended_questions.extend(self.get_questions_by_difficulty(section, 'difficult', difficult_count))
        else:
            # Recommend difficult questions
            recommended_questions.extend(self.get_questions_by_difficulty(section, 'difficult', rem))

        return recommended_questions
    
    #4
    def get_questions_by_difficulty(self, section, difficulty, count):
        # Retrieve questions from MongoDB
        # questions = self.db.questions.find({'section': section, 'difficulty': difficulty})

        questions =  [
            {'QID': 1, 'section': 'section1', 'difficulty': 'easy'},
            {'QID': 2, 'section': 'section2', 'difficulty': 'easy'},
            {'QID': 3, 'section': 'section3', 'difficulty': 'easy'},
            {'QID': 4, 'section': 'section1', 'difficulty': 'medium'},
            {'QID': 5, 'section': 'section2', 'difficulty': 'medium'},
            {'QID': 6, 'section': 'section3', 'difficulty': 'medium'},
            {'QID': 7, 'section': 'section1', 'difficulty': 'difficult'},
            {'QID': 8, 'section': 'section2', 'difficulty': 'difficult'},
            {'QID': 9, 'section': 'section3', 'difficulty': 'difficult'},
            {'QID': 10, 'section': 'section3', 'difficulty': 'medium'},
            {'QID': 11, 'section': 'section3', 'difficulty': 'medium'},
            {'QID': 12, 'section': 'section3', 'difficulty': 'medium'},
            {'QID': 13, 'section': 'section3', 'difficulty': 'difficult'},
            {'QID': 14, 'section': 'section3', 'difficulty': 'easy'},
            {'QID': 15, 'section': 'section3', 'difficulty': 'difficult'},
            {'QID': 16, 'section': 'section3', 'difficulty': 'easy'},
            {'QID': 17, 'section': 'section3', 'difficulty': 'medium'},
            {'QID': 18, 'section': 'section3', 'difficulty': 'difficult'},
            {'QID': 19, 'section': 'section3', 'difficulty': 'difficult'},
            {'QID': 20, 'section': 'section3', 'difficulty': 'medium'},
            {'QID': 21, 'section': 'section3', 'difficulty': 'easy'},
            {'QID': 22, 'section': 'section3', 'difficulty': 'medium'},
            {'QID': 23, 'section': 'section3', 'difficulty': 'difficult'},
            {'QID': 24, 'section': 'section3', 'difficulty': 'medium'},
            {'QID': 25, 'section': 'section3', 'difficulty': 'easy'}            

        ]
        return random.sample([question['QID'] for question in questions], min(count, len(questions)))
    
    #works independently 
    # 1st call after submission
    def update_user_scores(self):
        # Update user scores based on responses
        responses = [] # this needs to come from service handler
        for question_id, response in responses.items():
            section = self.master_questions[question_id]['section']
            difficulty = self.master_questions[question_id]['difficulty']
            if response == 'correct':
                self.user_scores[section][difficulty] += 1
            else:
                # Penalize for wrong response
                self.user_scores[section][difficulty] -= self.penalty
                # Ensure scores don't go negative
                self.user_scores[section][difficulty] = max(0, self.user_scores[section][difficulty])

        #need to update self.user_scores in the DB
                

    







