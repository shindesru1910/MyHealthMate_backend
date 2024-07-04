import pytz
import os
from django.db.models import Sum
# import jwt
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . models import *
from datetime import datetime,timezone,timedelta
from django.contrib.auth import authenticate, login
# from .authentication import create_token
# from firebase_admin import credentials
# from firebase_admin import firestore
from django.conf import settings

ist_timezone = pytz.timezone('Asia/Kolkata')

@csrf_exempt

def create_user(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Invalid Request','status':403},status=400)
    
    try:
        phone = request.POST['phone']
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            return JsonResponse({'msg':'email is already Exitst','status':404},status=200)

        user_user = User(email=email)
        user_user.save()
        return JsonResponse({'msg':'Data has been successfully created','status':200},status = 200)
    except Exception as e:
        return JsonResponse({'msg':str(e),'status':500},status = 200)
