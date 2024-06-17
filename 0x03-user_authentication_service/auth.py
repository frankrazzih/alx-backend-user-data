#!/usr/bin/env python3
'''encrypt a password'''

from db import DB
import bcrypt
from db import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4

def _hash_password(password: str)->bytes:
    '''hashes a password'''
    pwd_bytes = password.encode('UTF-8')
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_pwd

def _generate_uuid(self)->str:
    '''creates a uuid'''
    return str(uuid4())

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        '''Initializes a new Auth instance'''
        self._db = DB()

    def register_user(self, email: str, password: str)->User:
        '''save a new user to the db'''
        try:
            exists = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            user = self._db.add_user(email, hashed_pwd)
            return user
        if exists:
            raise ValueError(f'User {email} already exists')
    
    def valid_login(self, email: str, password: str)->bool:
        '''check if a users password is correct'''
        try:
            user = self._db.find_user_by(email=email)
            user_pwd = user.hashed_password
            pwd_bytes = password.encode('UTF-8')
            return bcrypt.checkpw(pwd_bytes, user_pwd)
        except:
            return False
        
    def create_session(self, email: str)->str:
        '''creates a session for the user with the email'''
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()
            self._db.commit()
            return user.session_id
        except:
            return None
    