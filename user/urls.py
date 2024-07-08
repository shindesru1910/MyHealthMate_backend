from django.urls import path
from . import views

urlpatterns = [
    path('create-user',views.create_user, name='create-user'),
    path('get-user',views.get_user, name='get-user'),
    path('update-user',views.update_user, name='update-user'),
    path('delete-user',views.delete_user, name='delete-user'),

#UserProfile Baaki hai

    path('create-doctor',views.create_doctor, name='create-doctor'),
    path('get-doctor',views.get_doctor, name='get-doctor'),
    path('update-doctor',views.update_doctor, name='update-doctor'),
    path('delete-doctor',views.delete_doctor, name='delete-doctor'),

    path('create-exerciseplan',views.create_exerciseplan, name='create-exerciseplan'),
    path('get-exerciseplan',views.get_exerciseplan, name='get-exerciseplan'),
    path('update-exerciseplan',views.update_exerciseplan, name='update-exerciseplan'),
    path('delete-exerciseplan',views.delete_exerciseplan, name='delete-exerciseplan'),
    
    path('create-health-recommendation',views.create_health_recommendation, name='create-health-recommendation'),
    path('get-health-recommendation',views.get_health_recommendation, name='get-health-recommendation'),
    path('update-health-recommendation',views.update_health_recommendation, name='update-health-recommendation'),
    path('delete-health-recommendation',views.delete_health_recommendation, name='delete-health-recommendation'),

    path('create-health-report',views.create_health_report, name='create-health-report'),
    path('get-health-report',views.get_health_report, name='get-health-report'),
    path('update-health-report',views.update_health_report, name='update-health-report'),
    path('delete-health-report',views.delete_health_report, name='delete-health-report'),

    path('create-appointment',views.create_appointment, name='create-appointment'),
    path('get-appointment',views.get_appointment, name='get-appointment'),
    path('update-appointment',views.update_appointment, name='update-appointment'),
    path('delete-appointment',views.delete_appointment, name='delete-appointment'),
   
    path('create-exercise-reminder',views.create_exercise_reminder, name='create-exercise-reminder'),
    path('get-exercise-reminder',views.get_exercise_reminder, name='get-exercise-reminder'),
    path('update-exercise-reminder',views.update_exercise_reminder, name='update-exercise-reminder'),
    path('delete-exercise-reminder',views.delete_exercise_reminder, name='delete-exercise-reminder'),

    path('create-feedback',views.create_feedback, name='create-feedback'),
    path('get-feedback',views.get_feedback, name='get-feedback'),
    path('update-feedback',views.update_feedback, name='update-feedback'),
    path('delete-feedback',views.delete_feedback, name='delete-feedback'),

    ]
