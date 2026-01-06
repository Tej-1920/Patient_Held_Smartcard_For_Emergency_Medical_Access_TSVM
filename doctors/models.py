from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from patients.models import Patient
import uuid

class DoctorManager(BaseUserManager):
    """Custom manager for Doctor model"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular Doctor"""
        if not email:
            raise ValueError('Doctors must have an email address')
        
        email = self.normalize_email(email)
        
        # Generate username from email if not provided
        username = extra_fields.pop('username', None)
        if not username:
            username = email.split('@')[0]
        
        doctor = self.model(
            email=email,
            username=username,
            **extra_fields
        )
        doctor.set_password(password)
        doctor.save(using=self._db)
        return doctor
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser Doctor"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

class Doctor(AbstractUser):
    SPECIALIZATION_CHOICES = [
        ('GENERAL', 'General Practitioner'),
        ('CARDIOLOGY', 'Cardiology'),
        ('NEUROLOGY', 'Neurology'),
        ('PEDIATRICS', 'Pediatrics'),
        ('ORTHOPEDICS', 'Orthopedics'),
        ('GYNECOLOGY', 'Gynecology'),
        ('DERMATOLOGY', 'Dermatology'),
        ('PSYCHIATRY', 'Psychiatry'),
        ('SURGERY', 'Surgery'),
        ('EMERGENCY', 'Emergency Medicine'),
        ('OTHER', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor_id = models.CharField(max_length=20, unique=True, editable=False)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)  # Make username optional
    nmc_registration_number = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    specialization = models.CharField(max_length=20, choices=SPECIALIZATION_CHOICES)
    hospital_name = models.CharField(max_length=200)
    hospital_address = models.TextField()
    years_of_experience = models.PositiveIntegerField(default=0)
    medical_license_number = models.CharField(max_length=100, unique=True)
    state_medical_council = models.CharField(max_length=100, default='Andhra Pradesh Medical Council')
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = DoctorManager()
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='doctor_users',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='doctor_users',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'nmc_registration_number']
    
    def save(self, *args, **kwargs):
        if not self.doctor_id:
            self.doctor_id = f"DR{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} ({self.doctor_id})"

class AccessLog(models.Model):
    ACCESS_TYPES = [
        ('EMERGENCY', 'Emergency Access'),
        ('AUTHORIZED', 'Authorized Access'),
        ('ROUTINE', 'Routine Check'),
    ]
    
    VALIDATION_STATUSES = [
        ('AUTHORIZED', 'Authorized'),
        ('BLACKLISTED', 'Blacklisted'),
        ('NOT_FOUND', 'Not Found'),
        ('PENDING', 'Pending Verification'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='access_logs')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='doctor_access_logs')
    access_type = models.CharField(max_length=20, choices=ACCESS_TYPES, default='EMERGENCY')
    access_reason = models.TextField()
    accessed_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    records_viewed = models.PositiveIntegerField(default=0)
    validation_status = models.CharField(max_length=20, choices=VALIDATION_STATUSES, default='PENDING')
    registration_number_used = models.CharField(max_length=50, null=True, blank=True, help_text="Registration number used for validation")
    state_council_used = models.CharField(max_length=100, null=True, blank=True, help_text="State medical council used for validation")
    
    class Meta:
        ordering = ('-accessed_at',)
    
    def __str__(self):
        return f"Dr. {self.doctor.first_name} {self.doctor.last_name} accessed {self.patient.first_name} {self.patient.last_name} - {self.accessed_at}"
