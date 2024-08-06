import jwt
import datetime
import uuid


def create_token(id, email,name,is_admin,activity_level,health_goals,dietary_preferences,health_conditions):
    return jwt.encode({
        'user_id': id,
        'useremail':email,
        'username':name,
        'is_admin':is_admin,
        'activity_level':activity_level,
        'health_goals':health_goals,
        'dietary_preferences':dietary_preferences,
        'health_conditions':health_conditions,
        'exp': datetime.datetime.now() + datetime.timedelta(days=7),
        'iat': datetime.datetime.now()
    }, 'srushti', algorithm='HS256')
