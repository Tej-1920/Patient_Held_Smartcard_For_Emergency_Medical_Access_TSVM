from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from patients.models import Patient
from doctors.models import Doctor

class CustomAuthBackend(BaseBackend):
    """
    Custom authentication backend that supports both Patient and Doctor models
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate user by checking both Patient and Doctor models
        """
        # Try to authenticate as Patient first
        try:
            patient = Patient.objects.get(email=username)
            if patient.check_password(password):
                return patient
        except Patient.DoesNotExist:
            pass
        
        # Try to authenticate as Doctor
        try:
            doctor = Doctor.objects.get(email=username)
            if doctor.check_password(password):
                return doctor
        except Doctor.DoesNotExist:
            pass
        
        return None
    
    def get_user(self, user_id):
        """
        Get user by checking both Patient and Doctor models
        """
        try:
            patient = Patient.objects.get(pk=user_id)
            return patient
        except Patient.DoesNotExist:
            pass
        
        try:
            doctor = Doctor.objects.get(pk=user_id)
            return doctor
        except Doctor.DoesNotExist:
            pass
        
        return None
