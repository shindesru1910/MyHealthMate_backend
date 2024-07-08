import pytz
# import os
# from django.db.models import Sum
# import jwt
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . models import *
# from datetime import datetime,timezone,timedelta
from django.contrib.auth import authenticate, login
# from .authentication import create_token
# from firebase_admin import credentials
# from firebase_admin import firestore
from django.conf import settings

ist_timezone = pytz.timezone('Asia/Kolkata')

@csrf_exempt
def create_user(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)
    
    try:
        phone = request.POST['phone']
        email = request.POST.get['email']
        
        if not phone or not email:
            return JsonResponse({'msg': 'Phone and email are required', 'status': 400}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'msg': 'Email already exists', 'status': 404}, status=404)

        user_user = User.objects.create(email=email, phone=phone)
        user_user.save()
        return JsonResponse({'msg': 'Data has been successfully created', 'status': 200}, status=200)
    except Exception as e:
        return JsonResponse({'msg': str(e), 'status': 500}, status=500)


@csrf_exempt
def get_user(request):
    try:
        users = User.objects.all()
        data = []

        for user in users:
            user_dict ={}
            user_dict['id'] = user.id
            user_dict['phone'] = user.phone
            user_dict['email'] = user.email


            data.append(user_dict)
        return JsonResponse({'data':data,'status':200},status = 200)
    except Exception as e:
        return JsonResponse({'data':str(e),'status':500},status = 200)
    
@csrf_exempt
def update_user(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request','status':403},status = 200)
    try:
        id = request.POST['id']
        phone = request.POST['phone']
        email = request.POST['email']

        user = User.objects.get(id = id)
        user.phone = phone
        user.email = email
        user.save()
        return JsonResponse({'msg':'Data has been updated successfully','status':200},status = 200)
    except Exception as e:
        return JsonResponse({'msg':str(e),'status':500},status = 200)
    
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


#USER PROFILE BAAKI HAI 

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

        user = Doctor.objects.get(id = id)
        user.delete()

        return JsonResponse({'msg':'Data has been removed successfully','status':200},status=200)
    except Exception as e:
        return JsonResponse({'msg':str(e),'status':500},status=200)
    
@csrf_exempt
def create_health_recommendation(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)
    
    try:
        user_id = request.POST['user']
        diet_recommendations = request.POST['diet_recommendations']
        exercise_recommendations = request.POST['exercise_recommendations']
        
        user = User.objects.get(id=user_id)
        recommendation = HealthRecommendation(
            user=user, diet_recommendations=diet_recommendations,
            exercise_recommendations=exercise_recommendations
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
            recommendation_dict['diet_recommendations'] = recommendation.diet_recommendations
            recommendation_dict['exercise_recommendations'] = recommendation.exercise_recommendations
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

@csrf_exempt
def get_feedback(request):
    try:
        feedbacks = Feedback.objects.all()
        data = []

        for feedback in feedbacks:
            feedback_dict = {}
            feedback_dict['id'] = feedback.id
            feedback_dict['user'] = feedback.user.id
            feedback_dict['feedback_text'] = feedback.feedback_text
            feedback_dict['created_at'] = feedback.created_at

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

