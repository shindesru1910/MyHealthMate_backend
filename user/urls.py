from django.urls import path
from . import views

urlpatterns = [
    path('create-user/',views.create_user, name='create-user'),
    path('get-user/',views.get_user, name='get-user'),
    path('delete-user/',views.delete_user, name='delete-user'),
    path('create-doctor/',views.create_doctor, name='create-doctor'),
    
    ]
