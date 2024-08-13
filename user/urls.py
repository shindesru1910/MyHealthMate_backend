from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from user.views import get_user_profile
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path('',views.user,name='user'),
    path('login',views.login,name='login'),
    
    #
    # path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('', views.index, name='index'),


    path('create-user',views.create_user, name='create-user'),
    path('get-user',views.get_user, name='get-user'),
    path('update-user',views.update_user, name='update-user'),
    path('delete-user',views.delete_user, name='delete-user'),
    
    path('create-user-profile',views.create_user_profile, name='create-user-profile'),
    path('get-user-profile',views.get_user_profile, name='get-user-profile'),
    path('update-user-profile',views.update_user_profile, name='update-user-profile'),
    path('delete-user-profile',views.delete_user_profile, name='delete-user-profile'),


    path('create-doctor',views.create_doctor, name='create-doctor'),
    path('get-doctor',views.get_doctor, name='get-doctor'),
    path('get-doctor/<int:doctor_id>', views.get_doctor_by_id, name='get_doctor_by_id'),    #Get appointmemnt for appointment form
    path('update-doctor',views.update_doctor, name='update-doctor'),
    path('delete-doctor',views.delete_doctor, name='delete-doctor'),
    path('get-specialties',views.get_specialties, name="get_specialties"),
    # Form Submission of Appointment
    path('submit-appointment',views.submit_appointment, name="submit-appointment"),
    path('get-available-slots',views.get_available_slots, name="get-available-slots"),

    path('create-exercise-plan',views.create_exerciseplan, name='create-exercise-plan'),
    path('get-exercise-plan',views.get_exerciseplan, name='get-exercise-plan'),
    path('update-exercise-plan',views.update_exerciseplan, name='update-exercise-plan'),
    path('delete-exercise-plan',views.delete_exerciseplan, name='delete-exercise-plan'),
    
    path('create-diet-plan',views.create_diet_plan, name='create-diet-plan'),
    path('get-diet-plan',views.get_diet_plan, name='get-diet-plan'),
    path('update-diet-plan',views.update_diet_plan, name='update-diet-plan'),
    path('delete-diet-plan',views.delete_diet_plan, name='delete-diet-plan'),

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
    path('get-appointments-by-user', views.get_appointments_by_user, name='get_appointments_by_user'),
    path('update-appointment',views.update_appointment, name='update-appointment'),
    path('delete-appointment',views.delete_appointment, name='delete-appointment'),


    path('create-feedback',views.create_feedback, name='create-feedback'),
    path('get-feedback',views.get_feedback, name='get-feedback'),
    path('update-feedback',views.update_feedback, name='update-feedback'),
    path('delete-feedback',views.delete_feedback, name='delete-feedback'),

    
    # path('send-reminder-email', views.send_reminder_email, name='send-reminder-email'),
    path('sendmail/',views.send_mail_to_all, name="sendmail"),

    
    path('upload-file', views.upload_file, name='upload-file'),
    path('get-user-files',views.get_user_files, name= 'get-user-files'),


    path('password-reset-request', views.password_reset_request, name='password-reset-request'),
    # path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password-reset-confirm'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('', TemplateView.as_view(template_name='index.html')), 


    path('api/get-user-profile/', get_user_profile, name='get_user_profile'),
    path('get-exercise-recommendations', views.get_exercise_recommendations, name='get-exercise-recommendations'),
    path('get-diet-recommendations', views.get_diet_recommendations, name='get-diet-recommendations'),


    path('generate-system-report',views.generate_system_report, name= 'generate-system-report'),
    path('get-upcoming-appointments',views.get_upcoming_appointments, name= 'get-upcoming-appointments'),

    path('api/users/<int:user_id>/',views.get_user_for_appointment, name='get_user'),
    path('api/doctors/<int:doctor_id>/',views.get_doctor_for_appointment, name='get_doctor'),
    path('api/delete-appointment/', views.delete_appointments, name='delete_appointment'),
    path('api/appointments/', views.get_appointments, name='get_appointments'),

    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.list_files, name='list_files'),
    path('download/<str:filename>/', views.download_file, name='download_file'),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
