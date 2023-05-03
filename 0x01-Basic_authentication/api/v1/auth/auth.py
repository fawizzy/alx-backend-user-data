
'''
Auth module
'''
from flask import request
from typing import TypeVar, List


class Auth():
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''
            Return false
        '''
        if path is None:
            return True
        if excluded_paths is None:
            return True
        
        if path in excluded_paths:
            return False
        
        for excluded_path in excluded_paths:
            if path.startswith(excluded_path):
                if path == excluded_path:
                    return False
            if excluded_path.startswith(path):
                return False
        return True
    

    def authorization_header(self, request=None) -> str: 
        '''
        Return None
        '''
        return None
    

    def current_user(self, request=None) -> TypeVar('User'):
        '''
            Aunthentication logic is here
            Retutn - 
                None if user is not auntheticated
        '''
        return None