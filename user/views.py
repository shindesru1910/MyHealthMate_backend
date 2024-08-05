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


logger = logging.getLogger(__name__)

ist_timezone = pytz.timezone('Asia/Kolkata')

@csrf_exempt
def login(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=400)

    email = request.POST['email']
    password = request.POST['password']

    user = authenticate(request, email=email, password=password)

    if user is not None:
        user_profile = UserProfile(user = user)
        token = create_token(user.id, user.email, user.first_name + ' ' + user.last_name,user.is_admin)
        return JsonResponse({'status': 200, 'msg': 'Login Successfully', 'token': token}, status=200)
    else:
        return JsonResponse({'status': 400, 'msg': 'Check your email or password!!'}, status=200)

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
# @csrf_exempt
# def submit_appointment(request):
#     if request.method == 'POST':
#         # Parse the incoming data
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         date = request.POST.get('date')
#         specialty = request.POST.get('speciality')
#         doctor_id = request.POST.get('doctor')
#         message = request.POST.get('message')

#         # Validate the data
#         if not all([name, email, date, specialty, doctor_id]):
#             return JsonResponse({'error': 'Missing required fields'}, status=400)
        
#         try:
#             user = User.objects.get(email=email)
#             doctor = Doctor.objects.get(id=doctor_id)

#             # Create the appointment
#             appointment = Appointment(
#                 user=user,
#                 doctor=doctor,
#                 appointment_date=date,
#                 status='scheduled',
#                 phone=phone,
#                 specialty=specialty,
#                 message=message
#             )

#             # Save the appointment
#             appointment.clean()  # Call clean to perform validation
#             appointment.save()

#             # Return success response
#             return JsonResponse({'status': 'OK'})
#         except User.DoesNotExist:
#             return JsonResponse({'error': 'User not found'}, status=404)
#         except Doctor.DoesNotExist:
#             return JsonResponse({'error': 'Doctor not found'}, status=404)
#         except ValidationError as e:
#             return JsonResponse({'error': str(e)}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)

#     return JsonResponse({'error': 'Method not allowed'}, status=405)



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
        user_id = request.POST['user_id']
        doctor_id = request.POST['doctor_id']
        appointment_date = request.POST['appointment_date']
        status = request.POST['status']

        user = User.objects.get(id=user_id)
        doctor = Doctor.objects.get(id=doctor_id)
        appointment = Appointment(user=user, doctor=doctor, appointment_date=appointment_date, status=status)
        appointment.save()

        return JsonResponse({'msg': 'Data has been successfully created', 'status': 200}, status=200)
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
# @csrf_exempt
# def create_exercise_reminder(request):
#     if request.method != 'POST':
#         return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)
    
#     try:
#         user_id = request.POST['user_id']
#         reminder_time = request.POST['reminder_time']
#         reminder_message = request.POST['reminder_message']

#         user = User.objects.get(id=user_id)
#         reminder = ExerciseReminder(user=user, reminder_time=reminder_time, reminder_message=reminder_message)
#         reminder.save()

#         return JsonResponse({'msg': 'Data has been successfully created', 'status': 200}, status=200)
#     except Exception as e:
#         return JsonResponse({'msg': str(e), 'status': 500}, status=500)

# @csrf_exempt
# def get_exercise_reminder(request):
#     try:
#         reminders = ExerciseReminder.objects.all()
#         data = []

#         for reminder in reminders:
#             reminder_dict = {}
#             reminder_dict['id'] = reminder.id
#             reminder_dict['user'] = reminder.user.id
#             reminder_dict['reminder_time'] = reminder.reminder_time
#             reminder_dict['reminder_message'] = reminder.reminder_message
#             reminder_dict['created_at'] = reminder.created_at
#             reminder_dict['updated_at'] = reminder.updated_at

#             data.append(reminder_dict)
#         return JsonResponse({'data': data, 'status': 200}, status=200)
#     except Exception as e:
#         return JsonResponse({'msg': str(e), 'status': 500}, status=500)


# @csrf_exempt
# def update_exercise_reminder(request):
#     if request.method != 'POST':
#         return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)
#     try:
#         id = request.POST['id']
#         user_id = request.POST['user_id']
#         reminder_time = request.POST['reminder_time']
#         reminder_message = request.POST['reminder_message']

#         reminder = ExerciseReminder.objects.get(id=id)
#         reminder.user = User.objects.get(id=user_id)
#         reminder.reminder_time = reminder_time
#         reminder.reminder_message = reminder_message
#         reminder.save()
#         return JsonResponse({'msg': 'Data has been updated successfully', 'status': 200}, status=200)
#     except Exception as e:
#         return JsonResponse({'msg': str(e), 'status': 500}, status=500)

# @csrf_exempt
# def delete_exercise_reminder(request):
#     if request.method != 'POST':
#         return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)
    
#     try:
#         id = request.POST['id']
#         reminder = ExerciseReminder.objects.get(id=id)
#         reminder.delete()
#         return JsonResponse({'msg': 'Data has been removed successfully', 'status': 200}, status=200)
#     except Exception as e:
#         return JsonResponse({'msg': str(e), 'status': 500}, status=500)

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


