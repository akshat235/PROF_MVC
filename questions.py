from flask import Blueprint, jsonify, request
import json
from models import Question
from rec import rec

questions_bp = Blueprint("questions", __name__)


@questions_bp.route('/get-questions', methods=['GET'])
def get_questions():

    data = request.json
    user_id = data.get('user_id')
    try:

        my_rec = rec(user_id=user_id)


        question_ids = my_rec.get_questions()
        
        question_details = []
        for question_id in question_ids:
            # Query MongoDB using MongoEngine to get specific fields by question ID
            question_detail = Question.objects(question_id=question_id).only('question_body', 'options', 'difficulty', 'tag').first()
            if question_detail:
                # Extract required fields from the Question document
                question_body = question_detail.question_body
                options = question_detail.options
                difficulty = question_detail.difficulty
                tag = question_detail.tag
                # Append question details to the list
                question_details.append({
                    'question_id': question_id,
                    'question_body': question_body,
                    'options': options,
                    'difficulty': difficulty,
                    'tag': tag
                })

        return jsonify(question_details), 200
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
                # 'correctAnswer': question.correctAnswer,
                'difficulty': question.difficulty,
                'tags': question.tags
            }), 200  
        else:
            return jsonify({'error': 'Question not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@questions_bp.route('/get-questions-by-ids', methods=['POST'])
def get_questions_by_ids():
    data = request.json
    qids = data.get('qids')
    if qids is None or not isinstance(qids, list):
        return jsonify({'error': 'No qids array provided in the request body or qids is not a list'}), 400
    try:
        qids = [int(qid) for qid in qids]
        all_questions = Question.objects()
        questions = [q for q in all_questions if q.questionId in qids]
        
        serialized_questions = []
        for question in questions:
            serialized_question = {
                'questionId': question.questionId,
                'questionBody': question.questionBody,
                'options': question.options,
                'difficulty': question.difficulty,
                'tags': question.tags
            }
            serialized_questions.append(serialized_question)
        
        return jsonify(serialized_questions), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

