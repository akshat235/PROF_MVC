from flask import jsonify, request, Blueprint
from models import Submission, Question  
from datetime import datetime




submissions_bp = Blueprint("submissions", __name__)


# @submissions_bp.route('/submit-response', methods=['POST'])
# def submit_response():
#     data = request.json
#     user_id = data.get('userID')
#     responses = data.get('responses')
#     if user_id is None or responses is None:
#         return jsonify({'error': 'userID or responses not provided in the request body'}), 400
#     try:
#         total_score = 0
#         difficulty_scores = {'Easy': 0, 'Medium': 0, 'Hard': 0}
#         # Fetch all questions first
#         all_questions = Question.objects.all()
#         for response in responses:
#             question_id = int(response.get('questionID'))
#             selected_option = response.get('selectedOption')
#             tags = response.get('tags')
#             question = next((q for q in all_questions if q.questionId == question_id), None)
#             if question:
#                 correct_answer = question.correctAnswer
#                 if selected_option == correct_answer:
#                     total_score += 1
#                     difficulty_scores[question.difficulty] += 1
#         current_date = datetime.now().strftime('%Y-%m-%d')
#         current_time = datetime.now().strftime('%H:%M:%S')
#         submission = Submission(userID=user_id, 
#                                 responses=responses,
#                                 totalScore=total_score,
#                                 difficultyScores=difficulty_scores,
#                                 submissionDate=current_date,
#                                 submissionTime=current_time)
#         submission.save()
#         return jsonify({'message': 'Response submitted successfully'}), 201
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

@submissions_bp.route('/submit-response', methods=['POST'])
def submit_response():
    data = request.json
    user_id = data.get('userID')
    responses = data.get('responses') # 
    if user_id is None or responses is None:
        return jsonify({'error': 'userID or responses not provided in the request body'}), 400
    try:
        total_score = 0
        difficulty_scores = {'Easy': 0, 'Medium': 0, 'Hard': 0} #remove this
        # Fetch all questions first
        all_questions = Question.objects.all()
        for response in responses:
            question_id = int(response.get('questionID'))
            selected_option = response.get('selectedOption')
            tags = response.get('tags')
            question = next((q for q in all_questions if q.questionId == question_id), None)
            if question:
                correct_answer = question.correctAnswer
                if selected_option == correct_answer:
                    total_score += 1
                    difficulty_scores[question.difficulty] += 1 #remove this
                    response['answer_status'] = 'correct'
                else:
                    response['answer_status'] = 'wrong'
        current_date = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime('%H:%M:%S')
        submission = Submission(userID=user_id, 
                                responses=responses,
                                totalScore=total_score,
                                difficultyScores=difficulty_scores, #remove this
                                submissionDate=current_date,
                                submissionTime=current_time)
        submission.save()

        # my_rec = rec(user_id)
        # my_rec.update_user_scores(responses)
        return jsonify({'message': 'Response submitted successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
@submissions_bp.route('/get-submissions-by-userID', methods=['GET'])
def get_submissions():
    user_id = request.args.get('user_id')
    if user_id is None:
        return jsonify({'error': 'user_id not provided in the request'}), 400
    try:
        submissions = Submission.objects(userID=user_id)
        test_scores = [{'totalScore': submission.totalScore, 'difficultyScores': submission.difficultyScores} for submission in submissions]
        return jsonify({'message': 'Submissions retrieved successfully', 'test_scores': test_scores}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
@submissions_bp.route('/tot_progress', methods=['GET'])
def tot_progress():
    user_id = request.args.get('user_id')
    if user_id is None:
        return jsonify({'error': 'user_id not provided in the request'}), 400
    try:
        submissions = Submission.objects(userID=user_id).order_by('-submissionDate', '-submissionTime')
        response_object = [{'totalScore': submission.totalScore, 'date': submission.submissionDate, 'time': submission.submissionTime, 'difficultyScores': submission.difficultyScores} for submission in submissions]
        return jsonify({'message': 'Total scores retrieved successfully', 'response': response_object}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@submissions_bp.route('/last-submission', methods=['GET'])
def last_submission():
    user_id = request.args.get('user_id')
    if user_id is None:
        return jsonify({'error': 'user_id not provided in the request'}), 400
    try:
        submission = Submission.objects(userID=user_id).order_by('-submissionDate', '-submissionTime').first()
        if submission:
            response_object = {
                'totalScore': submission.totalScore,
                'date': submission.submissionDate,
                'time': submission.submissionTime,
                'difficultyScores': submission.difficultyScores
            }
            return jsonify({'message': 'Last submission retrieved successfully', 'response': response_object}), 200
        else:
            return jsonify({'error': 'No submissions found for the user'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500