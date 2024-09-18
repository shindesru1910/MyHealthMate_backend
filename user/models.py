from django.conf import settings
from django.db import models
from django.contrib.auth.models import(BaseUserManager, AbstractBaseUser)
from django.contrib.auth.models import User
from django.forms import ValidationError

class CustomUserManager(BaseUserManager):
    def create_user(self,phone,email=None,password=None,address=None):
        # c
        if not email:
            raise ValueError('Users must have an email address')
        if not phone:
            raise ValueError('Users must have a phone number')
        
        user = self.model(
            email = email
        )
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, phone, password):
        user = self.model(
            phone=phone,

        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser):
    phone = models.BigIntegerField(null=False)
    email = models.EmailField(max_length=50,unique=True)
    first_name = models.CharField(max_length=50,null=True)
    last_name = models.CharField(max_length=50,null= True)
    date_of_birth = models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=6,null=True, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    is_admin = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    MEMBERSHIP_STATUS = [('regular', 'Regular'), ('premium', 'Premium')]
    ACTIVITY_LEVEL_CHOICES = [
    ('sedentary', 'Sedentary'),
    ('lightly_active', 'Lightly Active'),
    ('moderately_active', 'Moderately Active'),
    ('very_active', 'Very Active'),
    ('super_active', 'Super Active'),
    ]
    DIETARY_PREFERENCE_CHOICES = [
    ('vegetarian', 'Vegetarian'),
    ('vegan', 'Vegan'),
    ('gluten_free', 'Gluten-Free'),
    ('low_carb', 'Low-Carb'),
    ('high_protein', 'High-Protein'),
    ('diabetic_friendly', 'Diabetic-Friendly'),
    ('allergies', 'Allergies'),
    ]
    HEALTH_CONDITION_CHOICES=[
        ('hypertension','hypertension'),
        ('diabetes','diabetes'),
        ('asthma','asthma'),
        ('heart_disease','heart_disease'),
        ('allergy','allergy'),
        ('thyroid','thyroid'),
        ('cancer','cancer'),
        ('kidney_disease','kidney_disease'),
    ]
    MEDICAL_HISTORY_CHOICES=[
        ('previous_surgeries','previous_surgeries'),
        ('chronic_illnesses','chronic_illnesses'),
        ('medications','medications'),
        ('allergies','allergies'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weight = models.FloatField(null=False, default=0)
    height = models.FloatField(null=False, default=0)
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES,null=True)
    dietary_preferences = models.CharField(max_length=50, choices=DIETARY_PREFERENCE_CHOICES,null=True)
    health_conditions = models.TextField(null=True, choices=HEALTH_CONDITION_CHOICES)
    medical_history = models.TextField(blank=True, null=True,choices=MEDICAL_HISTORY_CHOICES)
    health_goals = models.TextField(blank=True, null=True)
    membership_status = models.CharField(max_length=7, choices=MEMBERSHIP_STATUS, default='regular')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

class DietPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=False,blank=True)
    suitable_for = models.TextField(null=False,blank=True)  # JSON field or text to describe suitability

class ExercisePlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=False,blank=True)
    suitable_for = models.TextField(null=False,blank=True)  # JSON field or text to describe suitability


class Doctor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    specialty = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=255)
    # reviews = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.specialty}"

class HealthRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    diet_plan = models.ForeignKey(DietPlan, on_delete=models.SET_NULL, null=True, blank=True)
    exercise_plan = models.ForeignKey(ExercisePlan, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class HealthReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_name = models.CharField(max_length=255)
    report_file = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

# New Appointment class to store appointment data
# class Appointment(models.Model):
#     STATUS_CHOICES = [
#         ('scheduled', 'Scheduled'),
#         ('pending', 'Pending'),
#         ('completed', 'Completed'),
#         ('cancelled', 'Cancelled'),
#     ]

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
#     appointment_date = models.DateTimeField()  # Handles both date and time
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')
#     phone = models.CharField(max_length=15, blank=True, null=True)  # For user's phone number
#     specialty = models.CharField(max_length=100, blank=True, null=True)  # For the specialty
#     message = models.TextField(blank=True, null=True)  # For any additional message
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def clean(self):
#         #validation 
#         pass



# class UserTimeslot(models.Model):
#     start_time = models.TimeField()
#     end_time = models.TimeField()
#     date = models.DateField()

#     def __str__(self):
#         return f"{self.date} from {self.start_time} to {self.end_time}"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    TIME_SLOTS = [
        ('12:00 PM', '12:00 PM'),
        ('1:00 PM', '1:00 PM'),
        ('2:00 PM', '2:00 PM'),
        ('3:00 PM', '3:00 PM'),
        ('4:00 PM', '4:00 PM'),
        ('5:00 PM', '5:00 PM'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15,null=False,blank=True)
    specialty = models.CharField(max_length=10, choices=STATUS_CHOICES,null=False,blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    time_slot = models.CharField(max_length=10, choices=TIME_SLOTS, null=False, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    message = models.TextField(null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def clean(self):
        # Custom validation logic to ensure a time slot isn't double booked
        if Appointment.objects.filter(
            doctor=self.doctor,
            appointment_date=self.appointment_date,
            time_slot=self.time_slot,
            status='scheduled'
        ).exists():
            raise ValidationError(f'The time slot {self.time_slot} on {self.appointment_date} is already booked.')


# exercise email reminder   
class EmailReminder(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    reminder_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f'Reminder for {self.email} at {self.reminder_time}'

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.user.last_name} - {self.feedback_text}"

# models.py


class HealthData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    heart_rate = models.IntegerField()
    systolic = models.IntegerField()
    diastolic = models.IntegerField()
    step_count = models.IntegerField()
    
    def __str__(self):
        return f"{self.user.username} - {self.date}"

# new models
  
# Create your models here.
