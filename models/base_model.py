#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from sqlalchemy import Column, Integer, String, DateTime
from sqlachemy.ext.declarative import delclarative_base
from datetime import datetime


Base = declarative_Base()

class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            if kwargs:
                kwargs['updated_at'] = datetime.strptime(
                        kwargs['updated_at'],'%Y-%m-%dT%H:%M:%S.%f')
                kwargs['created_at'] = datetime.strptime(
                        kwargs['created_at'],'%Y-%m-%dT%H:%M:%S.%f')
                for key, value in kwargs.items():
                    if key != "__class__":
                        if key in ['updated_at', 'created_at']:
                            value = datetime.strptime(
                                    value, '%Y-%m-%dT%H:%M:%S.%f')
                        setattr(self, key, value)

                if "id" not in kwargs:
                    self.id = str(uuid.uuid4())
                elif "created_at" not in kwargs:
                    self.created_at = datetime.now()
                elif "updated_at" not in kwargs:
                    self.updated_at = datetime.now()

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary

    def delete(self):
        """ Delete current instance from storage """
        models.storage.delete(self)
