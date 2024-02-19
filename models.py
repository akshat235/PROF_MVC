from mongoengine import Document, StringField, SequenceField

class User(Document):
    userID = SequenceField(primary_key=True)
    email = StringField(required=True)
    password = StringField(required=True)
    role = StringField(required=True)
    
    meta = {'collection': 'prof_mvc_users'} 
