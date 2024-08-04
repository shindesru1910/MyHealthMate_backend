import jwt
import datetime
import uuid
import jwt 

def create_token(id, email,name,is_admin,activity_level,health_goals):
    return jwt.encode({
        'user_id': id,
        'useremail':email,
        'username':name,
        'is_admin':is_admin,
        'activity_level':activity_level,
        'health_goals':health_goals,
        'exp': datetime.datetime.now() + datetime.timedelta(days=7),
        'iat': datetime.datetime.now()
    }, 'srushti', algorithm='HS256')
