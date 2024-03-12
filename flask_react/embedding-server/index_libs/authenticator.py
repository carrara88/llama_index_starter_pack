# authenticator.py
import jwt
import datetime
import json
import os


# NOTE: This should be a complex and unique secret key for your application
SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'insert-your-unique-secret-key-here')

class JWTAuth:
    users_json = os.getenv('JWT_USERS', '{}')
    try:
        users = json.loads(users_json)
    except json.JSONDecodeError:
        print(f"Error decoding JWT_USERS from JSON: {users_json}")
        users = {}

    @staticmethod
    def authenticate_user(username, password):
        try:
            user_info = JWTAuth.users.get(username)
            if user_info and user_info['password'] == password:
                return user_info
            return False
        except json.JSONDecodeError:
            print(f"Error decoding JWT")
    @staticmethod
    def encode_auth_token(user_id, role, index_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id,
                'role': role,
                'index_id': index_id
            }
            return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        except Exception as e:
            return e
    
    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'