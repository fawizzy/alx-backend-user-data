#!/usr/bin/env python3
'''
authorization module
'''
import bcrypt
from user import User
from db import DB, NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    '''
    encrypt password
    '''
    salt = bcrypt.gensalt()
    password = password.encode('utf-8')
    return bcrypt.hashpw(password, salt)


def _generate_uuid() -> str:
    """
    generate unique id
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        method to register new user
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
        check if credentials are valid
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        if bcrypt.checkpw(password.encode("utf-8"), user.hashed_password):
            return True
        return False

    def create_session(self, email: str) -> str:
        "create session id after loging in"
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return user.session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        get user profile from session id
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy session id
        """
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None

        session_id = None
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_reset_password_token(self, email: str) -> str:
        """
        get passord reset token
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return user.reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        update user password after getting reset token
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError()
        hashed = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed, reset_token=None)
