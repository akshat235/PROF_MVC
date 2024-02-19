from flask import Blueprint, jsonify
import json

questions_bp = Blueprint("questions", __name__)

@questions_bp.route('/get-questions', methods=['GET'])
def get_questions():
    try:
        with open('Data.json', 'r') as f:
            questions = json.load(f)
        return jsonify(questions), 200
    except FileNotFoundError:
        return jsonify({'error': 'Data file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500 
