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

def _generate_uuid()->str:
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
            if user is None:
                return None
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except:
            return None
        
    def get_user_from_session_id(self, session_id: str)->User:
        '''gets a user based on their session id'''
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except:
            return None   

    def destroy_session(self, user_id: int):
        '''destroys a users session_id'''
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str)->str:
        '''generates a password reset token'''
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except:
            raise ValueError
        
    def update_password(self, reset_token: str, password: str):
        '''updates a users password'''
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_pwd = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed_pwd, reset_token=None)
        except:
            raise ValueError

    