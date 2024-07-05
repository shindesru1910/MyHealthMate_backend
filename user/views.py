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
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        
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
def create_doctor(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request', 'status': 403}, status=403)
    
    try:
        # Retrieve data from POST request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        specialty = request.POST.get('specialty')
        contact_info = request.POST.get('contact_info')
        reviews = request.POST.get('reviews')
        location = request.POST.get('location')

        # Create a Doctor object and save it
        doctor_obj = Doctor(first_name=first_name, last_name=last_name, specialty=specialty, contact_info=contact_info, reviews=reviews, location=location)
        doctor_obj.save()

        return JsonResponse({'msg': 'Data has been successfully created', 'status': 200}, status=200)
    except Exception as e:
        return JsonResponse({'msg': str(e), 'status': 500}, status=500)