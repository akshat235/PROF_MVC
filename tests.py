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





BASE_URL = 'http://127.0.0.1:5000/questions' 

def get_questions():
    url = f'{BASE_URL}/get-questions'
    response = requests.get(url)
    if response:
        print(response.json())

# Testing get_questions
get_questions()
