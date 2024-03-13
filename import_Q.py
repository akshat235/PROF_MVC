import pandas as pd
from models import Question  # Import your Question model from models.py
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Read the CSV file into a DataFrame
csv_file = "D:\sequio\shaar_git\Shaar_questions - Sheet1.csv"
df = pd.read_csv(csv_file)

for index, row in df.iterrows():
    # Extract values from the row
    question_id = row['questionID']
    question_body = row['questionBody']
    options = [row['Option 1'], row['Option 2'], row['Option 3'], row['Option 4']]
    correct_answer = row['Correct answer']
    difficulty = row['Difficulty']
    tags = row['L1 tag']
    
    # Create a new Question object and save it to the MongoDB collection
    question = Question(
        questionId=question_id,
        questionBody=question_body,
        options=options,
        correctAnswer=correct_answer,
        difficulty=difficulty,
        tags=tags
    )
    question.save()