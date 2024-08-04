# models/user.py
from models.base_model import BaseModel
import json


class User(BaseModel):
    '''Subclass of BaseModel class'''
    __storage = None


    @classmethod
    def set_storage(cls, storage):
        cls.__storage = storage

    @classmethod
    def get_storage(cls):
        return cls.__storage

    def __init__(self, *args, **kwargs):
        '''Initialize User instance.'''
        # print("Storage inside User __init__:", storage)  # for debugging
        super().__init__(*args, **kwargs)
        self.email = kwargs.get('email', '')
        self.password = kwargs.get('password', '')
        self.first_name = kwargs.get('first_name', '')
        self.last_name = kwargs.get('last_name', '')
