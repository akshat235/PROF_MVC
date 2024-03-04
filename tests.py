import requests

# BASE_URL = 'http://127.0.0.1:5000/auth'

# def register(email, password, role):
#     url = f'{BASE_URL}/register'
#     data = {'email': email, 'password': password, 'role': role, 'classID':"54321"}
#     response = requests.post(url, json=data)
#     if response:
#         print(response.json())

# register('test5@gmail.com', 'password123', 'Student')


# def login(email, password):
#     url = f'{BASE_URL}/login'
#     data = {'email': email, 'password': password}
#     response = requests.post(url, json=data)
#     if response:
#         print(response.json())
        
# def check_email(email):
#     url = f'{BASE_URL}/check_email'
#     data = {'email': email}
#     response = requests.post(url, json=data)
#     if response:
#         print(response.json())


# # login('test@gmail.com', 'password123')
# check_email('test@gmail.com')


# BASE_URL = 'http://127.0.0.1:5000/questions' 

# def get_questions():
#     url = f'{BASE_URL}/get-questions'
#     response = requests.get(url)
#     if response:
#         print(response.json())

# # Testing get_questions
# get_questions()



# import requests
# import json

# BASE_URL = 'http://127.0.0.1:5000/questions/get-question'

# def get_question(qid):
#     data = {'qid': qid}
#     response = requests.post(BASE_URL, json=data)
#     if response.status_code == 200:
#         print("Question found:")
#         print(response.json())
#     elif response.status_code == 404:
#         print("Question not found.")
#     else:
#         print("Error:", response.json())

# # Testing get_question with a sample question ID
# get_question(1)


import requests
import json

BASE_URL = 'http://127.0.0.1:5000/submissions/submit-response'

def submit_response(user_id, responses):
    data = {'userID': user_id, 'responses': responses}
    response = requests.post(BASE_URL, json=data)
    if response.status_code == 201:
        print("Response submitted successfully")
        submission_data = response.json().get('submission')
        print("Submission details:")
        print(json.dumps(submission_data, indent=4))
    else:
        print("Error:", response.json())
user_id = "654321"
responses = [
    {"questionID": 1, "selectedOption": "Mg + O2 → MgO", "difficulty": "Easy"},
    {"questionID": 2, "selectedOption": "11", "difficulty": "Medium"},
    {"questionID": 18, "selectedOption": "11", "difficulty": "Hard"},
    {"questionID": 10, "selectedOption": "J.K. Rowling", "difficulty": "Easy"}
]
submit_response(user_id, responses)



# import requests

# def test_get_submissions_by_userID():
#     url = 'http://localhost:5000/submissions/get-submissions-by-userID'
#     user_id = '654321'
#     response = requests.get(url, params={'user_id': user_id})
#     print(response.json())
    
#     assert response.status_code == 200
#     assert 'Submissions retrieved successfully' in response.json()['message']
#     assert 'test_scores' in response.json()
#     print("Test passed: get-submissions-by-userID endpoint works as expected.")


# # Call the test function
# test_get_submissions_by_userID()




# import requests

# def test_tot_progress():
#     url = 'http://localhost:5000/submissions/tot_progress'
#     user_id = '654321'
#     response = requests.get(url, params={'user_id': user_id})
#     assert response.status_code == 200
#     assert 'Total scores retrieved successfully' in response.json()['message']
#     # assert 'total_scores' in response.json()
#     print(response.json())
#     print("Test passed: tot_progress endpoint works as expected.")

# test_tot_progress()


# import requests

# def test_get_questions_by_ids():
#     url = 'http://localhost:5000/questions/get-questions-by-ids'
#     qids = [3, 4, 9]
#     data = {'qids': qids}
#     response = requests.post(url, json=data)
    
#     # Check if the request was successful
#     assert response.status_code == 200
#     # Check if the response contains the expected number of questions
#     # assert len(response.json()) == len(qids)
#     # Optionally, check if the response contains the expected data structure for each question
#     for question in response.json():
#         assert 'questionId' in question
#         assert 'questionBody' in question
#         assert 'options' in question
#         assert 'difficulty' in question
#     print("Test passed: get-questions-by-ids endpoint works as expected.")
#     print(response.json())


# # Call the test function
# test_get_questions_by_ids()




# import requests

# def test_last_submission():
#     url = 'http://localhost:5000/submissions/last-submission'
#     user_id = '654321'
#     response = requests.get(url, params={'user_id': user_id})
#     assert response.status_code == 200
#     assert 'Last submission retrieved successfully' in response.json()['message']
#     assert 'response' in response.json()
#     print("Test passed: last-submission endpoint works as expected.")
#     print(response.json())

# test_last_submission()
# import requests

# def test_update_classID():
#     url = 'http://127.0.0.1:5000/auth/update-classID'
#     data = {
#         'email': 'test3@gmail.com',
#         'classID': '12345'
#     }
#     response = requests.post(url, json=data)
#     response_data = response.json()
#     print(response.json())
#     print("Test passed: update-classID endpoint works as expected.")
    
# test_update_classID()

# import requests
# import json

# def test_register():
#     url = 'http://127.0.0.1:5000/auth/register'
#     data = {
#         'email': 'test5@gmail.com',
#         'password': 'password123',
#         'role': 'Student'
#     }
#     response = requests.post(url, json=data)
    
#     # Print the response status code and JSON data
#     print("Response Status Code:", response.status_code)
#     print("Response Data:", response.json())

# # Call the test function
# test_register()

# import requests

# def test_highest_scores():
#     url = 'http://127.0.0.1:5000/dashboard/highest-scores'
#     classID = '54321' 
#     response = requests.get(url, params={'classID': classID})
#     if response:
#         # Print the response status code and JSON data
#         print("Response Status Code:", response.status_code)
#         print("Response Data:", response.json())

# # Call the test function
# test_highest_scores()

# import requests

# url = "http://localhost:5000/dashboard/add-email"
# data = {"email": "test9@gmail.com"}

# response = requests.post(url, json=data)

# print(response.status_code)
# print(response.json())

# import requests

# url = "http://localhost:5000/dashboard/remove-email"
# data = {"email": "test7@gmail.com"}

# response = requests.post(url, json=data)

# print(response.status_code)
# print(response.json())




# import requests

# url = "http://localhost:5000/dashboard/highest-average-scores"
# params = {"classID": "12345"}

# response = requests.get(url, params=params)

# print(response.status_code)
# print(response.json())

# import requests

# url = "http://localhost:5000/auth/user-details"
# # params = {"userID": 8} # Assuming userID 8 exists in your database
# # params = {"email": "test2@gmail.com"}
# params = {"classID": "54321"}

# response = requests.get(url, params=params)

# print(response.status_code)
# print(response.json())