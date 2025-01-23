from django.db import models
from db_connection import db
from enum import Enum
import bcrypt
from bson import ObjectId


class Role(Enum):
    STORE_MANAGER = 'store_manager'
    SUPPLIER = 'supplier'
    STAFF = 'staff'

class User:
    def __init__(self, username, password, email, role):
        self.username = username
        self.password_hash = self.hash_password(password)
        self.email = email
        self.role = role

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def save(self):
        db.users.insert_one(self.__dict__)

    @staticmethod
    def get_by_username(username):
        return db.users.find_one({'username': username})

    @staticmethod
    def get_by_email(email):
        return db.users.find_one({'email': email})

    @staticmethod
    def get_by_id(user_id):
        return db.users.find_one({'_id': ObjectId(user_id)})

    @staticmethod
    def check_password(stored_password, provided_password):
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)
