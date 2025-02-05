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



def create_doctor_token(user_id,doctor_id, email, name, is_admin, specialty, contact_info):
    return jwt.encode({
        'user_id' : user_id,
        'doctor_id': doctor_id,
        'doctoremail': email,
        'doctorname': name,
        'is_admin': is_admin,
        'specialty': specialty,
        'contact_info': contact_info,
        'exp': datetime.datetime.now() + datetime.timedelta(days=7),
        'iat': datetime.datetime.now()
    }, 'srushti', algorithm='HS256')


def decode_token(token):
    try:
        payload = jwt.decode(token, 'srushti', algorithm='HS256')
        return payload
    except jwt.ExpiredSignatureError:
        return {'error': 'Token has expired'}
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}
    except Exception as e:
        return {'error': str(e)}