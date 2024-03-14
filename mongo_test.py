from pymongo import MongoClient
from pymongo.server_api import ServerApi
from models import Submission

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
     
    sections = ['section1','section2','section3']

    user_scores = {section: {'easy': 0, 'medium': 25, 'difficult': 25} for section in sections}

    print(user_scores)


    # print(result)