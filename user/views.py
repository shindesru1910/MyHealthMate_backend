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
from django.core.mail import send_mail
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
            
        except UserProfile.DoesNotExist:
            # Handle the case where UserProfile does not exist
            pass

        # Create token with activity_level and health_goals
        token = create_token(user.id, user.email, user.first_name + ' ' + user.last_name, user.is_admin, activity_level, health_goals)
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

# ExerciseReminder APIs
@csrf_exempt
def create_exercise_reminder(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)
    
    try:
        user_id = request.POST['user_id']
        reminder_time = request.POST['reminder_time']
        reminder_message = request.POST['reminder_message']

        user = User.objects.get(id=user_id)
        reminder = ExerciseReminder(user=user, reminder_time=reminder_time, reminder_message=reminder_message)
        reminder.save()

        return JsonResponse({'msg': 'Data has been successfully created', 'status': 200}, status=200)
    except Exception as e:
        return JsonResponse({'msg': str(e), 'status': 500}, status=500)

@csrf_exempt
def get_exercise_reminder(request):
    try:
        reminders = ExerciseReminder.objects.all()
        data = []

        for reminder in reminders:
            reminder_dict = {}
            reminder_dict['id'] = reminder.id
            reminder_dict['user'] = reminder.user.id
            reminder_dict['reminder_time'] = reminder.reminder_time
            reminder_dict['reminder_message'] = reminder.reminder_message
            reminder_dict['created_at'] = reminder.created_at
            reminder_dict['updated_at'] = reminder.updated_at

            data.append(reminder_dict)
        return JsonResponse({'data': data, 'status': 200}, status=200)
    except Exception as e:
        return JsonResponse({'msg': str(e), 'status': 500}, status=500)


@csrf_exempt
def update_exercise_reminder(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)
    try:
        id = request.POST['id']
        user_id = request.POST['user_id']
        reminder_time = request.POST['reminder_time']
        reminder_message = request.POST['reminder_message']

        reminder = ExerciseReminder.objects.get(id=id)
        reminder.user = User.objects.get(id=user_id)
        reminder.reminder_time = reminder_time
        reminder.reminder_message = reminder_message
        reminder.save()
        return JsonResponse({'msg': 'Data has been updated successfully', 'status': 200}, status=200)
    except Exception as e:
        return JsonResponse({'msg': str(e), 'status': 500}, status=500)

@csrf_exempt
def delete_exercise_reminder(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)
    
    try:
        id = request.POST['id']
        reminder = ExerciseReminder.objects.get(id=id)
        reminder.delete()
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

# @csrf_exempt
# def get_feedback(request):
#     try:
#         feedbacks = Feedback.objects.all()
#         data = []

#         for feedback in feedbacks:
#             feedback_dict = {}
#             feedback_dict['id'] = feedback.id
#             feedback_dict['user'] = feedback.user.id
#             feedback_dict['feedback_text'] = feedback.feedback_text
#             feedback_dict['created_at'] = feedback.created_at

#             data.append(feedback_dict)
#         return JsonResponse({'data': data, 'status': 200}, status=200)
#     except Exception as e:
#         return JsonResponse({'msg': str(e), 'status': 500}, status=500)


#new
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

@csrf_exempt
@login_required
def set_reminder(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title')
            name = data.get('name')
            time = data.get('time')

            if not all([title, name, time]):
                return JsonResponse({'status': 'error', 'message': 'Missing fields'}, status=400)

            Reminder.objects.create(user=request.user, title=title, name=name, time=time)
            return JsonResponse({'status': 'success'}, status=200)
        except json.JSONDecodeError:
            logger.error("JSON decode error: %s", request.body)
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.error("Exception occurred: %s", e)
            return JsonResponse({'status': 'error', 'message': 'Server error'}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


def send_reminder_email(to_email, subject, body):
    try:
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
            fail_silently=False,
        )
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}. Error: {e}")


