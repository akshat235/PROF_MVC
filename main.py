from flask import Flask, session
# from flask_sqlalchemy import SQLAlchemy
from auth import auth_bp
from questions import questions_bp
from submission import submissions_bp
from dashboard import dashboard_bp
from flask_cors import CORS, cross_origin
from mongoengine import connect
import mongoengine


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

app.config['SESSION_TYPE'] = 'filesystem'   
app.config['SESSION_PERMANENT'] = False

app.config['MONGODB_SETTINGS'] = {
    'db': 'PROF_MVC',  
    'host': 'mongodb+srv://akshat:DOVvBNo0e6m2iH6X@doggo.yxoygou.mongodb.net/'
}

connect(alias='default', host=app.config['MONGODB_SETTINGS']['host'], db=app.config['MONGODB_SETTINGS']['db'])

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(questions_bp, url_prefix='/questions')
app.register_blueprint(submissions_bp, url_prefix='/submissions')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
 
if __name__ == '__main__':
   app.run()