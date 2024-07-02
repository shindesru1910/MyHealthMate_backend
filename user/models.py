from django.db import models
class user(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(null=False, max_length=50,default='default_password')
    email = models.EmailField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserProfile(models.Model):
    MEMBERSHIP_STATUS = [('regular', 'Regular'), ('premium', 'Premium')]
    user = models.OneToOneField(user, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=6, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    medical_history = models.TextField(blank=True, null=True)
    health_goals = models.TextField(blank=True, null=True)
    membership_status = models.CharField(max_length=7, choices=MEMBERSHIP_STATUS, default='regular')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Doctor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    specialty = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=255)
    reviews = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class HealthRecommendation(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    diet_recommendations = models.TextField()
    exercise_recommendations = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class HealthReport(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    report_name = models.CharField(max_length=255)
    report_file = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ExerciseReminder(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    reminder_time = models.TimeField()
    reminder_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Feedback(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    feedback_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
# Create your models here.
