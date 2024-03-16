import random
from pymongo import MongoClient
import pandas as pd
from models import Submission,Question
from pymongo.server_api import ServerApi
import pymongo



class rec:

    def __init__(self, user_id) -> None:
        
        self.user_id = user_id
        self.threshold_easy = 25
        self.threshold_medium = 25
        self.sections = ['Section A','Section B']
        self.penalty = 1
        url = 'mongodb+srv://akshat:DOVvBNo0e6m2iH6X@doggo.yxoygou.mongodb.net/'
        db_name = 'PROF_MVC'#change this
        self.mongo_client = MongoClient(url,server_api=ServerApi('1')) # add URL here
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
            question_ids = [(resp['questionID']) for resp in submission['responses']]

        tags_lookup = {}
        for question_id in question_ids:

            question = self.db['Questions'].find_one({'questionId':question_id},{'tags': 1})

            if question :

                tags_lookup[question_id] = question.get('tags',[])
            else:
                tags_lookup[question_id] = []

        responses = []

        for resp in submission['responses']:

            question_id = resp['questionID']
            answer_status = resp.get('answer_status',None)
            section = tags_lookup.get(question_id,[])
            responses.append({'questionID':question_id,'answer_status':answer_status, 'tags':section})
        
        return responses

    def get_user_score(self):

        user_scores = self.db.user_scores.find_one({'user_id': self.user_id},{'section_scores':1})
        user_scores = user_scores['section_scores']
        if user_scores:
            return user_scores
        else:
            # Initialize user scores if not present
            user_scores = {section: {'easy': 0, 'medium': 0, 'difficult': 0} for section in self.sections}
            self.db.user_scores.insert_one({'user_id': self.user_id, 'section_scores': user_scores})
            return user_scores

    #should be called 1st    
    def get_questions(self): #gets recommendations for each section

        selected_question_ids_by_section = []
        for section in ['Section A', 'Section B']: #add sections
            selected_question_ids_by_section.append(self.get_selection_question_ids(section))
        return selected_question_ids_by_section
    
    #2
    def get_selection_question_ids(self,section): #gives the recommendation for each section

        temp = []
        section_df =self.get_prev()
        final_data = [entry for entry in section_df if section in entry['tags']] 
        wrong_responses_section = [doc for doc in final_data if doc['answer_status'] == 'wrong']
        wrong_question_ids = [doc['questionID'] for doc in wrong_responses_section]

        total_questions = 10
        rem = total_questions - len(wrong_question_ids)

        # Choosing correct responses
        correct_responses = [doc for doc in final_data if doc['answer_status'] == 'correct']
        corr_ids = [doc['questionID'] for doc in correct_responses]
        corr_num = min(rem // 2, len(corr_ids))
        selected_correct_question_ids = random.sample(corr_ids, corr_num)

        repeat_qid = wrong_question_ids + selected_correct_question_ids

        rem = total_questions - len(repeat_qid)

        rec_qid = self.rec_questions(rem, section)  # Assuming rec_questions is a method that returns recommended questions for the section

        final_questions = repeat_qid + rec_qid

        return final_questions
    
    #3
    def rec_questions(self,rem,section):

        self.user_scores = self.get_user_score()

        u_scores = self.user_scores["section_scores"]
        section_score = u_scores.get(section,{})

              

        easy_score = section_score.get("easy",None)
        medium_score = section_score.get("medium",None)
        

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
        questions = self.db.Questions.find({'tags': section, 'difficulty': difficulty})
        # min_count = self.db.Questions.find({'tags': section, 'difficulty': difficulty}).count()
        return random.sample([question['questionId'] for question in questions], min(count, len(list(questions))))
    
    #works independently 
    # 1st call after submission
    def update_user_scores(self,responses): 
        # Update user scores based on responses
        self.master_questions = self.db.Questions.find()
        print(responses)
        self.user_scores = self.get_user_score()
        for response in responses:

            question_id = response['question_id']
            response = response['answer_status']
            section = self.master_questions[question_id]['tags']
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
                {'$set': {'section_scores': self.user_scores}},
                upsert=True  
            )
    







