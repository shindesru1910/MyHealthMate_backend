from django.db import models
from django.contrib.auth.models import(BaseUserManager, AbstractBaseUser)

class CustomUserMangaer(BaseUserManager):
    def create_user(self,phone,email=None,password=None,address=None):
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    objects = CustomUserMangaer()

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
    reviews = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ExerciseReminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reminder_time = models.TimeField()
    reminder_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
# Create your models here.
