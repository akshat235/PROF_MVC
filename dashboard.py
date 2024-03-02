from flask import jsonify, request, Blueprint
from models import Submission, User
from datetime import datetime


dashboard_bp = Blueprint("dashboard", __name__,)

@dashboard_bp.route('/highest-scores', methods=['GET'])
def highest_scores():
    classID = request.args.get('classID')
    if not classID:
        return jsonify({'error': 'classID is required'}), 400

    users = User.objects(classID=classID)
    user_ids = [user.userID for user in users]
    submissions = Submission.objects(userID__in=user_ids)
    highest_scores = {}
    for submission in submissions:
        student_id = submission.userID
        if student_id not in highest_scores:
            highest_scores[student_id] = submission.totalScore
        else:
            highest_scores[student_id] = max(highest_scores[student_id], submission.totalScore)
    highest_scores_list = [(student_id, score) for student_id, score in highest_scores.items()]

    return jsonify(highest_scores_list), 200