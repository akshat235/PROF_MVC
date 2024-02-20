from flask import Blueprint, jsonify, request
import json
from models import Question

questions_bp = Blueprint("questions", __name__)


@questions_bp.route('/get-questions', methods=['GET'])
def get_questions():
    try:

        questions = Question.objects.all()
        serialized_questions = []
        for question in questions:
            serialized_question = {
                'questionId': question.questionId,
                'questionBody': question.questionBody,
                'options': question.options,
                'correctAnswer': question.correctAnswer
            }
            serialized_questions.append(serialized_question)

        return jsonify(serialized_questions), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@questions_bp.route('/get-question', methods=['POST'])
def get_question():
    data = request.json
    qid = data.get('qid')
    
    if qid is None:
        return jsonify({'error': 'No qid provided in the request body'}), 400
    
    try:
        qid = int(qid)
    except ValueError:
        return jsonify({'error': 'Invalid qid provided'}), 400
    
    try:
        all_questions = Question.objects()
        question = next((q for q in all_questions if q.questionId == qid), None)
        
        if question:
            return jsonify({
                'questionId': question.questionId,
                'questionBody': question.questionBody,
                'options': question.options,
                'correctAnswer': question.correctAnswer
            }), 200  
        else:
            return jsonify({'error': 'Question not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
