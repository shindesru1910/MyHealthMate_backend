import jwt
import datetime
import uuid

def create_token(id, email, name):
    try:
        payload = {
            'user_id': id,
            'useremail': email,
            'username': name,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),  # Token expiration time
            'iat': datetime.datetime.utcnow()  # Token issued at time
        }
        token = jwt.encode(payload, 'srushti', algorithm='HS256')
        return token
    except Exception as e:
        print(f"Error creating token: {e}")
        return None
