from django.urls import path
from . import views

urlpatterns = [
    path('create-user',views.create_user, name='create-user'),
    path('get-user',views.get_user, name='get-user'),
    path('update-user',views.update_user, name='update-user'),
    path('delete-user',views.delete_user, name='delete-user'),
    path('create-doctor',views.create_doctor, name='create-doctor'),
    path('get-doctor',views.get_doctor, name='get-doctor'),
    path('update-doctor',views.update_doctor, name='update-doctor'),
    path('delete-doctor',views.delete_doctor, name='delete-doctor'),
    ]
