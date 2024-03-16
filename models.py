from mongoengine import Document, StringField, SequenceField, ListField, IntField, DictField

class User(Document):
    userID = SequenceField()
    email = StringField(required=True)
    password = StringField(required=True)
    role = StringField(required=True)
    classID = StringField()
    
    def to_json(self):
        return {
            'userID': self.userID,
            'email': self.email,
            'role': self.role,
            'classID': self.classID
        }
    
    
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
    userID = IntField(required=True)
    responses = ListField(DictField(), required=True)
    totalScore = IntField()
    difficultyScores = DictField()
    submissionDate = StringField()
    submissionTime = StringField()
    
    meta = {'collection': 'TestSubmissions'}

class Scores(Document):

    user_id = IntField(required=True)
    section_scores = DictField(DictField())

    meta = {'collection': 'user_scores'}




