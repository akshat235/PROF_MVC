import requests

# BASE_URL = 'http://127.0.0.1:5000/auth'

# def register(email, password, role):
#     url = f'{BASE_URL}/register'
#     data = {'email': email, 'password': password, 'role': role}
#     response = requests.post(url, json=data)
#     if response:
#         print(response.json())


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


# register('test1@gmail.com', 'password123', 'Student')
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


# import requests
# import json

# BASE_URL = 'http://127.0.0.1:5000/submissions/submit-response'

# def submit_response(user_id, responses):
#     data = {'userID': user_id, 'responses': responses}
#     response = requests.post(BASE_URL, json=data)
#     if response.status_code == 201:
#         print("Response submitted successfully")
#         submission_data = response.json().get('submission')
#         print("Submission details:")
#         print(json.dumps(submission_data, indent=4))
#     else:
#         print("Error:", response.json())
# user_id = "654321"
# responses = [
#     {"questionID": 1, "selectedOption": "Mg + O2 → MgO", "difficulty": "Easy"},
#     {"questionID": 2, "selectedOption": "11", "difficulty": "Medium"},
#     {"questionID": 18, "selectedOption": "11", "difficulty": "Hard"},
#     {"questionID": 10, "selectedOption": "J.K. Rowling", "difficulty": "Easy"}
# ]
# submit_response(user_id, responses)



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




import requests

def test_tot_progress():
    url = 'http://localhost:5000/submissions/tot_progress'
    user_id = '654321'
    response = requests.get(url, params={'user_id': user_id})
    assert response.status_code == 200
    assert 'Total scores retrieved successfully' in response.json()['message']
    # assert 'total_scores' in response.json()
    print(response.json())
    print("Test passed: tot_progress endpoint works as expected.")

test_tot_progress()


