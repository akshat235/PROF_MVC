from pymongo import MongoClient
from pymongo.server_api import ServerApi
from models import Submission,Question
from mongoengine import connect

if __name__ == "__main__":

    # db_name = 'PROF_MVC'#change this
    # uri = 'mongodb+srv://sharad:Sharad1234@doggo.yxoygou.mongodb.net/'
    # mongo_client = MongoClient(uri,server_api=ServerApi('1')) # add URL here
    # db = mongo_client[db_name]

    # # collection = db['TestSubmissions']
    # # # query = {'questionId': 1}
    # # result = collection.find({'userID' : 6})

    # query = {'userID': self.user_id}

    # projection = {'responses': 1, 'submissionDate': 1, 'submissionTime': 1,'_id':0}
    # sort_order = [('submissionDate', pymongo.DESCENDING), ('submissionTime', pymongo.DESCENDING)]
    # submission =  db['your_collection_name'].find_one(query, projection,sort = sort_order)

    connect(alias='default', host='mongodb+srv://akshat:DOVvBNo0e6m2iH6X@doggo.yxoygou.mongodb.net/', db='PROF_MVC')     
    question_id = 10
    question_detail = Question.objects(__raw__ = {'questionId' : 10}).only('questionBody', 'options', 'difficulty', 'tags')

    question_details = []
    if question_detail:
        # Extract required fields from the Question document

        for question in question_detail:
            question_body = question.questionBody
            options = question.options
            difficulty = question.difficulty
            tag = question.tags
            # Append question details to the list
            question_details.append({
                'question_id': question_id,
                'question_body': question_body,
                'options': options,
                'difficulty': difficulty,
                'tag': tag
            })

    print(question_details)


    # print(result)