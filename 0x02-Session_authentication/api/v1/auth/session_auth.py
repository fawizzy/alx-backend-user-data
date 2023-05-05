#!/usr/bin/env python3
'''
Session auth modul
'''
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    '''
    class for session authorization
    '''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''
        create session id
        '''
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None

        sessionID = str(uuid4())
        self.user_id_by_session_id[sessionID] = user_id
        return sessionID

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''
        return user based on a session ID
        '''
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None

        user_id = self.user_id_by_session_id.get(session_id)
        return user_id