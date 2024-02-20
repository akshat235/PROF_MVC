from flask import jsonify, request, Blueprint
from models import Submission, Question  



submissions_bp = Blueprint("submissions", __name__)

# @submissions_bp.route('/submit-response', methods=['POST'])
# def submit_response():
#     data = request.json
#     user_id = data.get('userID')
#     responses = data.get('responses')
#     if user_id is None or responses is None:
#         return jsonify({'error': 'userID or responses not provided in the request body'}), 400
#     try:
#         section_scores = {}
#         total_score = 0
#         for response in responses:
#             question_id = response.get('questionID')
#             selected_option = response.get('selectedOption')
#             question = Question.objects(questionId=question_id).first()
#             if question:
#                 correct_answer = question.correctAnswer
#                 if selected_option == correct_answer:
#                     total_score += 1  
#                     section_id = question.sectionId  
#                     section_scores[section_id] = section_scores.get(section_id, 0) + 1
#         submission = Submission(userID=user_id, responses=responses, sectionScores=section_scores, totalScore=total_score)
#         submission.save()
#         return jsonify({'message': 'Response submitted successfully'}), 201
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


@submissions_bp.route('/submit-response', methods=['POST'])
def submit_response():
    data = request.json
    user_id = data.get('userID')
    responses = data.get('responses')
    if user_id is None or responses is None:
        return jsonify({'error': 'userID or responses not provided in the request body'}), 400
    try:
        section_scores = {}
        total_score = 0
        for response in responses:
            question_id = response.get('questionID')
            selected_option = response.get('selectedOption')
            question = Question.objects(questionId=question_id).first()
            if question:
                correct_answer = question.correctAnswer
                if selected_option == correct_answer:
                    total_score += 1  
                    section_id = question.sectionId  
                    section_scores[section_id] = section_scores.get(section_id, 0) + 1
        submission = Submission(userID=user_id, responses=responses, sectionScores=section_scores, totalScore=total_score)
        submission.save()
        submission_data = {
            'userID': user_id,
            'responses': responses,
            'sectionScores': section_scores,
            'totalScore': total_score
        }
        return jsonify({'message': 'Response submitted successfully', 'submission': submission_data}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
