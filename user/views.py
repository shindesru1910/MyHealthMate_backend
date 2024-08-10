from datetime import time
import json
import logging
from django.forms import ValidationError
from django.utils.dateparse import parse_datetime
import pytz
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from . models import *
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.http import JsonResponse

from django.contrib.auth import authenticate
from .authentication import create_token

from django.utils.dateparse import parse_time
from django.core.mail import send_mail

from django.contrib.auth.decorators import login_required

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.models import User
import logging
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')




# import os
# from django.db.models import Sum
# import jwt
# from datetime import datetime,timezone,timedelta
# from firebase_admin import credentials
# from firebase_admin import firestore


logger = logging.getLogger(__name__)

ist_timezone = pytz.timezone('Asia/Kolkata')

@csrf_exempt
def login(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=400)

    email = request.POST.get('email')
    password = request.POST.get('password')

    user = authenticate(request, email=email, password=password)

    if user is not None:
        # Initialize variables with default values
        activity_level = None
        health_goals = None
        
        try:
            # Get the UserProfile associated with the user
            user_profile = UserProfile.objects.get(user=user)
            activity_level = user_profile.activity_level
            health_goals = user_profile.health_goals
            dietary_preferences = user_profile.dietary_preferences
            health_conditions = user_profile.health_conditions
           
            
        except UserProfile.DoesNotExist:
            # Handle the case where UserProfile does not exist
            pass

        # Create token with activity_level and health_goals
        token = create_token(user.id, user.email, user.first_name + ' ' + user.last_name, user.is_admin, activity_level, health_goals, dietary_preferences, health_conditions)
        return JsonResponse({'status': 200, 'msg': 'Login Successfully', 'token': token}, status=200)
    else:
        return JsonResponse({'status': 400, 'msg': 'Check your email or password!!'}, status=400)

@csrf_exempt
def create_user(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)
    
    try:
        print("POST Request")
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        password = request.POST.get('password')

        weight = request.POST.get('weight')
        height = request.POST.get('height')
        activity_level = request.POST.get('activity_level')
        dietary_preferences = request.POST.get('dietary_preferences')
        health_conditions = request.POST.get('health_conditions')
        medical_history = request.POST.get('medical_history')
        health_goals = request.POST.get('health_goals')
        membership_status = request.POST.get('membership_status')

        # Validate required fields
        if not phone or not email:
            return JsonResponse({'msg': 'Phone and email are required', 'status': 400}, status=400)
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse({'msg': 'Email already exists', 'status': 400}, status=400)

        # Create the User
        user = User(phone=phone, email=email, first_name=first_name, last_name=last_name, 
                    date_of_birth=date_of_birth, gender=gender)
        user.set_password(password)
        user.save()

        # Create the UserProfile
        user_profile = UserProfile(
            user=user, weight=weight, height=height, activity_level=activity_level,
            dietary_preferences=dietary_preferences, health_conditions=health_conditions,
            medical_history=medical_history, health_goals=health_goals, 
            membership_status=membership_status
        )
        user_profile.save()

        return JsonResponse({'msg': 'User Created Successfully', 'status': 200}, status=200)
    
    except Exception as e:
        return JsonResponse({'msg': str(e), 'status': 500}, status=500)


@csrf_exempt
def get_user(request):
    try:
        users = User.objects.all()
        data = []

        for user in users:
            user_dict = {
                'id': user.id,
                'phone': user.phone,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'date_of_birth': user.date_of_birth,
                'gender': user.gender,
            }

            try:
                user_profile = user.userprofile
                user_dict.update({
                    'weight': user_profile.weight,
                    'height': user_profile.height,
                    'activity_level': user_profile.activity_level,
                    'dietary_preferences': user_profile.dietary_preferences,
                    'health_conditions': user_profile.health_conditions,
                    'medical_history': user_profile.medical_history,
                    'health_goals': user_profile.health_goals,
                    'membership_status': user_profile.membership_status,
                })
            except UserProfile.DoesNotExist:
                user_dict.update({
                    'weight': None,
                    'height': None,
                    'activity_level': None,
                    'dietary_preferences': None,
                    'health_conditions': None,
                    'medical_history': None,
                    'health_goals': None,
                    'membership_status': None,
                })

            data.append(user_dict)
        
        return JsonResponse({'data': data, 'status': 200}, status=200)
    except Exception as e:
        return JsonResponse({'data': str(e), 'status': 500}, status=200)
    
