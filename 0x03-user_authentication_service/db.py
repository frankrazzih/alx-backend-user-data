#!/usr/bin/env python3
"""DB module.
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the database.
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Finds a user based on a set of filters.
        """
        key = next(iter(kwargs))
        value = kwargs.get(key)
        if hasattr(User, key):
            result = self._session.query(User).filter(getattr(User, key) == value).first()
        else:
            raise InvalidRequestError
        if result is None:
            raise NoResultFound
        return result

    def update_user(self, user_id: int, **kwargs)->None:
        '''updates a user's details'''
        user = self.find_user_by(id=user_id)
        key = next(iter(kwargs))
        try:    
            user.key = kwargs.get(key)
            self._session.commit()
        except:
            raise ValueError
        
    