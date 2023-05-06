#!/usr/bin/env python3
'''
Session auth views
'''
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session():
    """
    Handle user login
    Return:
        dictionary representation of user if found else error message
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password"}), 400
    users = User.search({"email": email})
    if users is None or users == []:
        return jsonify({"error": "no user found for this email"})
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            user_json = jsonify(user.to_json())
            sessionName = getenv("SESSION_NAME")
            user_json.set_cookie(sessionName, session_id)
            return user_json
    return jsonify({"error": "wrong password"}), 401
