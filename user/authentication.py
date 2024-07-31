import jwt
import datetime
import uuid
import jwt 

def create_token(id, email,name,is_admin):
    return jwt.encode({
        'user_id': id,
        'useremail':email,
        'username':name,
        'is_admin':is_admin,
        'exp': datetime.datetime.now() + datetime.timedelta(days=7),
        'iat': datetime.datetime.now()
    }, 'srushti', algorithm='HS256')