@login_required
def get_all_emails(request):
    if request.method == 'GET':
        emails = list(User.objects.values_list('email', flat=True))
        return JsonResponse({'emails': emails}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

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



# @csrf_exempt
# def get_exercise_recommendations(request):
#     if request.method == 'POST':
#         try:
#             # Parse the JSON data from the request body
#             data = json.loads(request.body)
#             activity_level = data.get('activity_level')
#             health_goals = data.get('health_goal')
#             if not health_goals:
#                 raise ValueError("Health goals are missing.")
            
#             recommendations = {
#             "sedentary": {
#                 "weight_loss": {
#                     "Walking": {
#                         "Frequency": "5 days a week",
#                         "Duration": "30 minutes",
#                         "Intensity": "Moderate pace to burn calories."
#                     },
#                     "Bodyweight Circuit": {
#                         "Frequency": "3 days a week",
#                         "Exercises": "Squats, lunges, push-ups, and planks.",
#                         "Reps/Sets": "3 sets of 15 reps.",
#                         "Goal": "Burn fat and build endurance."
#                     },
#                     "Stretching": {
#                         "Frequency": "Daily",
#                         "Duration": "10 minutes",
#                         "Focus": "Increase flexibility and prevent injuries."
#                     },
#                     "videos": [
#                         "https://www.youtube.com/watch?v=7zPiD3ibvCc",
#                         "https://www.youtube.com/watch?v=7zPiD3ibvCc",
#                         "https://www.youtube.com/watch?v=7zPiD3ibvCc"
#                     ]
#                 },
#                 "muscle_gain": {
#                     "Bodyweight Strength Training": {
#                         "Frequency": "4 days a week",
#                         "Exercises": "Push-ups, pull-ups, squats, and planks.",
#                         "Reps/Sets": "4 sets of 8-12 reps.",
#                         "Goal": "Build foundational muscle strength."
#                     },
#                     "Basic Weight Lifting": {
#                         "Frequency": "3 days a week",
#                         "Exercises": "Dumbbell bench press, bicep curls, tricep dips.",
#                         "Reps/Sets": "3 sets of 8-10 reps.",
#                         "Goal": "Increase muscle mass with light weights."
#                     },
#                     "videos": [
#                         "https://www.youtube.com/watch?v=HUx7GTeSoJw",
#                         "https://www.youtube.com/watch?v=meQwgZzVczc"
#                     ]
#                 },
#                 "flexibility": {
#                     "Daily Stretching Routine": {
#                         "Frequency": "7 days a week",
#                         "Duration": "15-20 minutes",
#                         "Focus": "Full-body stretches focusing on major muscle groups."
#                     },
#                     "Yoga": {
#                         "Frequency": "3 days a week",
#                         "Duration": "30 minutes",
#                         "Focus": "Improve flexibility and reduce stress."
#                     },
#                     "videos": [
#                         "https://www.youtube.com/watch?v=v7AYKMP6rOE",
#                         "https://www.youtube.com/watch?v=VaoV1PrYft4"
#                     ]
#                 },
#                 "general_fitness": {
#                     "Light Aerobics": {
#                         "Frequency": "4 days a week",
#                         "Duration": "30 minutes",
#                         "Focus": "Improve overall cardiovascular health."
#                     },
#                     "Mixed Bodyweight and Flexibility": {
#                         "Frequency": "3 days a week",
#                         "Exercises": "Combination of squats, lunges, push-ups, and stretching.",
#                         "Reps/Sets": "3 sets of 12-15 reps.",
#                         "Goal": "Balance strength and flexibility."
#                     },
#                     "videos": [
#                         "https://www.youtube.com/watch?v=MLqgL81V87A",
#                         "https://www.youtube.com/watch?v=X3-gKPNyrTA"
#                     ]
#                 },
#                 "stress_relief": {
#                     "Mindful Walking": {
#                         "Frequency": "5 days a week",
#                         "Duration": "20-30 minutes",
#                         "Focus": "Combine light exercise with mindfulness for stress reduction."
#                     },
#                     "Gentle Yoga": {
#                         "Frequency": "3 days a week",
#                         "Duration": "30 minutes",
#                         "Focus": "Reduce stress and tension in the body."
#                     },
#                     "Breathing Exercises": {
#                         "Frequency": "Daily",
#                         "Duration": "5-10 minutes",
#                         "Focus": "Practice deep breathing to reduce anxiety and stress."
#                     },
#                     "videos": [
#                         "https://www.youtube.com/watch?v=aNXKjGFUlMs",
#                         "https://www.youtube.com/watch?v=SEfs5TJZ6Nk"
#                     ]
#                 }
#             },
#             "lightly_active": {
#                 "weight_loss": {
#                     "Cardio Workouts": {
#                         "Frequency": "4-5 days a week",
#                         "Duration": "30-40 minutes",
#                         "Intensity": "Brisk walking, jogging, cycling.",
#                         "Goal": "Burn calories and improve cardiovascular health."
#                     },
#                     "Strength Training": {
#                         "Frequency": "3 days a week",
#                         "Exercises": "Weightlifting with light weights, resistance bands.",
#                         "Reps/Sets": "3 sets of 12-15 reps.",
#                         "Goal": "Increase muscle mass and metabolism."
#                     },
#                     "videos": [
#                         "https://www.youtube.com/watch?v=sVdQ2q8ZStI",
#                         "https://www.youtube.com/watch?v=UFP5xIk2RhA"
#                     ]
#                 },
#                 "muscle_gain": {
#                     "Strength and Hypertrophy": {
#                         "Frequency": "4 days a week",
#                         "Exercises": "Compound movements like squats, deadlifts, bench press.",
#                         "Reps/Sets": "4 sets of 8-10 reps.",
#                         "Goal": "Build muscle mass."
#                     },
#                     "High-Protein Diet": {
#                         "Advice": "Increase protein intake to support muscle growth.",
#                         "Foods": "Chicken, fish, eggs, legumes, protein shakes."
#                     },
#                     "videos": [
#                         "https://www.youtube.com/watch?v=7zPiD3ibvCc",
#                         "https://www.youtube.com/watch?v=HUx7GTeSoJw"
#                     ]
#                 },
#                 "flexibility": {
#                     "Dynamic Stretching": {
#                         "Frequency": "Before workouts",
#                         "Duration": "10 minutes",
#                         "Focus": "Prepare muscles and joints for exercise."
#                     },
#                     "Post-Workout Stretching": {
#                         "Frequency": "After each workout",
#                         "Duration": "10-15 minutes",
#                         "Focus": "Improve flexibility and reduce muscle tightness."
#                     },
#                     "videos": [
#                         "https://www.youtube.com/watch?v=KIxb-y3CaFk",
#                         "https://www.youtube.com/watch?v=uHYjN6Ou2-M"
#                     ]
#                 },
#                 "general_fitness": {
#                     "Mixed Cardio and Strength": {
#                         "Frequency": "4 days a week",
#                         "Exercises": "Combination of running, cycling, and weightlifting.",
#                         "Duration": "40-50 minutes",
#                         "Goal": "Maintain overall fitness and health."
#                     },
#                     "Active Recovery": {
#                         "Frequency": "1-2 days a week",
#                         "Activities": "Light activities like walking, yoga.",
#                         "Goal": "Promote recovery while staying active."
#                     },
#                     "videos": [
#                         "https://www.youtube.com/watch?v=e3-zpBc_hg8",
#                         "https://www.youtube.com/watch?v=iZ-PywX9roo"
#                     ]
#                 },
#                 "stress_relief": {
#                     "Yoga for Stress Relief": {
#                         "Frequency": "3 days a week",
#                         "Duration": "30 minutes",
#                         "Focus": "Relaxation and stress management."
#                     },
#                     "Breathing and Meditation": {
#                         "Frequency": "Daily",
#                         "Duration": "10-15 minutes",
#                         "Focus": "Reduce stress and anxiety."
#                     },
#                     "videos": [
#                         "https://www.youtube.com/watch?v=rYlLXrKhRAc",
#                         "https://www.youtube.com/watch?v=MLqgL81V87A"
#                     ]
#                 }
#             },
#             "moderately_active": {
#                 "weight_loss": {
#                     "High-Intensity Cardio": {
#                         "Frequency": "5 days a week",
#                         "Duration": "30-40 minutes",
#                         "Intensity": "High-intensity interval training (HIIT), running.",
#                         "Goal": "Maximize calorie burn and fat loss."
#                     },
#                     "Strength Training": {
#                         "Frequency": "4 days a week",
#                         "Exercises": "Weightlifting with moderate to heavy weights.",
#                         "Reps/Sets": "4 sets of 8-10 reps.",
#                         "Goal": "Build lean muscle to boost metabolism."
#                     },
#                     "videos": [
#                         "https://www.youtube.com/watch?v=UFP5xIk2RhA",
#                         "https://www.youtube.com/watch?v=meQwgZzVczc"
#                     ]
#                 },
#                 "muscle_gain": {
#                     "Strength and Hypertrophy": {
#                         "Frequency": "4-5 days a week",
#                         "Exercises": "Heavy weightlifting with compound movements.",
#                         "Reps/Sets": "4-5 sets of 6-8 reps.",
#                         "Goal": "Increase muscle size and strength."
#                     },
#                     "Protein and Supplement Advice": {
#                         "Advice": "Consider protein supplements and a high-protein diet.",
#                         "Supplements": "Whey protein, BCAAs, creatine."
#                     },
#                     "videos": [
#                         "https://www.youtube.com/watch?v=KIxb-y3CaFk",
#                         "https://www.youtube.com/watch?v=HUx7GTeSoJw"
#                     ]
#                 },
#                 "flexibility": {
#                     "Advanced Stretching": {
#                         "Frequency": "Daily",
#                         "Duration": "15-20 minutes",
#                         "Focus": "Improve flexibility for better performance."
#                     },
#                     "Yoga and Mobility Work": {
#                         "Frequency": "3 days a week",
#                         "Duration": "30 minutes",
#                         "Focus": "Enhance flexibility and mobility."
#                     },
#                     "videos": [
#                         "https://www.youtube.com/watch?v=3jiL6bhR64Y",
#                         "https://www.youtube.com/watch?v=KIxb-y3CaFk"
#                     ]
#                 },
#                 "general_fitness": {
#                     "Balanced Workout Routine": {
#                         "Frequency": "5 days a week",
#                         "Exercises": "Mix of cardio, strength training, and flexibility.",
#                         "Duration": "60 minutes",
#                         "Goal": "Maintain overall fitness and health."
#                     },
#                     "Active Recovery": {
#                         "Frequency": "1-2 days a week",
#                         "Activities": "Gentle activities like swimming, cycling.",
#                         "Goal": "Promote recovery and prevent burnout."
#                     },
#                     "videos": [
#                         "https://www.youtube.com/watch?v=1DYH5ud3zHo",
#                         "https://www.youtube.com/watch?v=UFP5xIk2RhA"
#                     ]
#                 },
#                 "stress_relief": {
#                     "High-Intensity Yoga": {
#                         "Frequency": "3 days a week",
#                         "Duration": "30 minutes",
#                         "Focus": "Combine exercise with relaxation techniques."
#                     },
#                     "Meditation and Mindfulness": {
#                         "Frequency": "Daily",
#                         "Duration": "15 minutes",
#                         "Focus": "Manage stress and enhance mental well-being."
#                     },
#                     "videos": [
#                         "https://www.youtube.com/watch?v=aNXKjGFUlMs",
#                         "https://www.youtube.com/watch?v=X3-gKPNyrTA"
#                     ]
#                 }
#             },
#             "very_active": {
#                 "weight_loss": {
#                     "High-Intensity Interval Training (HIIT)": {
#                         "Frequency": "5-6 days a week",
#                         "Duration": "20-30 minutes",
#                         "Intensity": "Short bursts of intense exercise followed by rest.",
#                         "Goal": "Maximize fat loss and improve cardiovascular fitness."
#                     },
#                     "Strength and Conditioning": {
#                         "Frequency": "4-5 days a week",
#                         "Exercises": "Combination of heavy lifting and metabolic conditioning.",
#                         "Reps/Sets": "4-5 sets of 6-8 reps.",
#                         "Goal": "Increase muscle mass while burning fat."
#                     },
#                     "videos": [
#                         "https://www.youtube.com/watch?v=4o2Bqdm6wm8",
#                         "https://www.youtube.com/watch?v=kjdXYdj2X2s"
#                     ]
#                 },
#                 "muscle_gain": {
#                     "Advanced Strength Training": {
#                         "Frequency": "5-6 days a week",
#                         "Exercises": "Heavy compound movements, advanced techniques like drop sets.",
#                         "Reps/Sets": "4-6 sets of 4-6 reps.",
#                         "Goal": "Maximize muscle growth and strength."
#                     },
#                     "Nutritional Advice": {
#                         "Advice": "Ensure high protein intake and consider supplements.",
#                         "Supplements": "Creatine, protein powder, BCAAs."
#                     },
#                     "videos": [
#                         "https://www.youtube.com/watch?v=HUx7GTeSoJw",
#                         "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
#                     ]
#                 },
#                 "flexibility": {
#                     "Advanced Flexibility Routine": {
#                         "Frequency": "Daily",
#                         "Duration": "20-30 minutes",
#                         "Focus": "Increase range of motion and recovery."
#                     },
#                     "Yoga for Athletes": {
#                         "Frequency": "3 days a week",
#                         "Duration": "30 minutes",
#                         "Focus": "Enhance flexibility and reduce muscle soreness."
#                     },
#                     "videos": [
#                         "https://www.youtube.com/watch?v=KIxb-y3CaFk",
#                         "https://www.youtube.com/watch?v=VaoV1PrYft4"
#                     ]
#                 },
#                 "general_fitness": {
#                     "Intensive Workout Programs": {
#                         "Frequency": "6 days a week",
#                         "Exercises": "Advanced cardio, strength, and flexibility workouts.",
#                         "Duration": "60-90 minutes",
#                         "Goal": "Maintain peak physical condition and performance."
#                     },
#                     "Active Recovery and Mobility": {
#                         "Frequency": "1 day a week",
#                         "Activities": "Light activities, stretching, foam rolling.",
#                         "Goal": "Aid recovery and maintain flexibility."
#                     },
#                     "videos": [
#                         "https://www.youtube.com/watch?v=UFP5xIk2RhA",
#                         "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
#                     ]
#                 },
#                 "stress_relief": {
#                     "High-Intensity Yoga and Meditation": {
#                         "Frequency": "3 days a week",
#                         "Duration": "30 minutes",
#                         "Focus": "Combine high-intensity exercise with relaxation."
#                     },
#                     "Mindfulness and Relaxation Techniques": {
#                         "Frequency": "Daily",
#                         "Duration": "15-20 minutes",
#                         "Focus": "Manage stress and improve mental well-being."
#                     },
#                     "videos": [
#                         "https://www.youtube.com/watch?v=aNXKjGFUlMs",
#                         "https://www.youtube.com/watch?v=X3-gKPNyrTA"
#                     ]
#                 }
#             }
# }
            
#             # Return recommendations based on the activity level
#             if activity_level in recommendations:
#                 return JsonResponse(recommendations[activity_level], safe=False)
#             else:
#                 return JsonResponse({"error": "Activity level not supported"}, status=400)
            
#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON format"}, status=400)
    
#         except Exception as e:
#         # Log the exception if necessary (for debugging purposes)
#             return JsonResponse({"error": "An unexpected error occurred"}, status=500)
    
#         finally:
#         # Any cleanup code (if needed) goes here
#             print("Request processing complete")