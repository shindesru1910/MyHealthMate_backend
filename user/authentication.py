# import jwt
import datetime
import uuid

def create_token(id, email,name):
    return jwt.encode({
        'user_id': id,
        'useremail':email,
        'username':name,
        'exp': datetime.datetime.now() + datetime.timedelta(days=7),
        'iat': datetime.datetime.now()
    }, 'srushti', algorithm='HS256')
