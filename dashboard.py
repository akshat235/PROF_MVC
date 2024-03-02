from flask import jsonify, request, Blueprint
from models import Submission, User
from datetime import datetime
import os


dashboard_bp = Blueprint("dashboard", __name__,)


@dashboard_bp.route('/highest-average-scores', methods=['GET'])
def highest_scores():
    classID = request.args.get('classID')
    if not classID:
        return jsonify({'error': 'classID is required'}), 400
    users = User.objects(classID=classID)
    user_ids = [user.userID for user in users]
    submissions = Submission.objects(userID__in=user_ids)
    highest_scores = {}
    total_score = 0
    for submission in submissions:
        student_id = submission.userID
        if student_id not in highest_scores:
            highest_scores[student_id] = submission.totalScore
        else:
            highest_scores[student_id] = max(highest_scores[student_id], submission.totalScore)
        total_score += submission.totalScore
    average_score = total_score / len(submissions) if submissions else 0
    return jsonify({
        'highest_scores': highest_scores,
        'average_score': average_score
    }), 200


@dashboard_bp.route('/add-email', methods=['POST'])
def update_email():
    data = request.json
    email = data.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    file_path = os.path.join(os.path.dirname(__file__), 'studentEmails.txt')
    with open(file_path, 'r') as file:
        emails = file.readlines()
        if email.strip() + '\n' in emails:
            return jsonify({'message': 'Email already exists'}), 200
    with open(file_path, 'a') as file:
        file.write(email + '\n')
    return jsonify({'message': 'Email added successfully'}), 201


@dashboard_bp.route('/remove-email', methods=['POST'])
def remove_email():
    data = request.json
    email = data.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    file_path = os.path.join(os.path.dirname(__file__), 'studentEmails.txt')
    with open(file_path, 'r') as file:
        emails = file.readlines()
    if email.strip() + '\n' not in emails:
        return jsonify({'message': 'Email not found'}), 404
    emails.remove(email.strip() + '\n')
    with open(file_path, 'w') as file:
        file.writelines(emails)
    return jsonify({'message': 'Email removed successfully'}), 200
