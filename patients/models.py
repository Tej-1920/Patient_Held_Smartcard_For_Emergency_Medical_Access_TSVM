from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid
import os

class PatientManager(BaseUserManager):
    """Custom manager for Patient model"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular Patient"""
        if not email:
            raise ValueError('Patients must have an email address')
        
        email = self.normalize_email(email)
        
        # Generate username from email if not provided
        username = extra_fields.pop('username', None)
        if not username:
            username = email.split('@')[0]
        
        patient = self.model(
            email=email,
            username=username,
            **extra_fields
        )
        patient.set_password(password)
        patient.save(using=self._db)
        return patient
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser Patient"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

class Patient(AbstractUser):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient_id = models.CharField(max_length=20, unique=True, editable=False)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)  # Make username optional
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, null=True, blank=True)
    chronic_diseases = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_relation = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='patient_images/', null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = PatientManager()
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='patient_users',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='patient_users',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']
    
    def save(self, *args, **kwargs):
        if not self.patient_id:
            self.patient_id = f"PT{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)
        
        # Generate QR code after saving
        self.generate_qr_code()
    
    def generate_qr_code(self):
        """Generate QR code for patient card"""
        try:
            import qrcode
            from io import BytesIO
            from django.core.files import File
            
            # Create QR code data with patient information
            qr_data = f"""
PATIENT SMART CARD
================
Patient ID: {self.patient_id}
Name: {self.first_name} {self.last_name}
Email: {self.email}
Phone: {self.phone_number}
Blood Group: {self.blood_group or 'N/A'}
Date of Birth: {self.date_of_birth or 'N/A'}
Emergency Contact: {self.emergency_contact_name or 'N/A'}
Emergency Phone: {self.emergency_contact_phone or 'N/A'}
================
            """.strip()
            
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            # Create QR code image
            qr_img = qr.make_image(fill_color="black", back_color="white")
            
            # Save QR code to file
            buffer = BytesIO()
            qr_img.save(buffer, format='PNG')
            buffer.seek(0)
            
            # Generate filename
            filename = f"qr_{self.patient_id}.png"
            
            # Save to model
            self.qr_code.save(filename, File(buffer), save=False)
            
        except ImportError:
            # If qrcode library is not installed, skip QR generation
            pass
        except Exception as e:
            # Log error but don't break the save process
            print(f"Error generating QR code for patient {self.patient_id}: {e}")
    
    def get_qr_data(self):
        """Get QR code data as string"""
        return f"""
PATIENT SMART CARD
================
Patient ID: {self.patient_id}
Name: {self.first_name} {self.last_name}
Email: {self.email}
Phone: {self.phone_number}
Blood Group: {self.blood_group or 'N/A'}
Date of Birth: {self.date_of_birth or 'N/A'}
Emergency Contact: {self.emergency_contact_name or 'N/A'}
Emergency Phone: {self.emergency_contact_phone or 'N/A'}
================
        """.strip()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.patient_id})"

class MedicalRecord(models.Model):
    RECORD_TYPE_CHOICES = [
        ('PRESCRIPTION', 'Prescription'),
        ('LAB_RESULT', 'Lab Result'),
        ('IMAGING', 'Imaging'),
        ('DISCHARGE_SUMMARY', 'Discharge Summary'),
        ('OTHER', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    record_type = models.CharField(max_length=20, choices=RECORD_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='medical_records/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    hospital_name = models.CharField(max_length=200, blank=True)
    doctor_name = models.CharField(max_length=100, blank=True)
    date_of_record = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.patient.first_name} {self.patient.last_name}"
