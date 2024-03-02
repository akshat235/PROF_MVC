from mongoengine import Document, StringField, SequenceField, ListField, IntField, DictField

class User(Document):
    userID = SequenceField()
    email = StringField(required=True)
    password = StringField(required=True)
    role = StringField(required=True)
    classID = StringField()
    
    meta = {'collection': 'prof_mvc_users'}

class Question(Document):
    questionId = IntField(primary_key=True)
    questionBody = StringField(required=True)
    options = ListField(StringField(), required=True)
    correctAnswer = StringField(required=True)
    difficulty = StringField()
    tags = StringField()
    
    meta = {'collection': 'Questions'}


class Submission(Document):
    userID = StringField(required=True)
    responses = ListField(DictField(), required=True)
    totalScore = IntField()
    difficultyScores = DictField()
    submissionDate = StringField()
    submissionTime = StringField()
    
    meta = {'collection': 'TestSubmissions'}

