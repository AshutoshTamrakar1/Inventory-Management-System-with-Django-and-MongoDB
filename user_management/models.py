from db_connection import db
from enum import Enum
import bcrypt
from bson import ObjectId
import logging

logger = logging.getLogger('user_management')

class Role(Enum):
    STORE_MANAGER = 'store_manager'
    SUPPLIER = 'supplier'
    STAFF = 'staff'

class User:
    def __init__(self, username, password, email, role, bio='', location='', birth_date=None, _id=None):
        self.username = username
        self.password_hash = self.hash_password(password) if isinstance(password, str) else password
        self.email = email
        self.role = role
        self.bio = bio
        self.location = location
        self.birth_date = birth_date
        self._id = _id

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def save(self):
        logger.info(f"Saving user: {self.username}")
        user_data = {
            'username': self.username,
            'password_hash': self.password_hash,
            'email': self.email,
            'role': self.role,
            'bio': self.bio,
            'location': self.location,
            'birth_date': self.birth_date
        }

        if self._id:
            db.users.update_one({'_id': self._id}, {'$set': user_data})
        else:
            self._id = db.users.insert_one(user_data).inserted_id

    @staticmethod
    def from_dict(user_data):
        return User(
            username=user_data['username'],
            password=user_data['password_hash'],
            email=user_data['email'],
            role=user_data['role'],
            bio=user_data.get('bio', ''),
            location=user_data.get('location', ''),
            birth_date=user_data.get('birth_date', ''),
            _id=user_data.get('_id')
        )

    @staticmethod
    def get_by_username(username):
        logger.info(f"Fetching user by username: {username}")
        user_data = db.users.find_one({'username': username})
        if user_data:
            return User.from_dict(user_data)

    @staticmethod
    def get_by_email(email):
        user_data = db.users.find_one({'email': email})
        if user_data:
            return User.from_dict(user_data)

    @staticmethod
    def get_by_id(user_id):
        user_data = db.users.find_one({'_id': ObjectId(user_id)})
        if user_data:
            return User.from_dict(user_data)

    @staticmethod
    def check_password(stored_password, provided_password):
        logger.info("Checking password for user login")
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)
