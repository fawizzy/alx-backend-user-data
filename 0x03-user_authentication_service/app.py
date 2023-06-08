#!/usr/bin/env pyhton3
"""
Flask app
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'])
def index() -> str:
    """
    index api
    """
    payload = {"message": "Bienvenue"}
    return jsonify(payload)


@app.route("/users", methods=['POST'])
def users() -> str:
    """
    Register new users
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        payload = {"email": f"{email}", "message": "user created"}
        return jsonify(payload)
    except ValueError:
        payload = {"message": "email already registered"}
        return jsonify(payload), 400


@app.route("/sessions", methods=['POST'])
def login():
    """
    log in users with valid credentials
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email=email)
        payload = jsonify({"email": f"{email}", "message": "logged in"})
        payload.set_cookie("session_id", session_id)
        return payload
    else:
        abort(401)


@app.route("/sessions", methods=['DELETE'])
def logout():
    """
    logout of a session
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user.session_id:
        AUTH.destroy_session(user.id)
        return redirect("/")
    else:
        abort(403)


@app.route("/profile", methods=['GET'])
def profile():
    """
    Return user email based on session id
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user.session_id:
        payload = {"email": f"{user.email}"}
        return jsonify(payload), 200
    else:
        abort(403)


@app.route("/reset_password", methods=['POST'])
def reset_password():
    """
    reset user password after generating
    reset password token
    """
    email = request.form.get('email')
    reset_token = AUTH.get_reset_password_token(email)
    if reset_token:
        payload = {"email": f"{email}", "reset_token": f"{reset_token}"}
        return jsonify(payload), 200
    else:
        abort(403)


@app.route("/reset_password", methods=['PUT'])
def update_password():
    """
    reset user password
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        payload = {"email": f"{email}", "message": "Password updated"}
        return jsonify(payload), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
