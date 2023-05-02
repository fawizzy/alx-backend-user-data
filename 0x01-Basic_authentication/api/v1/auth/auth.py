#!/usr/bin/env python3
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
        return False
    

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