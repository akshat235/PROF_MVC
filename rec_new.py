import random
from pymongo import MongoClient
import pandas as pd


class rec:

    def __init__(self, user_id) -> None:
        
        self.user_id = user_id
        self.treshold_easy = 25
        self.treshold_medium = 25
        self.penalty = 1
        db_name = 'sd'#change this
        self.mongo_client = MongoClient() # add URL here
        self.db = self.mongo_client[db_name]#add db name here


    def get_prev(self):
        
        #need to fix this. Should retrive the last submission ofr user_id and then associate each qid with tag
        # submission = Submission.objects(userID=self.user_id)
        # submission = self.db['TestSubmissions'].find({'userID':self.user_id})

        query = {'userID': self.user_id}

        projection = {'responses': 1, 'submissionDate': 1, 'submissionTime': 1,'_id':0}
        sort_order = [('submissionDate', pymongo.DESCENDING), ('submissionTime', pymongo.DESCENDING)]
        submission =  self.db['TestSubmissions'].find_one(query, projection,sort = sort_order)

        # submission = Submission.objects()
        if submission:
            response_object = [(resp['questionID'], resp.get('answer_status', None)) for resp in submission['responses']]

        responses = pd.DataFrame(response_object['responses'])

        def fetch_tags(question_id):

            collection = self.db['Questions']
            query = {'questionId': question_id}
            result = collection.find_one(query, {'tags': 1})
            if result:
                return result.get('tags', '')  # Assuming tags is a list field in MongoDB
            else:
                return ''

        responses['section'] = responses['questionID'].apply(fetch_tags)
        
        return responses

    def get_user_score(self):

        user_scores = self.db.user_scores.find_one({'user_id': self.user_id})
        if user_scores:
            return user_scores
        else:
            # Initialize user scores if not present
            user_scores = {section: {'easy': 0, 'medium': 0, 'difficult': 0} for section in self.sections}
            self.db.user_scores.insert_one({'user_id': self.user_id, 'scores': user_scores})
            return user_scores

    #should be called 1st    
    def get_questions(self): #gets recommendations for each section

        selected_question_ids_by_section = {}
        for section in ['Section A', 'Section B']: 
            selected_question_ids_by_section[section] = self.get_selected_question_ids(section)
        return selected_question_ids_by_section
    
    #2
    def get_selection_question_ids(self,section): #gives the recommendation for each section

        temp = []
        section_df = pd.DataFrame(self.get_prev().filter({'section': section}))
        wrong_responses_section = section_df.filter({'response': 'wrong'})
        wrong_question_ids = [doc['questionID'] for doc in wrong_responses_section]
        total_questions = 10
        rem = total_questions - len(wrong_question_ids)

        #choosing correct reponses
        correct_responses = section_df.filter({'response':'correct'})
        corr_ids = [doc['questionID'] for doc in correct_responses]
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
        questions = self.db.questions.find({'section': section, 'difficulty': difficulty})
        return random.sample([question['QID'] for question in questions], min(count, questions.count()))
    
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
            
            # self.db.prev_resp.find_one({'user_id': self.user_id})
            self.db.user_scores.update_one( #may need to change the schema based on the actual implementation in the DB
                {'user_id': self.user_id},
                {'$set': {'user_score': self.user_score}},
                upsert=True  
            )
    