@csrf_exempt
def update_user(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request','status':403},status = 200)
    
    try:
        id = request.POST['id']
        phone = request.POST['phone']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        date_of_birth = request.POST['date_of_birth']
        gender = request.POST['gender']

        weight = request.POST['weight']
        height = request.POST['height']
        activity_level = request.POST['activity_level']
        dietary_preferences = request.POST['dietary_preferences']
        health_conditions = request.POST['health_conditions']
        medical_history = request.POST['medical_history']
        health_goals = request.POST['health_goals']
        membership_status = request.POST['membership_status']

        # Update User data
        user = User.objects.get(id=id)
        user.phone = phone
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.date_of_birth = date_of_birth
        user.gender = gender
        user.save()

        # Update or create UserProfile data
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.weight = weight
        user_profile.height = height
        user_profile.activity_level = activity_level
        user_profile.dietary_preferences = dietary_preferences
        user_profile.health_conditions = health_conditions
        user_profile.medical_history = medical_history
        user_profile.health_goals = health_goals
        user_profile.membership_status = membership_status
        user_profile.save()

        return JsonResponse({'msg':'Data has been updated successfully','status':200},status=200)
    except Exception as e:
        return JsonResponse({'msg':str(e),'status':500},status=200)
    
@csrf_exempt
def delete_user(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)
    
    try:
        id = request.POST['id']

        user = User.objects.get(id = id)
        user.delete()

        return JsonResponse({'msg':'Data has been removed successfully','status':200},status=200)
    except Exception as e:
        return JsonResponse({'msg':str(e),'status':500},status=200)



@csrf_exempt
def create_user_profile(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)
    
    try:
        user_id = request.POST['user_id']
        user = User.objects.get(id = user_id)
        weight = request.POST['weight']
        height = request.POST['height']
        activity_level = request.POST['activity_level']
        dietary_preferences = request.POST['dietary_preferences']
        health_conditions = request.POST['health_conditions']
        medical_history = request.POST['medical_history']
        health_goals = request.POST['health_goals']
        membership_status = request.POST['membership_status']
        
        user_user = UserProfile.objects.create(user=user,weight=weight,height= height,activity_level= activity_level, dietary_preferences= dietary_preferences,health_conditions= health_conditions,health_goals=health_goals,medical_history=medical_history,membership_status= membership_status)
        user_user.save()
        return JsonResponse({'msg': 'Data has been successfully created', 'status': 200}, status=200)
    except Exception as e:
        return JsonResponse({'msg': str(e), 'status': 500}, status=500)
    
@csrf_exempt
def get_user_profile(request):
    try:
        users_profile = UserProfile.objects.all()
        data = []

        for user_profile in users_profile:
            user_profile_dict ={}
            user_profile_dict['id'] = user_profile.id
            user_profile_dict['weight'] = user_profile.weight
            user_profile_dict['height'] = user_profile.height
            user_profile_dict['activity_level'] = user_profile.activity_level
            user_profile_dict['dietary_preferences'] = user_profile.dietary_preferences
            user_profile_dict['health_conditions'] = user_profile.health_conditions
            user_profile_dict['medical_history'] = user_profile.medical_history
            user_profile_dict['health_goals'] = user_profile.health_goals
            user_profile_dict['health_goals'] = user_profile.health_goals
            user_profile_dict['membership_status'] = user_profile.membership_status


            data.append(user_profile_dict)
        return JsonResponse({'data':data,'status':200},status = 200)
    except Exception as e:
        return JsonResponse({'data':str(e),'status':500},status = 200)
    
@csrf_exempt
def update_user_profile(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request','status':403},status = 200)
    try:
        id = request.POST['id']
        weight = request.POST['weight']
        height = request.POST['height']
        activity_level = request.POST['activity_level']
        dietary_preferences = request.POST['dietary_preferences']
        health_conditions = request.POST['health_conditions']
        medical_history = request.POST['medical_history']
        health_goals = request.POST['health_goals']
        membership_status = request.POST['membership_status']

        user_profile = UserProfile.objects.get(id = id)
        user_profile.weight = weight
        user_profile.height = height
        user_profile.activity_level = activity_level
        user_profile.dietary_preferences = dietary_preferences
        user_profile.health_conditions = health_conditions
        user_profile.medical_history = medical_history
        user_profile.health_goals = health_goals
        user_profile.membership_status = membership_status
        user_profile.save()
        return JsonResponse({'msg':'Data has been updated successfully','status':200},status = 200)
    except Exception as e:
        return JsonResponse({'msg':str(e),'status':500},status = 200)
    
@csrf_exempt
def delete_user_profile(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)
    
    try:
        id = request.POST['id']

        user_profile = UserProfile.objects.get(id = id)
        user_profile.delete()

        return JsonResponse({'msg':'Data has been removed successfully','status':200},status=200)
    except Exception as e:
        return JsonResponse({'msg':str(e),'status':500},status=200)




@csrf_exempt
def create_doctor(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)
    
    try:
        # Retrieve data from POST request
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        specialty = request.POST['specialty']
        contact_info = request.POST['contact_info']
        reviews = request.POST['reviews']
        location = request.POST['location']

        # Create a Doctor object and save it
        doctor_obj = Doctor(first_name=first_name, last_name=last_name, specialty=specialty, contact_info=contact_info, reviews=reviews, location=location)
        doctor_obj.save()

        return JsonResponse({'msg': 'Data has been successfully created', 'status': 200}, status=200)
    except Exception as e:
        return JsonResponse({'msg': str(e), 'status': 500}, status=500)
    
@csrf_exempt
def get_doctor(request):
    try:
        doctors = Doctor.objects.all()
        data = []

        for doctor in doctors:
            doctor_dict ={}
            doctor_dict['id'] = doctor.id
            doctor_dict['first_name'] = doctor.first_name
            doctor_dict['last_name'] = doctor.last_name
            doctor_dict['specialty'] = doctor.specialty
            doctor_dict['contact_info'] = doctor.contact_info
            doctor_dict['reviews'] = doctor.reviews
            doctor_dict['location'] = doctor.location


            data.append(doctor_dict)
        return JsonResponse({'data':data,'status':200},status = 200)
    except Exception as e:
        return JsonResponse({'data':str(e),'status':500},status = 200)
    

@csrf_exempt
def get_doctor_by_id(request, doctor_id):
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        doctor_dict = {
            'id': doctor.id,
            'first_name': doctor.first_name,
            'last_name': doctor.last_name,
            'specialty': doctor.specialty,
            'contact_info': doctor.contact_info,
            'reviews': doctor.reviews,
            'location': doctor.location
        }
        return JsonResponse({'data': doctor_dict, 'status': 200}, status=200)
    except Doctor.DoesNotExist:
        return JsonResponse({'data': 'Doctor not found', 'status': 404}, status=404)
    except Exception as e:
        return JsonResponse({'data': str(e), 'status': 500}, status=500)
    
@csrf_exempt
def update_doctor(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request','status':403},status = 200)
    try:
        id = request.POST['id']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        specialty = request.POST['specialty']
        contact_info = request.POST['contact_info']
        reviews = request.POST['reviews']
        location = request.POST['location']

        doctor = Doctor.objects.get(id = id)
        doctor.first_name = first_name
        doctor.last_name = last_name
        doctor.specialty = specialty
        doctor.contact_info = contact_info
        doctor.reviews = reviews
        doctor.location = location
        doctor.save()
        return JsonResponse({'msg':'Data has been updated successfully','status':200},status = 200)
    except Exception as e:
        return JsonResponse({'msg':str(e),'status':500},status = 200)
    
@csrf_exempt
def delete_doctor(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)
    
    try:
        id = request.POST['id']

        doctor = Doctor.objects.get(id = id)
        doctor.delete()

        return JsonResponse({'msg':'Data has been removed successfully','status':200},status=200)
    except Exception as e:
        return JsonResponse({'msg':str(e),'status':500},status=200)
    
# Get Speciality for Appointment form API
@csrf_exempt
def get_specialties(request):
    if request.method != 'GET':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=200)
    
    try:
        # Retrieve unique specialties from the Doctor model
        specialties = Doctor.objects.values_list('specialty', flat=True).distinct()
        return JsonResponse({'specialties': list(specialties), 'status': 200}, status=200)
    except Exception as e:
        return JsonResponse({'msg': str(e), 'status': 500}, status=200)
    
# For Submitting the Appointment form, Submit API
@csrf_exempt
def submit_appointment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        specialty = request.POST.get('speciality')
        doctor_id = request.POST.get('doctor')
        message = request.POST.get('message')

        print(f'Received data: {name}, {email}, {phone}, {date}, {specialty}, {doctor_id}, {message}')

        if not all([name, email, phone, date, specialty, doctor_id, message]):
            return JsonResponse({'error': 'Missing required fields', 'data': {'name': name, 'email': email, 'phone': phone, 'date': date, 'specialty': specialty, 'doctor_id': doctor_id, 'message': message}}, status=400)

        try:
            user = User.objects.get(email=email)
            doctor = Doctor.objects.get(id=doctor_id)

            if Appointment.objects.filter(doctor=doctor, appointment_date=date).exists():
                return JsonResponse({'error': 'This date slot is already booked'}, status=400)

            appointment = Appointment(
                user=user,
                doctor=doctor,
                appointment_date=date,
                status='scheduled',
                phone=phone,
                specialty=specialty,
                message=message 
            )
            appointment.clean()
            appointment.save()

            return JsonResponse({'status': 'OK'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Doctor.DoesNotExist:
            return JsonResponse({'error': 'Doctor not found'}, status=404)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def get_available_slots(request):
    doctor_id = request.GET.get('doctor_id')
    date = request.GET.get('date')

    if not doctor_id or not date:
        return JsonResponse({'error': 'Missing required parameters'}, status=400)

    try:
        doctor = Doctor.objects.get(id=doctor_id)
        booked_slots = Appointment.objects.filter(doctor=doctor, appointment_date=date).values_list('appointment_time', flat=True)

        # Example available slots, assuming 30-minute intervals
        all_slots = ['09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30']
        available_slots = [slot for slot in all_slots if slot not in booked_slots]

        return JsonResponse({'available_slots': available_slots})
    except Doctor.DoesNotExist:
        return JsonResponse({'error': 'Doctor not found'}, status=404)



@csrf_exempt
def create_diet_plan(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)
    
    try:
        name = request.POST['name']
        description = request.POST['description']
        suitable_for = request.POST['suitable_for']
        
        dietplan_obj = DietPlan(
            name=name, 
            description=description,
            suitable_for=suitable_for
            
        )
        dietplan_obj.save()

        return JsonResponse({'msg': 'Diet Plan created successfully', 'status': 200}, status=200)
    except Exception as e:
        return JsonResponse({'msg': str(e), 'status': 500}, status=500)
    
@csrf_exempt
def get_diet_plan(request):
    try:
        dietplan = DietPlan.objects.all()
        data = []

        for dietplan in dietplan:
            dietplan_dict ={}
            dietplan_dict['name'] = dietplan.name
            dietplan_dict['description'] = dietplan.description
            dietplan_dict['suitable_for'] = dietplan.suitable_for

        
            data.append(dietplan_dict)
        return JsonResponse({'data':data,'status':200},status = 200)
    except Exception as e:
        return JsonResponse({'data':str(e),'status':500},status = 200)
    
@csrf_exempt
def update_diet_plan(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request','status':403},status = 200)
    try:
        id = request.POST['id']
        name = request.POST['name']
        description = request.POST['description']
        suitable_for = request.POST['suitable_for']
    
        dietplan = DietPlan.objects.get(id=id)
        dietplan.name = name
        dietplan.description = description
        dietplan.suitable_for = suitable_for
        dietplan.save()
        return JsonResponse({'msg':'Data has been updated successfully','status':200},status = 200)
    except Exception as e:
        return JsonResponse({'msg':str(e),'status':500},status = 200)
    
@csrf_exempt
def delete_diet_plan(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)
    
    try:
        id = request.POST['id']

        dietplan = DietPlan.objects.get(id = id)
        dietplan.delete()

        return JsonResponse({'msg':'Data has been removed successfully','status':200},status=200)
    except Exception as e:
        return JsonResponse({'msg':str(e),'status':500},status=200)

@csrf_exempt
def create_exerciseplan(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)
    
    try:
        # Retrieve data from POST request
        name = request.POST['name']
        description = request.POST['description']
        suitable_for = request.POST['suitable_for']

        exercise_obj = ExercisePlan(name=name, description=description, suitable_for=suitable_for)
        exercise_obj.save()

        return JsonResponse({'msg': 'Data has been successfully created', 'status': 200}, status=200)
    except Exception as e:
        return JsonResponse({'msg': str(e), 'status': 500}, status=500)
@csrf_exempt
def get_exerciseplan(request):
    try:
        exercises = ExercisePlan.objects.all()
        data = []

        for exercise in exercises:
            exercise_dict ={}
            exercise_dict['id'] = exercise.id
            exercise_dict['first_name'] = exercise.name
            exercise_dict['last_name'] = exercise.description
            exercise_dict['specialty'] = exercise.suitable_for


            data.append(exercise_dict)
        return JsonResponse({'data':data,'status':200},status = 200)
    except Exception as e:
        return JsonResponse({'data':str(e),'status':500},status = 200)
    
@csrf_exempt
def delete_exerciseplan(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)
    
    try:
        id = request.POST['id']

        exercise = ExercisePlan.objects.get(id = id)
        exercise.delete()

        return JsonResponse({'msg':'Data has been removed successfully','status':200},status=200)
    except Exception as e:
        return JsonResponse({'msg':str(e),'status':500},status=200)
    
@csrf_exempt
def update_exerciseplan(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request','status':403},status = 200)
    try:
        id = request.POST['id']
        name = request.POST['name']
        description = request.POST['description']
        suitable_for = request.POST['suitable_for']

        exercise = ExercisePlan.objects.get(id = id)
        exercise.name = name
        exercise.description = description
        exercise.suitable_for = suitable_for
        exercise.save()
        return JsonResponse({'msg':'Data has been updated successfully','status':200},status = 200)
    except Exception as e:
        return JsonResponse({'msg':str(e),'status':500},status = 200)
    
    
@csrf_exempt
def create_health_recommendation(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)
    
    try:
        user_id = request.POST['user']
        diet_plan = request.POST['diet_plan']
        exercise_plan = request.POST['exercise_plan']
        
        user = User.objects.get(id=user_id)
        recommendation = HealthRecommendation(
            user=user, 
            diet_plan=diet_plan,
            exercise_plan=exercise_plan
        )
        recommendation.save()
        
        return JsonResponse({'msg': 'Health recommendation created successfully', 'status': 200}, status=200)
    except Exception as e:
        return JsonResponse({'msg': str(e), 'status': 500}, status=500)
    
@csrf_exempt
def get_health_recommendation(request):
    try:
        recommendations = HealthRecommendation.objects.all()
        data = []

        for recommendation in recommendations:
            recommendation_dict = {}
            recommendation_dict['id'] = recommendation.id
            recommendation_dict['user'] = recommendation.user.id
            recommendation_dict['diet_plan'] = recommendation.diet_plan
            recommendation_dict['exercise_plan'] = recommendation.exercise_plan
            recommendation_dict['created_at'] = recommendation.created_at
            recommendation_dict['updated_at'] = recommendation.updated_at

            data.append(recommendation_dict)
        return JsonResponse({'data': data, 'status': 200}, status=200)
    except Exception as e:
        return JsonResponse({'msg': str(e), 'status': 500}, status=500)

@csrf_exempt
def update_health_recommendation(request):
    # this will be comment of this API
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)
    
    try:
        recommendation_id = request.POST['id']
        diet_plan = request.POST['diet_plan']
        exercise_plan = request.POST['exercise_plan']
        
        recommendation = HealthRecommendation.objects.get(id=recommendation_id)
        recommendation.diet_plan = diet_plan
        recommendation.exercise_plan = exercise_plan
        recommendation.save()
        
        return JsonResponse({'msg': 'Health recommendation updated successfully', 'status': 200}, status=200)
    except Exception as e:
        return JsonResponse({'msg': str(e), 'status': 500}, status=500)

@csrf_exempt
def delete_health_recommendation(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)
    
    try:
        recommendation_id = request.POST['id']
        recommendation = HealthRecommendation.objects.get(id=recommendation_id)
        recommendation.delete()
        
        return JsonResponse({'msg': 'Health recommendation deleted successfully', 'status': 200}, status=200)
    except Exception as e:
        return JsonResponse({'msg': str(e), 'status': 500}, status=500)

@csrf_exempt
def create_health_report(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)
    
    try:
        user_id = request.POST['user_id']
        report_name = request.POST['report_name']
        report_file = request.POST['report_file']

        user = User.objects.get(id=user_id)
        report = HealthReport(user=user, report_name=report_name, report_file=report_file)
        report.save()

        return JsonResponse({'msg': 'Data has been successfully created', 'status': 200}, status=200)
    except Exception as e:
        return JsonResponse({'msg': str(e), 'status': 500}, status=500)

@csrf_exempt
def get_health_report(request):
    try:
        reports = HealthReport.objects.all()
        data = []

        for report in reports:
            report_dict = {}
            report_dict['id'] = report.id
            report_dict['user'] = report.user.id
            report_dict['report_name'] = report.report_name
            report_dict['report_file'] = report.report_file
            report_dict['date'] = report.date

            data.append(report_dict)
        return JsonResponse({'data': data, 'status': 200}, status=200)
    except Exception as e:
        return JsonResponse({'msg': str(e), 'status': 500}, status=500)


@csrf_exempt
def update_health_report(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)
    try:
        id = request.POST['id']
        user_id = request.POST['user_id']
        report_name = request.POST['report_name']
        report_file = request.POST['report_file']

        report = HealthReport.objects.get(id=id)
        report.user = User.objects.get(id=user_id)
        report.report_name = report_name
        report.report_file = report_file
        report.save()
        return JsonResponse({'msg': 'Data has been updated successfully', 'status': 200}, status=200)
    except Exception as e:
        return JsonResponse({'msg': str(e), 'status': 500}, status=500)

@csrf_exempt
def delete_health_report(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)
    
    try:
        id = request.POST['id']
        report = HealthReport.objects.get(id=id)
        report.delete()
        return JsonResponse({'msg': 'Data has been removed successfully', 'status': 200}, status=200)
    except Exception as e:
        return JsonResponse({'msg': str(e), 'status': 500}, status=500)

# Appointment APIs
@csrf_exempt
def create_appointment(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)

    try:
        # Extract data from the POST request
        first_name = request.POST.get('name')  # You can split this into first_name and last_name if needed
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        doctor_id = request.POST.get('doctor_id')
        message = request.POST.get('message')

        # Find or create the user using first_name and last_name instead of 'name'
        user, created = User.objects.get_or_create(
            email=email,
            defaults={'first_name': first_name, 'last_name': '', 'email': email, 'password': '',phone:''}
        )

        # Get the selected doctor
        doctor = Doctor.objects.get(id=doctor_id)

        # Create the appointment
        appointment = Appointment(
            user=user,
            doctor=doctor,
            appointment_date=date,
            status='Pending',  # or any default status
            message=message
        )
        appointment.save()

        return JsonResponse({'msg': 'Appointment has been successfully created', 'status': 200}, status=200)
    except Doctor.DoesNotExist:
        return JsonResponse({'msg': 'Doctor not found', 'status': 404}, status=404)
    except Exception as e:
        return JsonResponse({'msg': str(e), 'status': 500}, status=500)

@csrf_exempt
def get_appointment(request):
    try:
        appointments = Appointment.objects.all()
        data = []

        for appointment in appointments:
            appointment_dict = {}
            appointment_dict['id'] = appointment.id
            appointment_dict['user'] = appointment.user.id
            appointment_dict['doctor'] = appointment.doctor.id
            appointment_dict['appointment_date'] = appointment.appointment_date
            appointment_dict['status'] = appointment.status
            appointment_dict['created_at'] = appointment.created_at
            appointment_dict['updated_at'] = appointment.updated_at

            data.append(appointment_dict)
        return JsonResponse({'data': data, 'status': 200}, status=200)
    except Exception as e:
        return JsonResponse({'msg': str(e), 'status': 500}, status=500)
    
@csrf_exempt
def get_appointments_by_user(request):
    if request.method == 'GET':
        try:
            user_id = request.GET.get('user_id')
            if not user_id:
                return JsonResponse({'error': 'User ID not provided'}, status=400)

            appointments = Appointment.objects.filter(user_id=user_id)
            data = []
            for appointment in appointments:
                data.append({
                    'id': appointment.id,
                    'appointment_date': appointment.appointment_date,
                    'status': appointment.status,
                    'doctor': appointment.doctor_id,  # Use doctor_id to fetch doctor details separately
                    'created_at': appointment.created_at,
                    'updated_at': appointment.updated_at,
                })

            return JsonResponse({'data': data, 'status': 200}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def update_appointment(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)
    try:
        id = request.POST['id']
        user_id = request.POST['user_id']
        doctor_id = request.POST['doctor_id']
        appointment_date = request.POST['appointment_date']
        status = request.POST['status']

        appointment = Appointment.objects.get(id=id)
        appointment.user = User.objects.get(id=user_id)
        appointment.doctor = Doctor.objects.get(id=doctor_id)
        appointment.appointment_date = appointment_date
        appointment.status = status
        appointment.save()
        return JsonResponse({'msg': 'Data has been updated successfully', 'status': 200}, status=200)
    except Exception as e:
        return JsonResponse({'msg': str(e), 'status': 500}, status=500)

@csrf_exempt
def delete_appointment(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)
    
    try:
        id = request.POST['id']
        appointment = Appointment.objects.get(id=id)
        appointment.delete()
        return JsonResponse({'msg': 'Data has been removed successfully', 'status': 200}, status=200)
    except Exception as e:
        return JsonResponse({'msg': str(e), 'status': 500}, status=500)


# Feedback APIs
@csrf_exempt
def create_feedback(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)
    
    try:
        user_id = request.POST['user_id']
        feedback_text = request.POST['feedback_text']

        user = User.objects.get(id=user_id)
        feedback = Feedback(user=user, feedback_text=feedback_text)
        feedback.save()

        return JsonResponse({'msg': 'Data has been successfully created', 'status': 200}, status=200)
    except Exception as e:
        return JsonResponse({'msg': str(e), 'status': 500}, status=500)




@csrf_exempt
def get_feedback(request):
    try:
        feedbacks = Feedback.objects.select_related('user').all()  
        data = []

        for feedback in feedbacks:
            feedback_dict = {
                'id': feedback.id,
                'user': {
                    'id': feedback.user.id,
                    'first_name': feedback.user.first_name,
                    'last_name': feedback.user.last_name
                },
                'feedback_text': feedback.feedback_text,
                'created_at': feedback.created_at
            }
            data.append(feedback_dict)

        return JsonResponse({'data': data, 'status': 200}, status=200)
    except Exception as e:
        return JsonResponse({'msg': str(e), 'status': 500}, status=500)

@csrf_exempt
def update_feedback(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)
    try:
        id = request.POST['id']
        user_id = request.POST['user_id']
        feedback_text = request.POST['feedback_text']

        feedback = Feedback.objects.get(id=id)
        feedback.user = User.objects.get(id=user_id)
        feedback.feedback_text = feedback_text
        feedback.save()
        return JsonResponse({'msg': 'Data has been updated successfully', 'status': 200}, status=200)
    except Exception as e:
        return JsonResponse({'msg': str(e), 'status': 500}, status=500)

@csrf_exempt
def delete_feedback(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)
    
    try:
        id = request.POST['id']
        feedback = Feedback.objects.get(id=id)
        feedback.delete()
        return JsonResponse({'msg': 'Data has been removed successfully', 'status': 200}, status=200)
    except Exception as e:
        return JsonResponse({'msg': str(e), 'status': 500}, status=500)

logger = logging.getLogger(__name__)



# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.utils import formataddr
from user.tasks import send_mail_func
@csrf_exempt
def send_mail_to_all(request):
    send_mail_func.delay() 
    return HttpResponse("Sent")
#     if request.method == 'POST':
#         try:
#             # data = json.loads(request.body)
#             email = request.POST.get('email')
#             subject = request.POST.get('subject')
#             message = request.POST.get('message')
#             reminder_time_str = request.POST.get('reminder_time')  # Expecting a time string like 'HH:MM'
#             reminder_time = time.fromisoformat(reminder_time_str)  # Convert string to time object

#             if not all([email, subject, message, reminder_time]):
#                 return JsonResponse({'status': 'failure', 'error': 'Missing required fields'}, status=400)

#             # Create and save the EmailReminder instance
#             reminder = EmailReminder(
#                 email=email,
#                 subject=subject,
#                 message=message,
#                 reminder_time=reminder_time
#             )
#             reminder.save()
            
#             # Email settings
#             SMTP_SERVER = 'smtp.gmail.com'
#             SMTP_PORT = 587
#             SMTP_USER = 'myhealthmate2002@gmail.com'
#             SMTP_PASSWORD = 'aase utgi axcq aqwd'
#             FROM_EMAIL = 'myhealthmate2002@gmail.com'

#             # Create the email content
#             msg = MIMEMultipart()
#             msg['From'] = formataddr(('My Health Mate', FROM_EMAIL))
#             msg['To'] = email
#             msg['Subject'] = subject

#             msg.attach(MIMEText(message, 'It is time for your Exercise, Stay Fit!'))

#             # Connect to the SMTP server and send the email
#             with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#                 server.starttls()
#                 server.login(SMTP_USER, SMTP_PASSWORD)
#                 server.send_message(msg)
            
#             return JsonResponse({'status': 'success'})

#         except Exception as e:
#             return JsonResponse({'status': 'failure', 'error': str(e)}, status=400)

#     return JsonResponse({'status': 'failure'}, status=400)



User = get_user_model()
@csrf_exempt
def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        logger.debug(f"Received password reset request for email: {email}")
        associated_user = User.objects.filter(email=email).first()
        print(associated_user)
        if associated_user:
            logger.debug(f"User found: {associated_user.email}")
            subject = "Password Reset Requested"
            email_template_name = "password_reset_email.html"
            context = {
                "email": associated_user.email,
                "domain": request.get_host(),
                "site_name": "MyHealthMate",
                "uid": urlsafe_base64_encode(force_bytes(associated_user.pk)),
                "token": default_token_generator.make_token(associated_user),
                "protocol": 'http',
            }
            email = render_to_string(email_template_name, context)
            try:
                send_mail(subject, email, settings.EMAIL_HOST_USER, [associated_user.email])
                logger.debug(f"Password reset email sent to {associated_user.email}")
            except BadHeaderError:
                logger.error("Invalid header found.")
                return HttpResponse('Invalid header found.')
            except Exception as e:
                logger.error(f"An error occurred: {str(e)}")
                return HttpResponse(f'An error occurred: {str(e)}')
        else:
            logger.debug("No user found with the provided email.")
        return JsonResponse({"message": "If an account with the provided email exists, a password reset link has been sent."})

@csrf_exempt   
def password_reset_confirm(request, uidb64=None, token=None):
    if request.method == 'POST':
        uid = force_text(urlsafe_base64_decode(uidb64))  # type: ignore
        user = User.objects.get(pk=uid)
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Password has been reset successfully."})
        else:
            return JsonResponse({"errors": form.errors}, status=400)
    else:
        return render(request, 'password_reset_confirm.html', {'uidb64': uidb64, 'token': token})


@csrf_exempt
def get_exercise_recommendations(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            activity_level = data.get('activity_level')
            
            recommendations = {
                "sedentary": {
                    "Walking": {
                        "Frequency": "5 days a week",
                        "Duration": "20-30 minutes",
                        "Intensity": "Start with a comfortable pace and gradually increase the speed as fitness improves."
                    },
                    "Basic Strength Training": {
                        "Frequency": "2-3 days a week",
                        "Exercises": "Bodyweight exercises like squats, lunges, push-ups, and planks.",
                        "Reps/Sets": "2-3 sets of 10-12 reps for each exercise."
                    },
                    "Stretching": {
                        "Frequency": "Daily",
                        "Duration": "5-10 minutes",
                        "Focus": "Stretch major muscle groups (hamstrings, quadriceps, back, shoulders)."
                    },
                    "Light Aerobics or Low-Impact Cardio": {
                        "Frequency": "3 days a week",
                        "Duration": "15-20 minutes",
                        "Options": "Light aerobic exercises, cycling, or swimming."
                    },
                    "Yoga or Pilates": {
                        "Frequency": "2-3 days a week",
                        "Duration": "20-30 minutes",
                        "Benefits": "Improves flexibility, core strength, and mental relaxation."
                    },
                    "Rest Days": "Ensure 1-2 rest days per week to allow the body to recover.",
                    "videos": [
                        "https://www.youtube.com/watch?v=DK2Erw90gMw",
                        "https://www.youtube.com/watch?v=7zPiD3ibvCc"
                    ]
                },
                "lightly_active": {
                    "Cardio Workouts": {
                        "Frequency": "4-5 days a week",
                        "Duration": "30-40 minutes",
                        "Options": "Brisk walking, Jogging, Cycling, Swimming",
                        "Intensity": "Moderate; maintain a pace where you can talk but not sing."
                    },
                    "Strength Training": {
                        "Frequency": "3 days a week",
                        "Exercises": "Weightlifting (light to moderate weights), Resistance band exercises, Bodyweight exercises like push-ups, squats, lunges, and planks.",
                        "Reps/Sets": "3 sets of 12-15 reps for each exercise."
                    },
                    "High-Intensity Interval Training (HIIT)": {
                        "Frequency": "1-2 days a week",
                        "Duration": "20-30 minutes",
                        "Structure": "Short bursts of high-intensity exercise (like sprinting, jump squats) followed by rest or low-intensity exercise.",
                        "Example": "30 seconds of sprinting followed by 1 minute of walking, repeated for 20 minutes."
                    },
                    "Flexibility and Mobility Work": {
                        "Frequency": "Daily or as part of a cool-down routine",
                        "Duration": "10-15 minutes",
                        "Focus": "Stretch major muscle groups, especially after workouts.",
                        "Options": "Yoga, Pilates, or dedicated stretching routines."
                    },
                    "Core Workouts": {
                        "Frequency": "3 days a week",
                        "Exercises": "Planks, Russian twists, bicycle crunches, leg raises.",
                        "Reps/Sets": "3 sets of 15-20 reps for each exercise."
                    },
                    "Active Rest Days": {
                        "Frequency": "1-2 days a week",
                        "Activities": "Engage in light activities like walking, stretching, or recreational sports to stay active without stressing the body."
                    },"videos": [
                        "https://www.youtube.com/watch?v=KIxb-y3CaFk",
                        "https://www.youtube.com/watch?v=UFP5xIk2RhA"
                    ]
                },
                "moderately_active": {
                    "Cardiovascular Exercise": {
                        "Frequency": "4-5 days a week",
                        "Duration": "40-60 minutes",
                        "Options": "Running or jogging, Swimming, Cycling, Rowing, Dance classes or aerobics",
                        "Intensity": "Moderate to high; aim for a pace where you’re breathing hard but can still speak in short sentences."
                    },
                    "Strength Training": {
                        "Frequency": "3-4 days a week",
                        "Exercises": "Compound movements like squats, deadlifts, bench presses, and rows. Isolation exercises for specific muscles (e.g., bicep curls, tricep extensions).",
                        "Reps/Sets": "3-4 sets of 8-12 reps for each exercise.",
                        "Weight": "Use moderate to heavy weights that challenge you by the last few reps."
                    },
                    "High-Intensity Interval Training (HIIT)": {
                        "Frequency": "1-2 days a week",
                        "Duration": "20-30 minutes",
                        "Structure": "30-45 seconds of high-intensity exercise (e.g., sprints, burpees, jump squats) followed by 15-30 seconds of rest.",
                        "Example": "8 rounds of 30 seconds of sprinting followed by 30 seconds of walking."
                    },
                    "Flexibility and Mobility Work": {
                        "Frequency": "Daily or as part of a cool-down routine",
                        "Duration": "10-15 minutes",
                        "Focus": "Stretching and mobility exercises targeting major muscle groups.",
                        "Options": "Yoga, dynamic stretching, foam rolling."
                    },
                    "Core Workouts": {
                        "Frequency": "3-4 days a week",
                        "Exercises": "Planks, Russian twists, hanging leg raises, mountain climbers.",
                        "Reps/Sets": "3 sets of 15-20 reps or timed holds (e.g., 1-minute plank)."
                    },
                    "Cross-Training or Sports": {
                        "Frequency": "1-2 days a week",
                        "Activities": "Engage in sports or other activities like tennis, basketball, or hiking to add variety to your routine."
                    },
                    "Active Rest Days": {
                        "Frequency": "1 day a week",
                        "Activities": "Light activities such as walking, gentle cycling, or yoga to stay active without intense exertion."
                    },
                    "videos": [
                        "https://www.youtube.com/watch?v=uHYjN6Ou2-M",
                        "https://www.youtube.com/watch?v=rYlLXrKhRAc"
                    ]
                },
                "very_active": {
                    "Cardiovascular Exercise": {
                        "Frequency": "5-6 days a week",
                        "Duration": "45-60 minutes",
                        "Options": "Running (including intervals and long-distance), Swimming (laps and intervals), Cycling (road cycling or spinning), Rowing, Advanced aerobics or HIIT classes",
                        "Intensity": "High; incorporate various intensity levels, including steady-state cardio and interval training."
                    },
                    "Strength Training": {
                        "Frequency": "4-5 days a week",
                        "Exercises": "Compound lifts: Deadlifts, squats, bench presses, overhead presses, pull-ups. Olympic lifts (for advanced individuals): Cleans, snatches. Accessory lifts: Lunges, rows, dips, curls.",
                        "Reps/Sets": "4-5 sets of 6-10 reps for strength; 3-4 sets of 12-15 reps for hypertrophy (muscle growth).",
                        "Weight": "Use heavy weights that push you near failure by the last rep."
                    },
                    "High-Intensity Interval Training (HIIT)": {
                        "Frequency": "2-3 days a week",
                        "Duration": "20-30 minutes",
                        "Structure": "30 seconds to 1 minute of all-out effort (e.g., sprints, burpees, kettlebell swings) followed by 15-30 seconds of rest.",
                        "Example": "10 rounds of 30-second sprints with 30-second walking breaks."
                    },
                    "Flexibility and Mobility Work": {
                        "Frequency": "Daily",
                        "Duration": "15-20 minutes",
                        "Focus": "Prevent injury and improve performance by targeting tight or overworked muscles.",
                        "Options": "Yoga, dynamic stretching, mobility drills, foam rolling, PNF stretching."
                    },
                    "Core and Functional Training": {
                        "Frequency": "4-5 days a week",
                        "Exercises": "Planks, hanging leg raises, medicine ball throws, Russian twists, stability exercises (e.g., single-leg deadlifts).",
                        "Reps/Sets": "3-4 sets of 15-20 reps or timed holds (e.g., 1-2 minute plank)."
                    },
                    "Cross-Training or Specialized Sports Training": {
                        "Frequency": "2-3 days a week",
                        "Activities": "Engage in sports-specific training, such as soccer, basketball, martial arts, or rock climbing, or cross-train with activities like trail running, swimming, or cycling to maintain variety and prevent burnout."
                    },
                    "Recovery and Active Rest": {
                        "Frequency": "1 day a week (active rest)",
                        "Activities": "Light activities like yoga, stretching, walking, or swimming at a relaxed pace to allow recovery without total inactivity.",
                        "Focus": "Incorporate adequate sleep, hydration, and nutrition to support the high activity level."
                    },"videos": [
                        "https://www.youtube.com/watch?v=DK2Erw90gMw",
                        "https://www.youtube.com/watch?v=7zPiD3ibvCc"
                    ]
                }
            }
            
            # Return recommendations based on the activity level
            if activity_level in recommendations:
                return JsonResponse(recommendations[activity_level], safe=False)
            else:
                return JsonResponse({"error": "Activity level not supported"}, status=400)
            
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    
        except Exception as e:
        # Log the exception if necessary (for debugging purposes)
            return JsonResponse({"error": "An unexpected error occurred"}, status=500)
    
        finally:
        # Any cleanup code (if needed) goes here
            print("Request processing complete")


'''
@csrf_exempt
def get_exercise_recommendations(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            activity_level = data.get('activity_level')
            health_goals = data.get('health_goal')
            if not health_goals:
                raise ValueError("Health goals are missing.")
            
            recommendations = {
            "sedentary": {
                "weight_loss": {
                    "Walking": {
                        "Frequency": "5 days a week",
                        "Duration": "30 minutes",
                        "Intensity": "Moderate pace to burn calories."
                    },
                    "Bodyweight Circuit": {
                        "Frequency": "3 days a week",
                        "Exercises": "Squats, lunges, push-ups, and planks.",
                        "Reps/Sets": "3 sets of 15 reps.",
                        "Goal": "Burn fat and build endurance."
                    },
                    "Stretching": {
                        "Frequency": "Daily",
                        "Duration": "10 minutes",
                        "Focus": "Increase flexibility and prevent injuries."
                    },
                    "videos": [
                        "https://www.youtube.com/watch?v=7zPiD3ibvCc",
                        "https://www.youtube.com/watch?v=7zPiD3ibvCc",
                        "https://www.youtube.com/watch?v=7zPiD3ibvCc"
                    ]
                },
                "muscle_gain": {
                    "Bodyweight Strength Training": {
                        "Frequency": "4 days a week",
                        "Exercises": "Push-ups, pull-ups, squats, and planks.",
                        "Reps/Sets": "4 sets of 8-12 reps.",
                        "Goal": "Build foundational muscle strength."
                    },
                    "Basic Weight Lifting": {
                        "Frequency": "3 days a week",
                        "Exercises": "Dumbbell bench press, bicep curls, tricep dips.",
                        "Reps/Sets": "3 sets of 8-10 reps.",
                        "Goal": "Increase muscle mass with light weights."
                    },
                    "videos": [
                        "https://www.youtube.com/watch?v=HUx7GTeSoJw",
                        "https://www.youtube.com/watch?v=meQwgZzVczc"
                    ]
                },
                "flexibility": {
                    "Daily Stretching Routine": {
                        "Frequency": "7 days a week",
                        "Duration": "15-20 minutes",
                        "Focus": "Full-body stretches focusing on major muscle groups."
                    },
                    "Yoga": {
                        "Frequency": "3 days a week",
                        "Duration": "30 minutes",
                        "Focus": "Improve flexibility and reduce stress."
                    },
                    "videos": [
                        "https://www.youtube.com/watch?v=v7AYKMP6rOE",
                        "https://www.youtube.com/watch?v=VaoV1PrYft4"
                    ]
                },
                "general_fitness": {
                    "Light Aerobics": {
                        "Frequency": "4 days a week",
                        "Duration": "30 minutes",
                        "Focus": "Improve overall cardiovascular health."
                    },
                    "Mixed Bodyweight and Flexibility": {
                        "Frequency": "3 days a week",
                        "Exercises": "Combination of squats, lunges, push-ups, and stretching.",
                        "Reps/Sets": "3 sets of 12-15 reps.",
                        "Goal": "Balance strength and flexibility."
                    },
                    "videos": [
                        "https://www.youtube.com/watch?v=MLqgL81V87A",
                        "https://www.youtube.com/watch?v=X3-gKPNyrTA"
                    ]
                },
                "stress_relief": {
                    "Mindful Walking": {
                        "Frequency": "5 days a week",
                        "Duration": "20-30 minutes",
                        "Focus": "Combine light exercise with mindfulness for stress reduction."
                    },
                    "Gentle Yoga": {
                        "Frequency": "3 days a week",
                        "Duration": "30 minutes",
                        "Focus": "Reduce stress and tension in the body."
                    },
                    "Breathing Exercises": {
                        "Frequency": "Daily",
                        "Duration": "5-10 minutes",
                        "Focus": "Practice deep breathing to reduce anxiety and stress."
                    },
                    "videos": [
                        "https://www.youtube.com/watch?v=aNXKjGFUlMs",
                        "https://www.youtube.com/watch?v=SEfs5TJZ6Nk"
                    ]
                }
            },
            "lightly_active": {
                "weight_loss": {
                    "Cardio Workouts": {
                        "Frequency": "4-5 days a week",
                        "Duration": "30-40 minutes",
                        "Intensity": "Brisk walking, jogging, cycling.",
                        "Goal": "Burn calories and improve cardiovascular health."
                    },
                    "Strength Training": {
                        "Frequency": "3 days a week",
                        "Exercises": "Weightlifting with light weights, resistance bands.",
                        "Reps/Sets": "3 sets of 12-15 reps.",
                        "Goal": "Increase muscle mass and metabolism."
                    },
                    "videos": [
                        "https://www.youtube.com/watch?v=sVdQ2q8ZStI",
                        "https://www.youtube.com/watch?v=UFP5xIk2RhA"
                    ]
                },
                "muscle_gain": {
                    "Strength and Hypertrophy": {
                        "Frequency": "4 days a week",
                        "Exercises": "Compound movements like squats, deadlifts, bench press.",
                        "Reps/Sets": "4 sets of 8-10 reps.",
                        "Goal": "Build muscle mass."
                    },
                    "high_protein Diet": {
                        "Advice": "Increase protein intake to support muscle growth.",
                        "Foods": "Chicken, fish, eggs, legumes, protein shakes."
                    },
                    "videos": [
                        "https://www.youtube.com/watch?v=7zPiD3ibvCc",
                        "https://www.youtube.com/watch?v=HUx7GTeSoJw"
                    ]
                },
                "flexibility": {
                    "Dynamic Stretching": {
                        "Frequency": "Before workouts",
                        "Duration": "10 minutes",
                        "Focus": "Prepare muscles and joints for exercise."
                    },
                    "Post-Workout Stretching": {
                        "Frequency": "After each workout",
                        "Duration": "10-15 minutes",
                        "Focus": "Improve flexibility and reduce muscle tightness."
                    },
                    "videos": [
                        "https://www.youtube.com/watch?v=KIxb-y3CaFk",
                        "https://www.youtube.com/watch?v=uHYjN6Ou2-M"
                    ]
                },
                "general_fitness": {
                    "Mixed Cardio and Strength": {
                        "Frequency": "4 days a week",
                        "Exercises": "Combination of running, cycling, and weightlifting.",
                        "Duration": "40-50 minutes",
                        "Goal": "Maintain overall fitness and health."
                    },
                    "Active Recovery": {
                        "Frequency": "1-2 days a week",
                        "Activities": "Light activities like walking, yoga.",
                        "Goal": "Promote recovery while staying active."
                    },
                    "videos": [
                        "https://www.youtube.com/watch?v=e3-zpBc_hg8",
                        "https://www.youtube.com/watch?v=iZ-PywX9roo"
                    ]
                },
                "stress_relief": {
                    "Yoga for Stress Relief": {
                        "Frequency": "3 days a week",
                        "Duration": "30 minutes",
                        "Focus": "Relaxation and stress management."
                    },
                    "Breathing and Meditation": {
                        "Frequency": "Daily",
                        "Duration": "10-15 minutes",
                        "Focus": "Reduce stress and anxiety."
                    },
                    "videos": [
                        "https://www.youtube.com/watch?v=rYlLXrKhRAc",
                        "https://www.youtube.com/watch?v=MLqgL81V87A"
                    ]
                }
            },
            "moderately_active": {
                "weight_loss": {
                    "High-Intensity Cardio": {
                        "Frequency": "5 days a week",
                        "Duration": "30-40 minutes",
                        "Intensity": "High-intensity interval training (HIIT), running.",
                        "Goal": "Maximize calorie burn and fat loss."
                    },
                    "Strength Training": {
                        "Frequency": "4 days a week",
                        "Exercises": "Weightlifting with moderate to heavy weights.",
                        "Reps/Sets": "4 sets of 8-10 reps.",
                        "Goal": "Build lean muscle to boost metabolism."
                    },
                    "videos": [
                        "https://www.youtube.com/watch?v=UFP5xIk2RhA",
                        "https://www.youtube.com/watch?v=meQwgZzVczc"
                    ]
                },
                "muscle_gain": {
                    "Strength and Hypertrophy": {
                        "Frequency": "4-5 days a week",
                        "Exercises": "Heavy weightlifting with compound movements.",
                        "Reps/Sets": "4-5 sets of 6-8 reps.",
                        "Goal": "Increase muscle size and strength."
                    },
                    "Protein and Supplement Advice": {
                        "Advice": "Consider protein supplements and a high-protein diet.",
                        "Supplements": "Whey protein, BCAAs, creatine."
                    },
                    "videos": [
                        "https://www.youtube.com/watch?v=KIxb-y3CaFk",
                        "https://www.youtube.com/watch?v=HUx7GTeSoJw"
                    ]
                },
                "flexibility": {
                    "Advanced Stretching": {
                        "Frequency": "Daily",
                        "Duration": "15-20 minutes",
                        "Focus": "Improve flexibility for better performance."
                    },
                    "Yoga and Mobility Work": {
                        "Frequency": "3 days a week",
                        "Duration": "30 minutes",
                        "Focus": "Enhance flexibility and mobility."
                    },
                    "videos": [
                        "https://www.youtube.com/watch?v=3jiL6bhR64Y",
                        "https://www.youtube.com/watch?v=KIxb-y3CaFk"
                    ]
                },
                "general_fitness": {
                    "Balanced Workout Routine": {
                        "Frequency": "5 days a week",
                        "Exercises": "Mix of cardio, strength training, and flexibility.",
                        "Duration": "60 minutes",
                        "Goal": "Maintain overall fitness and health."
                    },
                    "Active Recovery": {
                        "Frequency": "1-2 days a week",
                        "Activities": "Gentle activities like swimming, cycling.",
                        "Goal": "Promote recovery and prevent burnout."
                    },
                    "videos": [
                        "https://www.youtube.com/watch?v=1DYH5ud3zHo",
                        "https://www.youtube.com/watch?v=UFP5xIk2RhA"
                    ]
                },
                "stress_relief": {
                    "High-Intensity Yoga": {
                        "Frequency": "3 days a week",
                        "Duration": "30 minutes",
                        "Focus": "Combine exercise with relaxation techniques."
                    },
                    "Meditation and Mindfulness": {
                        "Frequency": "Daily",
                        "Duration": "15 minutes",
                        "Focus": "Manage stress and enhance mental well-being."
                    },
                    "videos": [
                        "https://www.youtube.com/watch?v=aNXKjGFUlMs",
                        "https://www.youtube.com/watch?v=X3-gKPNyrTA"
                    ]
                }
            },
            "very_active": {
                "weight_loss": {
                    "High-Intensity Interval Training (HIIT)": {
                        "Frequency": "5-6 days a week",
                        "Duration": "20-30 minutes",
                        "Intensity": "Short bursts of intense exercise followed by rest.",
                        "Goal": "Maximize fat loss and improve cardiovascular fitness."
                    },
                    "Strength and Conditioning": {
                        "Frequency": "4-5 days a week",
                        "Exercises": "Combination of heavy lifting and metabolic conditioning.",
                        "Reps/Sets": "4-5 sets of 6-8 reps.",
                        "Goal": "Increase muscle mass while burning fat."
                    },
                    "videos": [
                        "https://www.youtube.com/watch?v=4o2Bqdm6wm8",
                        "https://www.youtube.com/watch?v=kjdXYdj2X2s"
                    ]
                },
                "muscle_gain": {
                    "Advanced Strength Training": {
                        "Frequency": "5-6 days a week",
                        "Exercises": "Heavy compound movements, advanced techniques like drop sets.",
                        "Reps/Sets": "4-6 sets of 4-6 reps.",
                        "Goal": "Maximize muscle growth and strength."
                    },
                    "Nutritional Advice": {
                        "Advice": "Ensure high protein intake and consider supplements.",
                        "Supplements": "Creatine, protein powder, BCAAs."
                    },
                    "videos": [
                        "https://www.youtube.com/watch?v=HUx7GTeSoJw",
                        "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
                    ]
                },
                "flexibility": {
                    "Advanced Flexibility Routine": {
                        "Frequency": "Daily",
                        "Duration": "20-30 minutes",
                        "Focus": "Increase range of motion and recovery."
                    },
                    "Yoga for Athletes": {
                        "Frequency": "3 days a week",
                        "Duration": "30 minutes",
                        "Focus": "Enhance flexibility and reduce muscle soreness."
                    },
                    "videos": [
                        "https://www.youtube.com/watch?v=KIxb-y3CaFk",
                        "https://www.youtube.com/watch?v=VaoV1PrYft4"
                    ]
                },
                "general_fitness": {
                    "Intensive Workout Programs": {
                        "Frequency": "6 days a week",
                        "Exercises": "Advanced cardio, strength, and flexibility workouts.",
                        "Duration": "60-90 minutes",
                        "Goal": "Maintain peak physical condition and performance."
                    },
                    "Active Recovery and Mobility": {
                        "Frequency": "1 day a week",
                        "Activities": "Light activities, stretching, foam rolling.",
                        "Goal": "Aid recovery and maintain flexibility."
                    },
                    "videos": [
                        "https://www.youtube.com/watch?v=UFP5xIk2RhA",
                        "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
                    ]
                },
                "stress_relief": {
                    "High-Intensity Yoga and Meditation": {
                        "Frequency": "3 days a week",
                        "Duration": "30 minutes",
                        "Focus": "Combine high-intensity exercise with relaxation."
                    },
                    "Mindfulness and Relaxation Techniques": {
                        "Frequency": "Daily",
                        "Duration": "15-20 minutes",
                        "Focus": "Manage stress and improve mental well-being."
                    },
                    "videos": [
                        "https://www.youtube.com/watch?v=aNXKjGFUlMs",
                        "https://www.youtube.com/watch?v=X3-gKPNyrTA"
                    ]
                }
            }
}
            
            # Return recommendations based on the activity level
            if activity_level in recommendations:
                return JsonResponse(recommendations[activity_level], safe=False)
            else:
                return JsonResponse({"error": "Activity level not supported"}, status=400)
            
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    
        except Exception as e:
        # Log the exception if necessary (for debugging purposes)
            return JsonResponse({"error": "An unexpected error occurred"}, status=500)
    
        finally:
        # Any cleanup code (if needed) goes here
            print("Request processing complete")
'''

'''
first api for diet plan
@csrf_exempt
def get_diet_recommendations(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            dietary_preference = data.get('dietary_preference')
            health_condition = data.get('health_condition')
            medical_history = data.get('medical_history')

            # Sample diet recommendations
            recommendations = {
                "vegetarian": {
                    "diabetes": {
                        "name": "Low Glycemic vegetarian Diet",
                        "description": "A vegetarian diet focusing on low glycemic index foods to help manage blood sugar levels. Includes plenty of whole grains, legumes, vegetables, and fruits.",
                        "meals": {
                            "Breakfast": "Oatmeal with berries and a handful of nuts.",
                            "Lunch": "Quinoa salad with chickpeas, cucumber, and olive oil dressing.",
                            "Dinner": "Stir-fried tofu with mixed vegetables.",
                            "Snacks": "Apple slices with almond butter."
                        },
                        "videos": [
                            "https://www.youtube.com/watch?v=DiabetesDiet",
                            "https://www.youtube.com/watch?v=VegetarianRecipes"
                        ]
                    },
                    "heart_disease": {
                        "name": "Heart-Healthy vegetarian Diet",
                        "description": "A vegetarian diet designed to reduce cholesterol and improve heart health.",
                        "meals": {
                            "Breakfast": "Smoothie with spinach, banana, and flax seeds.",
                            "Lunch": "Lentil soup with a side of whole-grain bread.",
                            "Dinner": "Grilled portobello mushrooms with quinoa and steamed broccoli.",
                            "Snacks": "Carrot sticks with hummus."
                        },
                        "videos": [
                            "https://www.youtube.com/watch?v=HeartDiet",
                            "https://www.youtube.com/watch?v=VegetarianHeart"
                        ]
                    }
                },
                "vegan": {
                    "cancer": {
                        "name": "Anti-cancer vegan Diet",
                        "description": "A vegan diet rich in antioxidants and fiber to support cancer prevention and recovery.",
                        "meals": {
                            "Breakfast": "Green smoothie with kale, berries, and chia seeds.",
                            "Lunch": "Quinoa and black bean salad with avocado.",
                            "Dinner": "Stuffed bell peppers with lentils and vegetables.",
                            "Snacks": "Mixed nuts and a piece of fruit."
                        },
                        "videos": [
                            "https://www.youtube.com/watch?v=VeganCancer",
                            "https://www.youtube.com/watch?v=AntiCancerDiet"
                        ]
                    },
                    "allergy": {
                        "name": "Allergy-Friendly vegan Diet",
                        "description": "A vegan diet free from common allergens like nuts, gluten, and soy.",
                        "meals": {
                            "Breakfast": "Buckwheat pancakes with fresh fruit.",
                            "Lunch": "Sweet potato and chickpea bowl with tahini dressing.",
                            "Dinner": "Zucchini noodles with tomato sauce and roasted vegetables.",
                            "Snacks": "Rice cakes with avocado."
                        },
                        "videos": [
                            "https://www.youtube.com/watch?v=VeganAllergy",
                            "https://www.youtube.com/watch?v=AllergyFriendly"
                        ]
                    }
                },
                "gluten_free": {
                    "asthma": {
                        "name": "Anti-Inflammatory gluten_free Diet",
                        "description": "A gluten-free diet that includes anti-inflammatory foods to help reduce asthma symptoms.",
                        "meals": {
                            "Breakfast": "Scrambled eggs with spinach and avocado.",
                            "Lunch": "Brown rice salad with black beans, corn, and cilantro-lime dressing.",
                            "Dinner": "Grilled salmon with sweet potato and green beans.",
                            "Snacks": "Blueberries with a handful of walnuts."
                        },
                        "videos": [
                            "https://www.youtube.com/watch?v=AsthmaDiet",
                            "https://www.youtube.com/watch?v=GlutenFreeRecipes"
                        ]
                    },
                    "thyroid": {
                        "name": "thyroid Support gluten_free Diet",
                        "description": "A gluten-free diet designed to support thyroid function with nutrient-rich foods.",
                        "meals": {
                            "Breakfast": "Greek yogurt with chia seeds and a few slices of cucumber.",
                            "Lunch": "Grilled chicken breast with a side of steamed asparagus.",
                            "Dinner": "Baked cod with cauliflower mash and sautéed spinach.",
                            "Snacks": "Brazil nuts (rich in selenium)."
                        },
                        "videos": [
                            "https://www.youtube.com/watch?v=ThyroidDiet",
                            "https://www.youtube.com/watch?v=GlutenFreeSupport"
                        ]
                    }
                },
                "low_carb": {
                    "kidney_disease": {
                        "name": "Kidney-Friendly low_carb Diet",
                        "description": "A low-carb diet designed to support kidney health while managing carbohydrate intake.",
                        "meals": {
                            "Breakfast": "Scrambled eggs with bell peppers and onions.",
                            "Lunch": "Turkey and avocado lettuce wraps.",
                            "Dinner": "Grilled chicken with steamed broccoli and cauliflower rice.",
                            "Snacks": "Cucumber slices with hummus."
                        },
                        "videos": [
                            "https://www.youtube.com/watch?v=KidneyDiet",
                            "https://www.youtube.com/watch?v=LowCarbRecipes"
                        ]
                    },
                    "heart_disease": {
                        "name": "Heart-Healthy low_carb Diet",
                        "description": "A low-carb diet rich in heart-healthy fats and lean proteins.",
                        "meals": {
                            "Breakfast": "Smoothie with avocado, spinach, and protein powder.",
                            "Lunch": "Grilled salmon with a side of mixed greens and olive oil dressing.",
                            "Dinner": "Roasted chicken with asparagus and a side of mashed cauliflower.",
                            "Snacks": "Nuts and seeds with a piece of fruit."
                        },
                        "videos": [
                            "https://www.youtube.com/watch?v=HeartLowCarb",
                            "https://www.youtube.com/watch?v=LowCarbHeart"
                        ]
                    }
                },
                "high_protein": {
                    "previous_surgeries": {
                        "name": "Post-Surgery high_protein Diet",
                        "description": "A high-protein diet to support recovery and tissue repair after surgery.",
                        "meals": {
                            "Breakfast": "Scrambled eggs with turkey bacon.",
                            "Lunch": "Grilled chicken breast with quinoa and steamed vegetables.",
                            "Dinner": "Baked fish with sweet potato and green beans.",
                            "Snacks": "Greek yogurt with a handful of almonds."
                        },
                        "videos": [
                            "https://www.youtube.com/watch?v=PostSurgeryDiet",
                            "https://www.youtube.com/watch?v=HighProteinRecovery"
                        ]
                    },
                    "chronic_illnesses": {
                        "name": "Chronic Illness Support high_protein Diet",
                        "description": "A diet rich in protein to support overall health and manage chronic illnesses.",
                        "meals": {
                            "Breakfast": "Protein smoothie with whey protein, spinach, and berries.",
                            "Lunch": "Lean beef or turkey with a side of roasted vegetables.",
                            "Dinner": "Chicken stir-fry with mixed vegetables and quinoa.",
                            "Snacks": "Cottage cheese with sliced peaches."
                        },
                        "videos": [
                            "https://www.youtube.com/watch?v=ChronicIllnessDiet",
                            "https://www.youtube.com/watch?v=HighProteinHealth"
                        ]
                    }
                },
                "diabetic_friendly": {
                    "medications": {
                        "name": "diabetic_friendly Diet for Medication Management",
                        "description": "A diet designed to support blood sugar management while considering medication effects.",
                        "meals": {
                            "Breakfast": "Steel-cut oats with cinnamon and walnuts.",
                            "Lunch": "Chicken and vegetable soup with a side salad.",
                            "Dinner": "Grilled turkey with sautéed spinach and whole-grain pasta.",
                            "Snacks": "Celery sticks with peanut butter."
                        },
                        "videos": [
                            "https://www.youtube.com/watch?v=DiabeticDiet",
                            "https://www.youtube.com/watch?v=MedicationFriendly"
                        ]
                    },
                    "allergies": {
                        "name": "Allergy-Friendly Diabetic Diet",
                        "description": "A diabetic diet tailored to avoid allergens while managing blood sugar levels.",
                        "meals": {
                            "Breakfast": "Quinoa porridge with almond milk and berries.",
                            "Lunch": "Grilled chicken with a side of roasted Brussels sprouts.",
                            "Dinner": "Baked salmon with steamed green beans and brown rice.",
                            "Snacks": "Sliced apples with sunflower seed butter."
                        },
                        "videos": [
                            "https://www.youtube.com/watch?v=DiabeticAllergy",
                            "https://www.youtube.com/watch?v=AllergyDiabetic"
                        ]
                    }
                }
            }

            # Return recommendations based on the user's dietary preference, health condition, and medical history
            if dietary_preference in recommendations:
                if health_condition in recommendations[dietary_preference]:
                    return JsonResponse(recommendations[dietary_preference][health_condition], safe=False)
                else:
                    return JsonResponse({"error": "Health condition not supported"}, status=400)
            else:
                return JsonResponse({"error": "Dietary preference not supported"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
'''


# dietery_preference and health_condtion api
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json

@csrf_exempt
def get_diet_recommendations(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            dietary_preference = data.get('dietary_preference')
            health_condition = data.get('health_condition')
            
            # Detailed diet recommendations
            dietary_recommendations = {
                "vegetarian": {
                    "Breakfast": [
                        "Smoothie Bowl: Spinach, banana, almond milk, protein powder, topped with berries, nuts, seeds.",
                        "Overnight Oats: Rolled oats, almond milk, chia seeds, topped with fruits and nuts.",
                        "Avocado Toast: Whole-grain toast with mashed avocado, cherry tomatoes.",
                        "Greek Yogurt Parfait: Greek yogurt, granola, fresh berries, nuts."
                    ],
                    "Lunch": [
                        "Quinoa Salad: Quinoa, black beans, corn, tomatoes, avocado, lime dressing.",
                        "Chickpea Salad: Mashed chickpeas, vegan mayo, celery, onion, lettuce.",
                        "Stuffed Bell Peppers: Bell peppers filled with rice, chickpeas, spinach, feta.",
                        "Sweet Potato Bowl: Roasted sweet potatoes, black beans, avocado, salsa, Greek yogurt."
                    ],
                    "Dinner": [
                        "Vegetable Stir-Fry: Mixed veggies, tofu, soy sauce, over brown rice.",
                        "Lentil Soup: Lentils, carrots, celery, tomatoes, spinach.",
                        "Vegetable Curry: Mixed veggies, chickpeas, coconut milk, served with rice.",
                        "Spaghetti Marinara: Whole-grain spaghetti with marinara sauce, side salad."
                    ],
                    "Snacks": [
                        "Apple Slices with Almond Butter",
                        "Carrot and Celery Sticks with Hummus",
                        "Chia Pudding: Chia seeds soaked in almond milk, topped with fruit.",
                        "Trail Mix: Nuts, seeds, dried fruit.",
                        "Greek Yogurt with Fruit",
                        "Nuts and Seeds"
                    ]
                },
                "vegan": {
                    "Breakfast": [
                        "Smoothie Bowl: Kale, banana, almond milk, chia seeds, topped with berries and granola.",
                        "Chia Pudding: Chia seeds soaked in coconut milk, topped with fresh fruit and nuts.",
                        "vegan Pancakes: Made with almond milk, served with maple syrup and fruit.",
                        "Avocado Toast: Whole-grain toast with mashed avocado, cherry tomatoes, and a sprinkle of nutritional yeast."
                    ],
                    "Lunch": [
                        "Quinoa Salad: Quinoa, black beans, corn, avocado, cherry tomatoes, lime dressing.",
                        "vegan Wrap: Whole-grain wrap with hummus, shredded carrots, cucumber, spinach, and avocado.",
                        "Stuffed Sweet Potatoes: Sweet potatoes filled with black beans, corn, avocado, and salsa.",
                        "vegan Buddha Bowl: Brown rice, roasted chickpeas, mixed vegetables, tahini dressing."
                    ],
                    "Dinner": [
                        "vegan Stir-Fry: Mixed vegetables, tofu, soy sauce, served over rice or noodles.",
                        "Lentil Curry: Lentils, coconut milk, tomatoes, and mixed spices, served with rice.",
                        "vegan Chili: Beans, tomatoes, bell peppers, onions, and spices.",
                        "Stuffed Bell Peppers: Bell peppers filled with quinoa, black beans, corn, and avocado."
                    ],
                    "Snacks": [
                        "Apple Slices with Peanut Butter",
                        "Veggie Sticks with Hummus",
                        "Mixed Nuts and Dried Fruit",
                        "vegan Yogurt with Fruit",
                        "Rice Cakes with Avocado",
                        "Energy Balls: Dates, nuts, seeds, cocoa powder."
                    ]
                },
                "gluten_free": {
                    "Breakfast": [
                        "Greek Yogurt Parfait: Greek yogurt with fresh fruit and gluten-free granola.",
                        "Smoothie: Spinach, banana, almond milk, chia seeds, and berries.",
                        "gluten_free Oatmeal: Cooked with almond milk, topped with nuts, seeds, and fresh fruit.",
                        "Egg Muffins: Eggs baked with spinach, bell peppers, and onions."
                    ],
                    "Lunch": [
                        "Quinoa Salad: Quinoa, chickpeas, cucumber, cherry tomatoes, and olive oil dressing.",
                        "gluten_free Wrap: Wrap with hummus, avocado, shredded carrots, and mixed greens.",
                        "Stuffed Sweet Potatoes: Sweet potatoes filled with black beans, corn, and salsa.",
                        "Grilled Chicken Salad: Mixed greens, grilled chicken, avocado, and a balsamic vinaigrette."
                    ],
                    "Dinner": [
                        "Grilled Salmon: Served with quinoa and steamed broccoli.",
                        "Chicken Stir-Fry: Chicken with mixed vegetables, gluten-free soy sauce, and rice.",
                        "Zucchini Noodles: With marinara sauce and roasted vegetables.",
                        "gluten_free Pasta: Tossed with tomato sauce, spinach, and grilled chicken."
                    ],
                    "Snacks": [
                        "Apple Slices with Almond Butter",
                        "gluten_free Rice Cakes with Avocado",
                        "Nuts and Seeds Mix",
                        "Carrot and Cucumber Sticks with Hummus",
                        "Fresh Fruit or Fruit Smoothie",
                        "gluten_free Energy Bars"
                    ]
                },
                "low_carb": {
                    "Breakfast": [
                        "Avocado Eggs: Baked eggs in avocado halves.",
                        "Greek Yogurt with Nuts: Unsweetened Greek yogurt with almonds or walnuts.",
                        "Smoothie: Spinach, protein powder, almond milk, and a small handful of berries.",
                        "Chia Seed Pudding: Made with chia seeds, almond milk, and a few slices of fruit."
                    ],
                    "Lunch": [
                        "Grilled Chicken Salad: Mixed greens with grilled chicken, avocado, and olive oil dressing.",
                        "Lettuce Wraps: Turkey or chicken with avocado, shredded veggies, and a low-carb sauce.",
                        "Zucchini Noodles: Tossed with pesto sauce and grilled shrimp.",
                        "Cauliflower Rice Bowl: Cauliflower rice with stir-fried veggies and a protein of choice."
                    ],
                    "Dinner": [
                        "Baked Salmon: Served with roasted asparagus and a side salad.",
                        "Stuffed Bell Peppers: Filled with ground beef, cauliflower rice, and cheese.",
                        "Chicken Thighs: Roasted with rosemary and served with sautéed spinach.",
                        "Beef Stir-Fry: Strips of beef with bell peppers, broccoli, and a low-carb sauce."
                    ],
                    "Snacks": [
                        "Nuts and Seeds: Almonds, walnuts, or pumpkin seeds.",
                        "Cheese Slices or Sticks",
                        "Cucumber Slices with Hummus",
                        "Hard-Boiled Eggs",
                        "Celery Sticks with Cream Cheese"
                    ]
                },
                "high_protein": {
                    "Breakfast": [
                        "Egg White Omelette: With spinach, tomatoes, and mushrooms.",
                        "Greek Yogurt: Plain, topped with a few nuts or seeds.",
                        "Protein Smoothie: Whey or plant-based protein powder, almond milk, spinach, and berries.",
                        "Cottage Cheese: With a slice of whole-grain toast or fruit."
                    ],
                    "Lunch": [
                        "Grilled Chicken Breast: Served with quinoa and mixed vegetables.",
                        "Tuna Salad: Tuna mixed with Greek yogurt, celery, and a side of leafy greens.",
                        "Turkey and Avocado Wrap: Sliced turkey breast with avocado, lettuce, and tomato in a low-carb wrap.",
                        "Lentil Soup: High in protein and fiber, served with a side of mixed greens."
                    ],
                    "Dinner": [
                        "Baked Cod: With a side of steamed broccoli and sweet potato.",
                        "Beef Stir-Fry: Lean beef strips with bell peppers, onions, and snap peas.",
                        "Chicken Breast: Grilled or baked with a side of roasted Brussels sprouts and brown rice.",
                        "Tofu Stir-Fry: Tofu with mixed vegetables and a low-sodium soy sauce."
                    ],
                    "Snacks": [
                        "Hard-Boiled Eggs",
                        "Protein Bars: Low sugar, high protein.",
                        "Edamame: Steamed and lightly salted.",
                        "Jerky: Beef or turkey, without added sugars.",
                        "Hummus: With raw veggies like carrots or bell peppers."
                    ]
                },
                "diabetic_friendly": {
                    "Breakfast": [
                        "Steel-Cut Oats: Cooked with cinnamon and topped with a few nuts or seeds.",
                        "Greek Yogurt: Plain, with a small portion of fresh berries.",
                        "Eggs: Scrambled with vegetables like spinach, tomatoes, and bell peppers.",
                        "Chia Seed Pudding: Made with unsweetened almond milk and a small portion of fruit."
                    ],
                    "Lunch": [
                        "Grilled Chicken Salad: With mixed greens, cucumbers, tomatoes, and a light vinaigrette.",
                        "Lentil Soup: Rich in fiber and protein, paired with a side of non-starchy vegetables.",
                        "Quinoa Salad: With black beans, corn, bell peppers, and a squeeze of lime.",
                        "Turkey Wrap: In a whole grain or low-carb wrap, with avocado, lettuce, and tomato."
                    ],
                    "Dinner": [
                        "Baked Salmon: Served with a side of steamed green beans and a small portion of quinoa.",
                        "Stir-Fried Tofu: With mixed vegetables like broccoli, bell peppers, and snap peas.",
                        "Grilled Turkey: With a side of roasted Brussels sprouts and sweet potato.",
                        "Vegetable Stir-Fry: With a mix of non-starchy vegetables and a lean protein source like chicken or tofu."
                    ],
                    "Snacks": [
                        "Raw Veggies: Like carrot sticks or bell pepper slices with hummus.",
                        "Nuts: A small handful of almonds or walnuts.",
                        "Apple Slices: With a thin spread of almond butter.",
                        "Cottage Cheese: With a few fresh berries or sliced cucumber."
                    ]
                }
            }

            health_conditions = {
                "asthma": {
                    "Eat More": [
                        "Anti-Inflammatory Foods: Apples, berries, spinach, fatty fish (salmon).",
                        "Antioxidant-Rich Foods: Blueberries, oranges, green tea.",
                        "Magnesium-Rich Foods: Spinach, pumpkin seeds, brown rice.",
                        "Hydrating Foods: Water, herbal teas (chamomile)."
                    ],
                    "Avoid": [
                        "Processed Foods: High in preservatives.",
                        "Sugary Foods: Can increase inflammation.",
                        "Sulfites: Found in some dried fruits and wine."
                    ],
                    "Include": [
                        "Omega-3 Fatty Acids: Fish like salmon, flaxseeds.",
                        "Anti-Inflammatory Spices: Turmeric, ginger."
                    ],
                    "Sample Meal Plan": [
                        "Breakfast: Spinach and berry smoothie.",
                        "Lunch: Quinoa salad with mixed vegetables.",
                        "Snack: Almonds and apple.",
                        "Dinner: Baked salmon with broccoli and sweet potato."
                    ]
                },
                "diabetes": {
                    "Eat More": [
                        "Non-Starchy Vegetables: Leafy greens, broccoli, bell peppers.",
                        "Whole Grains: Brown rice, quinoa.",
                        "Lean Proteins: Chicken, tofu, legumes.",
                        "Healthy Fats: Avocado, nuts, olive oil.",
                        "Low-Glycemic Fruits: Apples, berries, pears."
                    ],
                    "Limit": [
                        "Refined Carbohydrates: White bread, pastries.",
                        "Sugary Foods: Sweets, sugary drinks.",
                        "High-Sodium Foods: Processed snacks, canned soups."
                    ],
                    "Include": [
                        "Fiber: Whole grains, vegetables.",
                        "Protein: Lean meats, legumes.",
                        "Healthy Fats: Avocados, nuts."
                    ],
                    "Sample Meal Plan": [
                        "Breakfast: Steel-cut oats with berries.",
                        "Lunch: Grilled chicken salad with mixed greens.",
                        "Snack: Greek yogurt with a few nuts.",
                        "Dinner: Baked salmon with quinoa and green beans."
                    ]
                },
                "heart_disease": {
                    "Eat More": [
                        "Fruits & Vegetables: Apples, bananas, leafy greens.",
                        "Whole Grains: Oats, barley.",
                        "Lean Proteins: Chicken, fish.",
                        "Low-Fat Dairy: Skim milk, yogurt.",
                        "Potassium-Rich Foods: Bananas, sweet potatoes, tomatoes."
                    ],
                    "Limit": [
                        "Sodium: Salt, processed foods.",
                        "Saturated Fats: Red meat, butter.",
                        "Alcohol: Limit intake."
                    ],
                    "Include": [
                        "Potassium: Helps counteract the effects of sodium.",
                        "Magnesium: Found in nuts, seeds, and leafy greens.",
                        "Calcium: Low-fat dairy or fortified alternatives."
                    ],
                    "Sample Meal Plan": [
                        "Breakfast: Smoothie with spinach, banana, and almond milk.",
                        "Lunch: Salad with grilled chicken, mixed greens, and a lemon vinaigrette.",
                        "Snack: Apple slices with almond butter.",
                        "Dinner: Baked cod with roasted sweet potatoes and steamed broccoli."
                    ]
                },
                "thyroid": {
                    "Eat More": [
                        "Oats: High in soluble fiber.",
                        "Nuts: Almonds, walnuts.",
                        "Fatty Fish: Salmon, mackerel.",
                        "Fruits & Vegetables: Apples, berries, leafy greens.",
                        "Legumes: Beans, lentils."
                    ],
                    "Limit": [
                        "Saturated Fats: Red meat, butter.",
                        "Trans Fats: Processed foods.",
                        "Cholesterol-Rich Foods: Eggs, full-fat dairy."
                    ],
                    "Include": [
                        "Fiber: Soluble fiber from oats, fruits, and vegetables.",
                        "Omega-3 Fatty Acids: From fatty fish.",
                        "Plant Sterols: Found in fortified foods."
                    ],
                    "Sample Meal Plan": [
                        "Breakfast: Oatmeal with fresh berries.",
                        "Lunch: Lentil soup with a side of mixed greens.",
                        "Snack: A handful of almonds.",
                        "Dinner: Grilled salmon with quinoa and steamed vegetables."
                    ]
                },
                "cancer": {
                    "Eat More": [
                        "Fruits & Vegetables: Especially colorful varieties like berries, carrots, and broccoli.",
                        "Whole Grains: Brown rice, quinoa, whole wheat bread.",
                        "Lean Proteins: Chicken, turkey, tofu, legumes.",
                        "Nuts & Seeds: Flaxseeds, chia seeds, almonds.",
                        "Fatty Fish: Salmon, mackerel, sardines rich in omega-3 fatty acids."
                    ],
                    "Limit": [
                        "Processed Foods: High in sodium, unhealthy fats, and sugars.",
                        "Red Meat: Limit consumption to reduce cancer risk.",
                        "Sugary Drinks: Soda, sugary juices, and energy drinks.",
                        "Alcohol: Limit or avoid alcohol consumption.",
                        "High-Fat Dairy: Full-fat milk, cheese, and yogurt."
                    ],
                    "Include": [
                        "Antioxidants: Found in berries, green tea, and nuts.",
                        "Fiber: From whole grains, fruits, and vegetables.",
                        "Omega-3 Fatty Acids: From fatty fish and flaxseeds.",
                        "Cruciferous Vegetables: Broccoli, cauliflower, Brussels sprouts.",
                        "Herbs & Spices: Turmeric, garlic, and ginger for their anti-inflammatory properties."
                    ],
                    "Sample Meal Plan": [
                        "Breakfast: Smoothie with spinach, banana, and flaxseeds.",
                        "Lunch: Quinoa salad with mixed vegetables and grilled chicken.",
                        "Snack: A handful of berries and a small serving of almonds.",
                        "Dinner: Baked salmon with a side of steamed broccoli and brown rice."
                    ]
                },
                "kidney_disease": {
                    "Eat More": [
                        "Lean Proteins: Chicken, turkey, tofu, and legumes in controlled portions.",
                        "Fruits & Vegetables: Apples, berries, bell peppers, and leafy greens.",
                        "Whole Grains: Brown rice, quinoa, and whole wheat bread.",
                        "Healthy Fats: Olive oil, avocados, and nuts in moderation.",
                        "Low-Potassium Foods: Cabbage, cauliflower, and cucumbers."
                    ],
                    "Limit": [
                        "Sodium: Salt, processed foods, and canned soups.",
                        "Potassium: Bananas, oranges, potatoes, and tomatoes.",
                        "Phosphorus: Dairy products, nuts, and processed foods.",
                        "Red Meat: Limit consumption to reduce strain on kidneys.",
                        "Sugary Foods: Limit intake of sweets and sugary beverages."
                    ],
                    "Include": [
                        "Low-Sodium Seasonings: Herbs and spices like garlic, basil, and rosemary.",
                        "Hydration: Adequate water intake as advised by a healthcare provider.",
                        "High-Quality Carbohydrates: Whole grains for energy and fiber.",
                        "Omega-3 Fatty Acids: From fatty fish like salmon, if permitted by diet.",
                        "Calcium-Rich Foods: Low-phosphorus options like almond milk or fortified plant-based milks."
                    ],
                    "Sample Meal Plan": [
                        "Breakfast: Oatmeal with fresh berries and a splash of almond milk.",
                        "Lunch: Grilled chicken breast with quinoa and steamed green beans.",
                        "Snack: A small apple with a handful of unsalted almonds.",
                        "Dinner: Baked cod with a side of cauliflower rice and sautéed spinach."
                    ]
                }
            }
            
            combined_recommendations = {
                "vegetarian": {
                    "diabetes": {
                        "Breakfast": [
                            "Chia Pudding: Chia seeds soaked in almond milk with berries and a touch of honey.",
                            "Greek Yogurt Parfait: Unsweetened Greek yogurt layered with nuts, seeds, and a small amount of fresh fruit."
                        ],
                        "Lunch": [
                            "Quinoa & Black Bean Salad: Quinoa, black beans, corn, bell peppers, avocado, and a lime-cilantro dressing.",
                            "Vegetable & Hummus Wrap: Whole wheat wrap filled with hummus, spinach, shredded carrots, cucumbers, and bell peppers.",
                            
                        ],
                        "Dinner": [
                            "Stuffed Bell Peppers: Bell peppers stuffed with a mixture of quinoa, black beans, corn, tomatoes, and spices.",
                            "Cauliflower Rice Stir-Fry: Cauliflower rice with mixed vegetables, tofu, and a low-sodium soy sauce."
                        ],
                        "Snacks": [
                            "Mixed Nuts: Almonds, walnuts, and pistachios.",
                            "Celery Sticks with Almond Butter"
                        ]
                    },
                    "asthma": {
                        "Breakfast": [
                            "Smoothie Bowl: Spinach, banana, almond milk, and chia seeds, topped with fresh berries and a handful of granola.",
                            "Whole Grain Cereal with Almond Milk: Served with a side of fresh fruit."
                        ],
                        "Lunch": [
                            "Sweet Potato & Black Bean Salad: Roasted sweet potatoes, black beans, corn, red onions, and a cilantro-lime dressing.",
                            "Spinach & Chickpea Salad: Fresh spinach, chickpeas, cucumber, cherry tomatoes, and a balsamic vinaigrette."
                        ],
                        "Dinner": [
                            "Butternut Squash Soup: A creamy soup made with butternut squash, carrots, onions, and ginger.",
                            "Stir-Fried Tofu with Broccoli: Tofu stir-fried with broccoli, bell peppers, and a light soy sauce."
                        ],
                        "Snacks": [
                            "Apple Slices with Almond Butter",
                            "Cucumber Sticks with Hummus"
                        ]
                    },
                    "heart_disease": {
                        "Breakfast": [
                            "Oatmeal with Berries: Rolled oats cooked with almond milk, topped with fresh berries and a sprinkle of flaxseeds.",
                            "Avocado Toast: Whole grain toast with mashed avocado, topped with cherry tomatoes and a drizzle of olive oil."
                        ],
                        "Lunch": [
                            "Lentil & Spinach Salad: Lentils, fresh spinach, cherry tomatoes, red onions, and a lemon-tahini dressing.",
                            "Grilled Vegetable Sandwich: Whole grain bread with grilled zucchini, eggplant, bell peppers, and a smear of hummus."
                        ],
                        "Dinner": [
                            "Vegetable Stew: A hearty stew made with tomatoes, carrots, sweet potatoes, zucchini, and kidney beans.",
                            "Baked Eggplant Parmesan: Slices of eggplant baked with marinara sauce and a small amount of parmesan cheese."
                        ],
                        "Snacks": [
                            "Sliced Apples with Peanut Butter",
                            "Carrot Sticks with Hummus"
                        ]
                    },
                    "thyroid": {
                        "Breakfast": [
                            "Quinoa Porridge: Quinoa cooked with almond milk, topped with walnuts and fresh fruit.",
                            "Berry Smoothie: Blended berries, spinach, flaxseeds, and almond milk."
                        ],
                        "Lunch": [
                            "Kale & White Bean Salad: Kale, white beans, cherry tomatoes, red onions, and a lemon-mustard vinaigrette.",
                            "Roasted Vegetable & Chickpea Wrap: Whole grain wrap with roasted vegetables and chickpeas."
                        ],
                        "Dinner": [
                            "Sweet Potato & Black Bean Chili: A hearty chili made with sweet potatoes, black beans, tomatoes, and spices.",
                            "Stuffed Zucchini Boats: Zucchini stuffed with a mixture of quinoa, tomatoes, and herbs."
                        ],
                        "Snacks": [
                            "Pumpkin Seeds",
                            "Sliced Pear with Almond Butter"
                        ]
                    },
                    "cancer": {
                        "Breakfast": [
                            "Berry Chia Pudding: Chia seeds soaked in coconut milk with a mix of fresh berries.",
                            "Green Smoothie: Spinach, pineapple, banana, and flaxseeds blended with water."
                        ],
                        "Lunch": [
                            "Broccoli & Quinoa Salad: Broccoli, quinoa, chickpeas, bell peppers, and a tahini dressing.",
                            "Vegetable & Lentil Soup: A hearty soup with lentils, carrots, celery, and tomatoes."
                        ],
                        "Dinner": [
                            "Baked Sweet Potato: Served with a side of sautéed spinach and black beans.",
                            "Cauliflower & Chickpea Curry: Cauliflower and chickpeas cooked in a light curry sauce."
                        ],
                        "Snacks": [
                            "Mixed Nuts and Seeds",
                            "Fresh Fruit Salad"
                        ]
                    },
                    "kidney_disease": {
                        "Breakfast": [
                            "Oatmeal with Berries: Rolled oats cooked with water, topped with fresh berries and a sprinkle of chia seeds.",
                            "Apple & Almond Butter Toast: Whole grain toast with almond butter and sliced apples."
                        ],
                        "Lunch": [
                            "Cucumber & Tomato Salad: Cucumbers, tomatoes, bell peppers, and a light vinaigrette.",
                            "Vegetable & Quinoa Bowl: Quinoa mixed with steamed vegetables and a small amount of olive oil."
                        ],
                        "Dinner": [
                            "Steamed Vegetables: Mixed steamed vegetables served with a side of brown rice.",
                            "Lentil Soup: A simple soup made with lentils, carrots, celery, and herbs."
                        ],
                        "Snacks": [
                            "Pear Slices",
                            "Carrot Sticks"
                        ]
                    },
                    "none": {
                        "Breakfast": [
                            "Fruit Smoothie: Mixed berries, banana, spinach, and almond milk blended together.",
                            "Whole Grain Pancakes: Served with a side of fresh fruit and a drizzle of maple syrup."
                        ],
                        "Lunch": [
                            "Vegetable Stir-Fry: Mixed vegetables and tofu stir-fried with a light soy sauce, served over brown rice.",
                            "Chickpea Salad: Chickpeas, cucumbers, cherry tomatoes, and a lemon-herb dressing."
                        ],
                        "Dinner": [
                            "Spaghetti with Marinara Sauce: Whole grain spaghetti served with a homemade marinara sauce and a side of mixed greens.",
                            "Vegetable Curry: Mixed vegetables cooked in a mild curry sauce, served with basmati rice."
                        ],
                        "Snacks": [
                            "Fresh Fruit",
                            "Trail Mix"
                        ]
                    },

                },
                
                "vegan": {
                    "diabetes": {
                        "Breakfast": [
                            "Chia Seed Pudding: Chia seeds soaked in almond milk with a few fresh berries and a sprinkle of nuts.",
                            "Smoothie Bowl: Blended spinach, avocado, and berries topped with a few slices of banana and chia seeds."
                        ],
                        "Lunch": [
                            "Quinoa & Chickpea Salad: Quinoa mixed with chickpeas, cucumbers, tomatoes, red onions, and a lemon-tahini dressing.",
                            "Sweet Potato & Black Bean Wrap: Whole grain wrap filled with roasted sweet potatoes, black beans, corn, and avocado."
                        ],
                        "Dinner": [
                            "Lentil & Vegetable Stew: A rich stew with lentils, carrots, potatoes, and spinach in a tomato base.",
                            "Stuffed Acorn Squash: Acorn squash stuffed with a mixture of brown rice, cranberries, and nuts."
                        ],
                        "Snacks": [
                            "Almonds and Walnuts",
                            "Veggie Sticks with Guacamole"
                        ]
                    },
                    "asthma": {
                        "Breakfast": [
                            "Green Smoothie: Spinach, kale, banana, and a touch of ginger blended with coconut water.",
                            "Oatmeal with Fresh Fruit: Oats cooked with almond milk, topped with fresh fruit like apples and berries."
                        ],
                        "Lunch": [
                            "Kale & Quinoa Salad: Kale mixed with quinoa, avocado, cherry tomatoes, and a light vinaigrette.",
                            "Roasted Vegetable & Hummus Wrap: Whole grain wrap with roasted vegetables and a spread of hummus."
                        ],
                        "Dinner": [
                            "Vegetable Stir-Fry: Mixed vegetables stir-fried with tofu and a ginger-garlic sauce.",
                            "Stuffed Bell Peppers: Bell peppers filled with a mixture of brown rice, black beans, corn, and spices."
                        ],
                        "Snacks": [
                            "Apple Slices with Almond Butter",
                            "Cucumber Slices with Lemon and Mint"
                        ]
                    },
                    "heart_disease": {
                        "Breakfast": [
                            "Berry Smoothie: Mixed berries blended with almond milk and a scoop of flaxseeds.",
                            "Whole Grain Toast with Nut Butter: Toasted whole grain bread topped with almond or peanut butter."
                        ],
                        "Lunch": [
                            "Chickpea & Spinach Salad: Chickpeas, spinach, cucumbers, and cherry tomatoes with a balsamic dressing.",
                            "Roasted Sweet Potato & Black Bean Bowl: Sweet potatoes, black beans, avocado, and a light lime dressing."
                        ],
                        "Dinner": [
                            "Vegetable & Bean Chili: Chili made with a variety of vegetables and beans, flavored with herbs and spices.",
                            "Baked Stuffed Zucchini: Zucchini filled with a mixture of quinoa, tomatoes, and herbs, baked to perfection."
                        ],
                        "Snacks": [
                            "Mixed Nuts: Almonds, walnuts, and cashews.",
                            "Bell Pepper Strips with Hummus"
                        ]
                    },
                    "thyroid": {
                        "Breakfast": [
                            "Flaxseed & Berry Smoothie: Blended berries with flaxseeds and a splash of almond milk.",
                            "Quinoa Porridge: Cooked quinoa with almond milk, cinnamon, and a topping of walnuts."
                        ],
                        "Lunch": [
                            "Seaweed & Avocado Salad: Seaweed mixed with avocado, cucumbers, and a sesame-ginger dressing.",
                            "Sweet Potato & Kale Stew: A comforting stew with sweet potatoes, kale, and chickpeas."
                        ],
                        "Dinner": [
                            "Butternut Squash Soup: Creamy butternut squash soup with a hint of ginger.",
                            "Stuffed Portobello Mushrooms: Portobello mushrooms filled with a mixture of quinoa, spinach, and pine nuts."
                        ],
                        "Snacks": [
                            "Roasted Pumpkin Seeds",
                            "Carrot Sticks with Tahini"
                        ]
                    },
                    "cancer": {
                        "Breakfast": [
                            "Anti-Cancer Smoothie: Spinach, kale, pineapple, and flaxseeds blended with coconut water.",
                            "Berry Chia Pudding: Chia seeds soaked in almond milk with mixed berries and a touch of honey."
                        ],
                        "Lunch": [
                            "Broccoli & Cauliflower Salad: Broccoli and cauliflower mixed with a lemon-tahini dressing.",
                            "Lentil & Veggie Soup: A hearty soup with lentils, carrots, celery, and tomatoes."
                        ],
                        "Dinner": [
                            "Quinoa-Stuffed Bell Peppers: Bell peppers filled with quinoa, black beans, corn, and tomatoes.",
                            "Vegetable Stir-Fry with Tofu: Mixed vegetables stir-fried with tofu and a light soy sauce."
                        ],
                        "Snacks": [
                            "Fresh Fruit: Apple slices or a bowl of berries.",
                            "Nuts & Seeds: Almonds and pumpkin seeds."
                        ]
                    },
                    "kidney_disease": {
                        "Breakfast": [
                            "Apple & Oatmeal Porridge: Cooked oatmeal with diced apples and a sprinkle of cinnamon.",
                            "Smoothie with Spinach & Banana: Spinach and banana blended with almond milk and a touch of chia seeds."
                        ],
                        "Lunch": [
                            "Cucumber & Avocado Salad: Sliced cucumber and avocado with a lemon-herb dressing.",
                            "Quinoa & Roasted Vegetable Bowl: Quinoa topped with roasted vegetables like carrots and zucchini."
                        ],
                        "Dinner": [
                            "Cauliflower Rice Stir-Fry: Cauliflower rice stir-fried with mixed vegetables and tofu.",
                            "Vegetable Soup: A light soup made with carrots, celery, and green beans."
                        ],
                        "Snacks": [
                            "Pear Slices",
                            "Celery Sticks with Almond Butter"
                        ]
                    },
                    "none": {
                        "Breakfast": [
                            "Fruit & Nut Granola: Granola with dried fruits, nuts, and a splash of almond milk.",
                            "Avocado Smoothie: Blended avocado, spinach, and a touch of honey with almond milk."
                        ],
                        "Lunch": [
                            "Mediterranean Chickpea Salad: Chickpeas, cherry tomatoes, cucumbers, olives, and a lemon-olive oil dressing.",
                            "Vegetable & Quinoa Wrap: Whole grain wrap with quinoa, mixed vegetables, and a spread of hummus."
                        ],
                        "Dinner": [
                            "Stuffed Bell Peppers: Bell peppers filled with brown rice, black beans, and corn.",
                            "Mushroom & Spinach Risotto: Creamy risotto made with mushrooms, spinach, and a touch of nutritional yeast."
                        ],
                        "Snacks": [
                            "Mixed Fresh Fruit: A bowl of seasonal fruits.",
                            "Trail Mix: A mix of nuts, seeds, and dried fruit."
                        ]
                    }
                },

                "gluten_free": {
                    "diabetes": {
                        "Breakfast": [
                            "Chia Seed Pudding: Chia seeds soaked in coconut milk with a few raspberries and a dash of cinnamon.",
                            "Quinoa Breakfast Bowl: Quinoa cooked with almond milk, topped with nuts, seeds, and a small amount of fresh fruit."
                        ],
                        "Lunch": [
                            "Grilled Chicken Salad: Mixed greens with grilled chicken, avocado, cherry tomatoes, cucumbers, and a balsamic vinaigrette.",
                            "Stuffed Sweet Potatoes: Sweet potatoes filled with black beans, corn, tomatoes, and topped with avocado and cilantro."
                        ],
                        "Dinner": [
                            "Zucchini Noodles with Pesto: Spiralized zucchini with a homemade basil pesto sauce.",
                            "Roasted Vegetable Medley: A mix of roasted vegetables like bell peppers, carrots, and Brussels sprouts."
                        ],
                        "Snacks": [
                            "Mixed Nuts: Almonds, walnuts, and cashews.",
                            "Fresh Veggies with Guacamole"
                        ]
                    },
                    "asthma": {
                        "Breakfast": [
                            "Smoothie Bowl: Blend of spinach, banana, almond milk, and blueberries, topped with chia seeds and a few nuts.",
                            "Gluten-Free Oatmeal: Cooked with almond milk and topped with sliced bananas and a sprinkle of walnuts."
                        ],
                        "Lunch": [
                            "Quinoa Salad with Avocado: Quinoa mixed with diced avocado, cherry tomatoes, cucumber, and a lemon vinaigrette.",
                            "Turkey & Veggie Lettuce Wraps: Ground turkey cooked with mixed vegetables wrapped in lettuce leaves."
                        ],
                        "Dinner": [
                            "Baked Salmon with Asparagus: Salmon fillets baked with a side of roasted asparagus and a squeeze of lemon.",
                            "Sweet Potato and Kale Curry: Sweet potatoes and kale in a coconut curry sauce."
                        ],
                        "Snacks": [
                            "Apple Slices with Almond Butter",
                            "Celery Sticks with Hummus"
                        ]
                    },
                    "heart_disease": {
                        "Breakfast": [
                            "Oatmeal with Berries: Rolled oats cooked with almond milk, topped with fresh berries and a sprinkle of flaxseeds.",
                            "Avocado Toast: Whole grain toast with mashed avocado, topped with cherry tomatoes and a drizzle of olive oil."
                        ],
                        "Lunch": [
                            "Lentil & Spinach Salad: Lentils, fresh spinach, cherry tomatoes, red onions, and a lemon-tahini dressing.",
                            "Grilled Vegetable Sandwich: Whole grain bread with grilled zucchini, eggplant, bell peppers, and a smear of hummus."
                        ],
                        "Dinner": [
                            "Vegetable Stew: A hearty stew made with tomatoes, carrots, sweet potatoes, zucchini, and kidney beans.",
                            "Baked Eggplant Parmesan: Slices of eggplant baked with marinara sauce and a small amount of parmesan cheese."
                        ],
                        "Snacks": [
                            "Sliced Apples with Peanut Butter",
                            "Carrot Sticks with Hummus"
                        ]
                    },
                    "thyroid": {
                        "Breakfast": [
                            "Smoothie with Spinach & Berries: Blend of spinach, blueberries, flaxseeds, and almond milk.",
                            "Egg White Omelette: Filled with spinach, tomatoes, and mushrooms."
                        ],
                        "Lunch": [
                            "Chicken & Avocado Salad: Grilled chicken breast with avocado, mixed greens, and a lemon vinaigrette.",
                            "Butternut Squash Soup: Smooth soup made with roasted butternut squash, carrots, and ginger."
                        ],
                        "Dinner": [
                            "Grilled Tilapia with Steamed Broccoli: Tilapia fillets grilled with a side of steamed broccoli.",
                            "Stuffed Acorn Squash: Acorn squash filled with a mix of quinoa, nuts, and dried cranberries."
                        ],
                        "Snacks": [
                            "Greek Yogurt with Flaxseeds",
                            "Pumpkin Seeds"
                        ]
                    },
                    "cancer": {
                        "Breakfast": [
                            "Berry Smoothie: Blend of strawberries, blueberries, spinach, and flaxseed oil.",
                            "Quinoa Porridge: Cooked quinoa with almond milk, topped with nuts and a few slices of fresh fruit."
                        ],
                        "Lunch": [
                            "Roasted Beet & Walnut Salad: Roasted beets with walnuts, mixed greens, and a balsamic vinaigrette.",
                            "Turkey & Avocado Lettuce Wraps: Ground turkey with avocado and veggies wrapped in lettuce leaves."
                        ],
                        "Dinner": [
                            "Baked Chicken with Brussels Sprouts: Chicken baked with a side of roasted Brussels sprouts.",
                            "Sweet Potato & Black Bean Chili: A hearty chili made with sweet potatoes and black beans."
                        ],
                        "Snacks": [
                            "Sliced Pear with Almonds",
                            "Cucumber Slices with Hummus"
                        ]
                    },
                    "kidney_disease": {
                        "Breakfast": [
                            "Apple Cinnamon Chia Pudding: Chia seeds soaked in almond milk with chopped apples and a sprinkle of cinnamon.",
                            "Berry Quinoa Salad: Quinoa with mixed berries, chia seeds, and a drizzle of honey."
                        ],
                        "Lunch": [
                            "Grilled Chicken & Veggie Skewers: Skewers with grilled chicken and vegetables like bell peppers and zucchini.",
                            "Spinach & Apple Salad: Spinach with sliced apples, walnuts, and a simple vinaigrette."
                        ],
                        "Dinner": [
                            "Baked Cod with Steamed Green Beans: Cod fillets baked with a side of green beans.",
                            "Vegetable Stir-Fry: Mixed vegetables stir-fried with tofu and a low-sodium soy sauce."
                        ],
                        "Snacks": [
                            "Fresh Fruit (such as berries or apple slices)",
                            "Carrot Sticks with Greek Yogurt Dip"
                        ]
                    },
                    "none": {
                        "Breakfast": [
                            "Fruit & Nut Granola: Gluten-free granola with mixed nuts and dried fruit.",
                            "Smoothie Bowl: Blend of banana, spinach, almond milk, and a variety of fruits, topped with seeds and nuts."
                        ],
                        "Lunch": [
                            "Chicken Caesar Salad: Grilled chicken with romaine lettuce, gluten-free croutons, and a Caesar dressing.",
                            "Stuffed Bell Peppers: Bell peppers filled with quinoa, black beans, corn, and cheese."
                        ],
                        "Dinner": [
                            "Pasta Primavera: Gluten-free pasta with a mix of vegetables in a light tomato sauce.",
                            "Grilled Shrimp with Veggies: Shrimp grilled with a side of roasted mixed vegetables."
                        ],
                        "Snacks": [
                            "Trail Mix: A mix of gluten-free pretzels, nuts, and dried fruit.",
                            "Rice Cakes with Almond Butter"
                        ]
                    }
                },
                    
                "low_carb": {
                    "diabetes": {
                        "Breakfast": [
                            "Egg Muffins: Baked egg muffins with spinach, mushrooms, and cheese.",
                            "Chia Seed Pudding: Chia seeds soaked in unsweetened almond milk with a few raspberries."
                        ],
                        "Lunch": [
                            "Grilled Chicken Salad: Mixed greens, grilled chicken, avocado, cucumber, and a lemon vinaigrette.",
                            "Zucchini Noodles with Pesto: Spiralized zucchini tossed with a homemade basil pesto sauce."
                        ],
                        "Dinner": [
                            "Baked Salmon: Salmon fillet baked with herbs and served with a side of sautéed asparagus.",
                            "Stuffed Portobello Mushrooms: Portobello mushrooms stuffed with spinach, feta, and sun-dried tomatoes."
                        ],
                        "Snacks": [
                            "Cucumber Slices with Cream Cheese",
                            "Hard-Boiled Eggs"
                        ]
                    },
                    "asthma": {
                        "Breakfast": [
                            "Greek Yogurt with Nuts: Unsweetened Greek yogurt topped with walnuts and a few blueberries.",
                            "Smoothie: Spinach, avocado, unsweetened almond milk, and a small handful of berries."
                        ],
                        "Lunch": [
                            "Chicken & Avocado Salad: Grilled chicken, avocado, cherry tomatoes, and a vinaigrette.",
                            "Egg Salad Lettuce Wraps: Egg salad served in crisp lettuce leaves."
                        ],
                        "Dinner": [
                            "Grilled Turkey Burgers: Lean turkey burgers served with a side of roasted cauliflower.",
                            "Spaghetti Squash with Marinara: Roasted spaghetti squash with a homemade marinara sauce."
                        ],
                        "Snacks": [
                            "Celery Sticks with Almond Butter",
                            "Cheese Cubes"
                        ]
                    },
                    "heart_disease": {
                        "Breakfast": [
                            "Scrambled Eggs with Spinach: Scrambled eggs cooked with fresh spinach.",
                            "Berry Smoothie: A smoothie made with unsweetened almond milk, spinach, and a small portion of mixed berries."
                        ],
                        "Lunch": [
                            "Grilled Chicken & Veggie Bowl: Chicken breast with steamed broccoli, bell peppers, and a drizzle of olive oil.",
                            "Cauliflower Rice Stir-Fry: Cauliflower rice stir-fried with mixed vegetables and tofu."
                        ],
                        "Dinner": [
                            "Baked Cod: Cod fillet baked with lemon and served with a side of steamed green beans.",
                            "Stuffed Bell Peppers: Bell peppers stuffed with a mixture of ground turkey, tomatoes, and spices."
                        ],
                        "Snacks": [
                            "Sliced Bell Peppers with Guacamole",
                            "Almonds"
                        ]
                    },
                    "thyroid": {
                        "Breakfast": [
                            "Smoothie Bowl: Blended spinach, avocado, unsweetened almond milk, and a few strawberries.",
                            "Egg & Veggie Scramble: Scrambled eggs with tomatoes, spinach, and bell peppers."
                        ],
                        "Lunch": [
                            "Grilled Chicken Salad: Grilled chicken with mixed greens, avocado, and a balsamic vinaigrette.",
                            "Shredded Brussels Sprouts with Almonds: Sautéed Brussels sprouts with sliced almonds."
                        ],
                        "Dinner": [
                            "Baked Chicken Thighs: Chicken thighs baked with rosemary and served with a side of roasted zucchini.",
                            "Stuffed Acorn Squash: Acorn squash stuffed with a mixture of ground turkey, onions, and spinach."
                        ],
                        "Snacks": [
                            "Greek Yogurt with Flaxseeds",
                            "Cucumber and Tomato Salad"
                        ]
                    },
                    "cancer": {
                        "Breakfast": [
                            "Avocado & Egg: Half an avocado topped with a poached egg.",
                            "Smoothie: Spinach, unsweetened almond milk, chia seeds, and a small portion of berries."
                        ],
                        "Lunch": [
                            "Salmon Salad: Mixed greens with grilled salmon, avocado, and a light vinaigrette.",
                            "Broccoli & Cheese Soup: Homemade broccoli soup with cheddar cheese."
                        ],
                        "Dinner": [
                            "Grilled Shrimp Skewers: Shrimp grilled with a side of roasted Brussels sprouts.",
                            "Stuffed Bell Peppers: Bell peppers stuffed with quinoa, black beans, and corn."
                        ],
                        "Snacks": [
                            "Mixed Nuts",
                            "Apple Slices with Almond Butter"
                        ]
                    },
                    "kidney_disease": {
                        "Breakfast": [
                            "Greek Yogurt with Blueberries: Unsweetened Greek yogurt with a few fresh blueberries.",
                            "Egg White Omelet: Egg white omelet with spinach and mushrooms."
                        ],
                        "Lunch": [
                            "Turkey & Spinach Wrap: Turkey breast with spinach and a low-carb tortilla.",
                            "Cauliflower Rice Salad: Cauliflower rice mixed with cherry tomatoes and cucumbers."
                        ],
                        "Dinner": [
                            "Baked Chicken Breast: Chicken breast baked with herbs and served with steamed green beans.",
                            "Zucchini Noodles with Marinara: Zucchini noodles with a low-sodium marinara sauce."
                        ],
                        "Snacks": [
                            "Sliced Bell Peppers",
                            "Hard-Boiled Eggs"
                        ]
                    },
                    "none": {
                            "Breakfast": [
                                "Veggie Omelet: An omelet with mushrooms, spinach, and bell peppers.",
                                "Smoothie: Almond milk, spinach, and a small handful of mixed berries."
                            ],
                            "Lunch": [
                                "Grilled Chicken Salad: Chicken breast with mixed greens, cucumber, and a light vinaigrette.",
                                "Zucchini Noodles with Pesto: Zucchini noodles tossed with basil pesto."
                            ],
                            "Dinner": [
                                "Grilled Salmon: Salmon fillet with a side of roasted asparagus.",
                                "Stuffed Bell Peppers: Bell peppers stuffed with quinoa, black beans, and corn."
                            ],
                            "Snacks": [
                                "Almonds",
                                "Celery Sticks with Hummus"
                            ]
                        }
                },

                "high_protein": {
                    "diabetes": {
                        "Breakfast": [
                            "Greek Yogurt with Almonds: Unsweetened Greek yogurt topped with sliced almonds and chia seeds.",
                            "Egg White Omelette: Egg whites with spinach, mushrooms, and tomatoes."
                        ],
                        "Lunch": [
                            "Grilled Chicken Salad: Grilled chicken breast over a bed of mixed greens, cucumbers, cherry tomatoes, and olive oil vinaigrette.",
                            "Tuna Salad Lettuce Wraps: Tuna mixed with avocado, celery, and a squeeze of lemon juice, wrapped in lettuce leaves."
                        ],
                        "Dinner": [
                            "Baked Salmon: Baked salmon fillet with steamed broccoli and quinoa.",
                            "Turkey Meatballs: Lean turkey meatballs with zucchini noodles and marinara sauce."
                        ],
                        "Snacks": [
                            "Cottage Cheese with Berries",
                            "Hard-Boiled Eggs"
                        ]
                    },
                    "asthma": {
                        "Breakfast": [
                            "Smoothie with Protein Powder: A smoothie made with almond milk, protein powder, spinach, and a banana.",
                            "Scrambled Eggs with Spinach: Scrambled eggs cooked with spinach and a side of whole grain toast."
                        ],
                        "Lunch": [
                            "Chicken and Quinoa Bowl: Grilled chicken breast with quinoa, roasted vegetables, and a drizzle of olive oil.",
                            "Lentil Soup: A hearty soup made with lentils, carrots, and celery."
                        ],
                        "Dinner": [
                            "Grilled Tofu Stir-Fry: Grilled tofu with mixed vegetables like bell peppers, broccoli, and snap peas, served with brown rice.",
                            "Baked Cod: Baked cod fillet with roasted sweet potatoes and green beans."
                        ],
                        "Snacks": [
                            "Edamame",
                            "Almond Butter on Whole Grain Crackers"
                        ]
                    },
                    "heart_disease": {
                        "Breakfast": [
                            "Overnight Oats with Protein Powder: Oats soaked overnight in almond milk with protein powder, topped with blueberries.",
                            "Egg White Scramble: Egg whites scrambled with tomatoes, onions, and a side of avocado."
                        ],
                        "Lunch": [
                            "Grilled Salmon Salad: Grilled salmon fillet over mixed greens, cucumbers, cherry tomatoes, and balsamic vinaigrette.",
                            "Turkey & Avocado Wrap: Whole wheat wrap with lean turkey, avocado, spinach, and a smear of hummus."
                        ],
                        "Dinner": [
                            "Baked Chicken Breast: Baked chicken breast with quinoa and steamed asparagus.",
                            "Lentil & Vegetable Stir-Fry: Lentils stir-fried with mixed vegetables and a low-sodium soy sauce."
                        ],
                        "Snacks": [
                            "Walnuts and Dried Cranberries",
                            "Cucumber Slices with Cottage Cheese"
                        ]
                    },
                    "thyroid": {
                        "Breakfast": [
                            "Quinoa Porridge: Quinoa cooked in almond milk with a sprinkle of cinnamon and a handful of nuts.",
                            "Egg & Avocado Breakfast Bowl: Soft-boiled eggs served over sliced avocado and a side of sautéed kale."
                        ],
                        "Lunch": [
                            "Turkey & Spinach Salad: Sliced turkey breast with spinach, sliced almonds, and a lemon-olive oil dressing.",
                            "Chicken & Broccoli Stir-Fry: Grilled chicken stir-fried with broccoli and bell peppers, served with brown rice."
                        ],
                        "Dinner": [
                            "Baked Cod with Vegetables: Baked cod with steamed carrots, green beans, and a small serving of quinoa.",
                            "Beef & Veggie Skewers: Lean beef skewers with bell peppers, onions, and cherry tomatoes."
                        ],
                        "Snacks": [
                            "Pumpkin Seeds",
                            "Greek Yogurt with Flaxseeds"
                        ]
                    },
                    "cancer": {
                        "Breakfast": [
                            "Protein Smoothie: Smoothie with almond milk, protein powder, spinach, and blueberries.",
                            "Scrambled Tofu: Tofu scrambled with turmeric, spinach, and a side of whole grain toast."
                        ],
                        "Lunch": [
                            "Grilled Chicken & Veggie Wrap: Whole wheat wrap with grilled chicken, avocado, and a mix of roasted vegetables.",
                            "Lentil & Quinoa Salad: A hearty salad with lentils, quinoa, cherry tomatoes, cucumbers, and a lemon-tahini dressing."
                        ],
                        "Dinner": [
                            "Baked Salmon with Kale: Baked salmon fillet served with sautéed kale and a small portion of brown rice.",
                            "Vegetable & Tofu Stir-Fry: Tofu stir-fried with bell peppers, snap peas, and broccoli, served over quinoa."
                        ],
                        "Snacks": [
                            "Almonds and Dried Apricots",
                            "Edamame"
                        ]
                    },
                    "kidney_disease": {
                        "Breakfast": [
                            "Low-Sodium Egg White Omelette: Egg whites cooked with spinach, tomatoes, and a pinch of pepper.",
                            "Cream of Wheat: Cream of wheat cooked with water, topped with a few slices of banana."
                        ],
                        "Lunch": [
                            "Grilled Chicken & Cucumber Salad: Grilled chicken breast with cucumbers, bell peppers, and a low-sodium vinaigrette.",
                            "Tofu & Vegetable Stir-Fry: Tofu stir-fried with zucchini, carrots, and green beans."
                        ],
                        "Dinner": [
                            "Baked Tilapia: Baked tilapia with steamed cauliflower and a small portion of white rice.",
                            "Low-Phosphorus Lentil Soup: Lentils cooked with carrots, celery, and low-sodium broth."
                        ],
                        "Snacks": [
                            "Unsalted Rice Cakes with Almond Butter",
                            "Apple Slices"
                        ]
                    },
                    "none": {
                        "Breakfast": [
                            "Egg & Avocado Toast: Whole grain toast topped with scrambled eggs and avocado slices.",
                            "Protein Pancakes: Pancakes made with protein powder, oats, and egg whites, topped with fresh berries."
                        ],
                        "Lunch": [
                            "Grilled Chicken & Veggie Bowl: Grilled chicken breast with quinoa, mixed greens, and roasted vegetables.",
                            "Tuna Salad: Tuna mixed with Greek yogurt, celery, and a squeeze of lemon, served on whole grain bread."
                        ],
                        "Dinner": [
                            "Baked Salmon with Quinoa: Baked salmon fillet with a side of quinoa and steamed broccoli.",
                            "Turkey & Vegetable Stir-Fry: Lean turkey stir-fried with bell peppers, snap peas, and brown rice."
                        ],
                        "Snacks": [
                            "Cottage Cheese with Pineapple",
                            "Almonds and a Hard-Boiled Egg"
                        ]
                    }
                },
                
                "diabetic_friendly": {
                    "diabetes": {
                        "Breakfast": [
                            "Chia Pudding: Chia seeds soaked in almond milk with berries and a touch of honey.",
                            "Greek Yogurt Parfait: Unsweetened Greek yogurt layered with nuts, seeds, and a small amount of fresh fruit."
                        ],
                        "Lunch": [
                            "Quinoa & Black Bean Salad: Quinoa, black beans, corn, bell peppers, avocado, and a lime-cilantro dressing.",
                            "Vegetable & Hummus Wrap: Whole wheat wrap filled with hummus, spinach, shredded carrots, cucumbers, and bell peppers."
                        ],
                        "Dinner": [
                            "Stuffed Bell Peppers: Bell peppers stuffed with a mixture of quinoa, black beans, corn, tomatoes, and spices.",
                            "Cauliflower Rice Stir-Fry: Cauliflower rice with mixed vegetables, tofu, and a low-sodium soy sauce."
                        ],
                        "Snacks": [
                            "Mixed Nuts: Almonds, walnuts, and pistachios.",
                            "Celery Sticks with Almond Butter"
                        ]
                },
                    "asthma": {
                        "Breakfast": [
                            "Smoothie Bowl: A blend of spinach, banana, berries, and almond milk topped with nuts and seeds.",
                            "Oatmeal with Pears: Rolled oats with almond milk, topped with sliced pears and a sprinkle of cinnamon."
                        ],
                        "Lunch": [
                            "Spinach & Chickpea Salad: Fresh spinach with chickpeas, cucumber, tomatoes, and a lemon-olive oil dressing.",
                            "Vegetable Soup: A light vegetable broth with carrots, celery, zucchini, and quinoa."
                        ],
                        "Dinner": [
                            "Stuffed Sweet Potatoes: Baked sweet potatoes stuffed with black beans, corn, and avocado.",
                            "Roasted Vegetable Medley: Roasted carrots, Brussels sprouts, and butternut squash with a side of quinoa."
                        ],
                        "Snacks": [
                            "Apple Slices with Almond Butter",
                            "Carrot Sticks with Guacamole"
                        ]
                    },
                    "heart_disease": {
                        "Breakfast": [
                            "Oatmeal with Berries: Rolled oats cooked with almond milk, topped with fresh berries and a sprinkle of flaxseeds.",
                            "Avocado Toast: Whole grain toast with mashed avocado, topped with cherry tomatoes and a drizzle of olive oil."
                        ],
                        "Lunch": [
                            "Lentil & Spinach Salad: Lentils, fresh spinach, cherry tomatoes, red onions, and a lemon-tahini dressing.",
                            "Grilled Vegetable Sandwich: Whole grain bread with grilled zucchini, eggplant, bell peppers, and a smear of hummus."
                        ],
                        "Dinner": [
                            "Vegetable Stew: A hearty stew made with tomatoes, carrots, sweet potatoes, zucchini, and kidney beans.",
                            "Baked Eggplant Parmesan: Slices of eggplant baked with marinara sauce and a small amount of parmesan cheese."
                        ],
                        "Snacks": [
                            "Sliced Apples with Peanut Butter",
                            "Carrot Sticks with Hummus"
                        ]
                    },
                    "thyroid": {
                        "Breakfast": [
                            "Buckwheat Pancakes: Buckwheat flour pancakes served with a side of fresh berries and a dollop of yogurt.",
                            "Smoothie: A blend of kale, banana, almond milk, and a scoop of plant-based protein powder."
                        ],
                        "Lunch": [
                            "Quinoa Salad: Quinoa with spinach, roasted sweet potatoes, and a lemon-tahini dressing.",
                            "Veggie Wrap: Whole grain wrap with hummus, shredded carrots, cucumbers, and avocado."
                        ],
                        "Dinner": [
                            "Grilled Tofu with Vegetables: Grilled tofu with steamed broccoli, carrots, and a side of brown rice.",
                            "Vegetable Stir-Fry: Mixed vegetables stir-fried with ginger, garlic, and a low-sodium tamari sauce."
                        ],
                        "Snacks": [
                            "Brazil Nuts: A handful of Brazil nuts for selenium support.",
                            "Apple Slices with Almond Butter"
                        ]
                    },
                    "cancer": {
                        "Breakfast": [
                            "Green Smoothie: Spinach, kale, apple, banana, and a scoop of chia seeds blended with almond milk.",
                            "Oatmeal with Berries: Rolled oats with a mixture of berries and a sprinkle of ground flaxseeds."
                        ],
                        "Lunch": [
                            "Kale & Quinoa Salad: Kale with cooked quinoa, roasted chickpeas, and a lemon-tahini dressing.",
                            "Vegetable Soup: Broth-based vegetable soup with carrots, celery, and barley."
                        ],
                        "Dinner": [
                            "Grilled Portobello Mushrooms: Grilled mushrooms with a side of roasted Brussels sprouts and sweet potatoes.",
                            "Vegetable Curry: Mixed vegetables simmered in a coconut milk curry sauce, served with brown rice."
                        ],
                        "Snacks": [
                            "Carrot & Celery Sticks with Hummus",
                            "Mixed Berries: A small bowl of mixed fresh berries."
                        ]
                    },
                    "kidney_disease": {
                        "Breakfast": [
                            "Apple Cinnamon Oatmeal: Oats cooked with almond milk, topped with diced apples and a dash of cinnamon.",
                            "Smoothie: A blend of low-potassium fruits like blueberries, strawberries, and almond milk."
                        ],
                        "Lunch": [
                            "Rice & Vegetable Stir-Fry: Brown rice with steamed broccoli, cauliflower, and a drizzle of olive oil.",
                            "Cucumber & Avocado Salad: Sliced cucumbers, avocado, and a lemon-olive oil dressing."
                        ],
                        "Dinner": [
                            "Grilled Vegetables: A mix of grilled vegetables like bell peppers, zucchini, and eggplant, served with quinoa.",
                            "Stuffed Bell Peppers: Bell peppers stuffed with a mixture of rice, black beans, and herbs."
                        ],
                        "Snacks": [
                            "Apple Slices with Peanut Butter",
                            "Rice Cakes with Hummus"
                        ]
                    },
                    "none": {
                "Breakfast": [
                    "Overnight Oats: Rolled oats soaked in almond milk with chia seeds, topped with fresh berries.",
                    "Avocado Toast: Whole grain toast topped with mashed avocado and a sprinkle of chia seeds."
                ],
                "Lunch": [
                    "Quinoa & Veggie Salad: Quinoa mixed with roasted vegetables and a lemon-tahini dressing.",
                    "Vegetable Wrap: Whole grain wrap filled with hummus, spinach, shredded carrots, and cucumber."
                ],
                "Dinner": [
                    "Stir-Fried Vegetables: A variety of stir-fried vegetables served with brown rice or quinoa.",
                    "Stuffed Zucchini: Zucchini boats stuffed with quinoa, black beans, and diced tomatoes."
                ],
                "Snacks": [
                    "Mixed Nuts: Almonds, walnuts, and cashews.",
                    "Carrot Sticks with Hummus"
                ]
            }
                }
            }
    
         # Handle cases based on provided data
            if dietary_preference and health_condition:
                if dietary_preference in combined_recommendations:
                    if health_condition in combined_recommendations[dietary_preference]:
                        return JsonResponse(combined_recommendations[dietary_preference][health_condition], safe=False)
                    else:
                        return JsonResponse({"error": "No combined recommendations found for the given health condition"}, status=404)
                else:
                    return JsonResponse({"error": "No combined recommendations found for the given dietary preference"}, status=404)

            elif dietary_preference:
                if dietary_preference in combined_recommendations:
                    return JsonResponse(combined_recommendations[dietary_preference], safe=False)
                else:
                    return JsonResponse({"error": "Invalid dietary preference"}, status=400)

            elif health_condition:
                # Iterate over all dietary preferences to find the health condition
                for diet in combined_recommendations:
                    if health_condition in combined_recommendations[diet]:
                        return JsonResponse(combined_recommendations[diet][health_condition], safe=False)
                return JsonResponse({"error": "Invalid health condition"}, status=400)

            return JsonResponse({"error": "Missing dietary preference or health condition"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)



#Medical file upload
#uploaded by user
from django.core.files.storage import default_storage
@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES:
        file_urls = []
        for file_key in request.FILES:
            file = request.FILES[file_key]
            file_name = default_storage.save(file.name, file)
            file_urls.append(default_storage.url(file_name))
        return JsonResponse({'file_urls': file_urls}, status=201)
    return JsonResponse({'error': 'No files uploaded'}, status=400)

#accessed by admin
@csrf_exempt
def get_user_files(request):
    users = User.objects.all()
    user_files = []
    for user in users:
        files = UploadedFile.objects.filter(user=user)
        user_files.append({
            'username': user.first_name + user.last_name,
            'files': [{'name': file.file.name, 'url': file.file.url} for file in files]
        })
    return JsonResponse({'user_files': user_files})

# for generating the system report
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Doctor, Appointment, Feedback

@csrf_exempt
def generate_system_report(request):
    # Fetch data from your models (e.g., User, Appointment, Feedback)
    users = User.objects.all()
    doctors = Doctor.objects.all()
    appointments = Appointment.objects.all()
    feedbacks = Feedback.objects.all()

    # Adjust the queries to reflect your custom User model fields
    total_users = users.count()
    total_doctors = doctors.count()
    total_appointments = appointments.count()
    upcoming_appointments = appointments.filter(status='upcoming').count()
    total_feedback = feedbacks.count()

    # If your User model has an is_superuser field, you might use that to check for admin users
    admin_users = users.filter(is_superuser=True).count()

    # Prepare the data for JSON response
    data = {
        'users': {
            'total': total_users,
            'admin_users': admin_users,  # Example: Count of admin users
        },
        'doctors': {
            'total': total_doctors,
        },
        'appointments': {
            'total': total_appointments,
            'upcoming': upcoming_appointments,
        },
        'feedbacks': {
            'total': total_feedback,
        }
    }

    # Return the response as JSON
    return JsonResponse(data)

@csrf_exempt
def get_user_for_appointment(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        return JsonResponse({'name': f"{user.first_name} {user.last_name}"})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

@csrf_exempt
def get_doctor_for_appointment(request, doctor_id):
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        return JsonResponse({
            'first_name': doctor.first_name,
            'last_name': doctor.last_name,
            'specialty': doctor.specialty,
            'location': doctor.location
        })
    except Doctor.DoesNotExist:
        return JsonResponse({'error': 'Doctor not found'}, status=404)

@csrf_exempt
def delete_appointments(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('id')
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.delete()
            return JsonResponse({'status': 200, 'msg': 'Appointment deleted successfully'})
        except Appointment.DoesNotExist:
            return JsonResponse({'status': 404, 'msg': 'Appointment not found'})
    return JsonResponse({'status': 405, 'msg': 'Method not allowed'}, status=405)

def get_appointments(request):
    appointments = Appointment.objects.all()
    data = [
        {
            'id': appt.id,
            'user': appt.user.id,
            'doctor': appt.doctor.id,
            'appointment_date': appt.appointment_date,
            'status': appt.status,
            'created_at': appt.created_at,
            'updated_at': appt.updated_at
        }
        for appt in appointments
    ]
    return JsonResponse({'status': 200, 'data': data})

from django.utils import timezone
from datetime import datetime
import pytz

@csrf_exempt
def get_upcoming_appointments(request):
    try:
        # Get the current time in IST
        ist = pytz.timezone('Asia/Kolkata')
        now_ist = timezone.now().astimezone(ist)  # Get the current time in IST

        # Convert appointment_date to IST before filtering
        upcoming_appointments = Appointment.objects.all()
        filtered_appointments = []

        for appointment in upcoming_appointments:
            # Convert appointment_date to IST
            appointment_ist = appointment.appointment_date.astimezone(ist)
            if appointment_ist >= now_ist:
                appointment_dict = {
                    'id': appointment.id,
                    'user': appointment.user.id,
                    'doctor': appointment.doctor.id,
                    'appointment_date': appointment.appointment_date,
                    'status': appointment.status,
                    'created_at': appointment.created_at,
                    'updated_at': appointment.updated_at,
                }
                filtered_appointments.append(appointment_dict)

        return JsonResponse({'total': len(filtered_appointments), 'data': filtered_appointments, 'status': 200}, status=200)
    except Exception as e:
        return JsonResponse({'msg': str(e), 'status': 500}, status=500)
