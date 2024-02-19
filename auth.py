from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from models import User
import hashlib
from argon2 import PasswordHasher


auth_bp = Blueprint("auth", __name__, )

ph = PasswordHasher(time_cost=4, parallelism=8, hash_len=64)

def get_allowed_emails():
    allowed_emails = set()
    with open('studentEmails.txt', 'r') as f:
        for line in f:
            email = line.strip()
            if email:  
                allowed_emails.add(email)
    return allowed_emails


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    allowed_emails = get_allowed_emails()
    if email not in allowed_emails:
        return jsonify({'error': 'Email not allowed to register'}), 403
    if User.objects(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400
    hashed_password = ph.hash(password)
    user = User(email=email, password=hashed_password, role=role)
    user.save()
    return jsonify({'message': 'User registered successfully'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user = User.objects(email=email).first()
    if user:
        if ph.verify(user.password, password):
            return jsonify({'message': 'Login successful'})
    return jsonify({'error': 'Invalid email or password'}), 401

@auth_bp.route('/check_email', methods=['POST'])
def check_email():
    data = request.json
    email = data.get('email')
    allowed_emails = get_allowed_emails()
    if email in allowed_emails:
        return jsonify({'message': 'Email exists in allowed emails'}), 200
    else:
        return jsonify({'error': 'User not allowed to register for the class'}), 404