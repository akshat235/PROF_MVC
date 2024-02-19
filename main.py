from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from auth import auth_bp
from questions import questions_bp
# from test_handler import test_bp
# from dashboard import dashboard_bp
from flask_cors import CORS, cross_origin
# from models import db, Question
from mongoengine import connect
import mongoengine
import sqlalchemy_cockroachdb


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


 
if __name__ == '__main__':
   app.run(debug=True)
