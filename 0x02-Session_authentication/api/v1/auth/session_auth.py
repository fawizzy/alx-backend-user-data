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

        sessionID = uuid4()
        self.user_id_by_session_id[sessionID] = user_id
        return sessionID
