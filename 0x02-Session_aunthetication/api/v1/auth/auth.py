#!/usr/bin/env python3
'''
Auth module
'''
from flask import request
from typing import TypeVar, List


class Auth():
    '''
    class to manage API authentication
    '''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''
        Check if a path requires authentication based on excluded paths.

        Args:
            path (str): The path to check for authentication requirement.
            excluded_paths (List[str]):
                A list of paths that are excluded from authentication.

        Returns:
            bool: True if the path requires authentication, False otherwise.
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
        Get the authorization header from a Flask request.

        Args:
            request: A Flask request object.

        Returns:
            str:
                The value of the authorization header,
                or None if it doesn't exist.
        '''
        if request is None:
            return None
        if request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        Authenticate the current user based on a Flask request.

        Args:
            request: A Flask request object.

        Returns:
            TypeVar('User'):
             The authenticated user, or None if authentication fails.
        '''
        return None
